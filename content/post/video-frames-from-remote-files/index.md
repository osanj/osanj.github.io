---
title: How to Efficiently Retrieve Video Frames from MinIO using pyAV
date: 2022-02-18
tags: ["software engineering", "python"]
markup: "mmark"
use_math: false
use_justify: true
---

A video is made up of frames, but retrieving a specific frame from a video file is not straight forward. What if the video file is stored remotely?

<!--more-->

&nbsp;

## The Problem

Let's say you have a dataset of video files stored in some kind of object storage and in some script you need to access _specific_ frames. In this post the storage solution is [MinIO](https://min.io) ([which uses the same interface like S3 buckets on AWS](https://min.io/product/s3-compatibility)). For video decoding [pyAV](https://github.com/PyAV-Org/PyAV) is used which is one of the few libraries that provide _native_ bindings to ffmpeg, especially to the ffmpeg module which performs the actual encoding and decoding. Many other packages [provide a glorified ffmpeg interface using `subprocess`](https://github.com/kkroening/ffmpeg-python/blob/f3079726fae7b7b71e4175f79c5eeaddc1d205fb/ffmpeg/_run.py#L288-L291) (which is like starting a shell and sending your generated command there, meh).

The aim is to provide the following interface:

`def get_frame(client: Minio, video_id: str, frame_index: int) -> npt.NDArray[np.uint8]:`

In words: given a client, a video id and a frame number the decoded frame (3 channel unsigned char matrix) should be returned.

A quick and dirty solution would be to download the entire videofile and then loop over the frames ([e.g. with opencv](https://docs.opencv.org/4.5.5/dd/d43/tutorial_py_video_display.html)) until you get the one you are looking for. If only short videos are stored or this is only used very rarely, it is fine. However, doing this in a system with reasonable traffic sounds inefficient, for a single frame the entire file needs to be downloaded. Let's say you want to create thumbnails for movie files, you would need to download the _entire_ movie just to extract a single frame - that does not sound right :no_good:

To come up with a somewhat reasonable solution we first need to gain some understanding on how videos are encoded.

&nbsp;

## A High-Level Understanding of Video Compression

For images we use encodings like JPEG or PNG. A video is a series of images (a.k.a frames), so just encode every frame with some image encoding, right? Well, no. Video encoding is a bit more involved. To reach reasonable compression rates, proper video encoding algorithms exploit the fact that consecutive frames likely show a lot of similar information. The basic idea is instead of storing that information for each frame, it is possible to store it once and then reuse it for some time with additional information, e.g. some kind of offset or scale. Video encoding is a true [rabbit hole](https://last.hit.bme.hu/download/vidtech/k%C3%B6nyvek/Iain%20E.%20Richardson%20-%20H264%20(2nd%20edition).pdf), all kinds of traditional signal and image processing concepts are thrown at the problem: Optical flow for motion estimation, discrete cosine transform for frequency decomposition of blocks, signal quantization, you name it.

![frame types](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/I_P_and_B_frames.svg/1024px-I_P_and_B_frames.svg.png)

For this usecase all these details are not important, however the notion that most frames only store partial information is important, more details [here](https://ottverse.com/i-p-b-frames-idr-keyframes-differences-usecases/). Only keyframes (also called I-frames) contain all the information of the specific frame, other frames depend on the nearest keyframe before as well as intermediate frames.

&nbsp;

## Seeking in Videos

Armed with the knowledge of keyframes, there is a path forward for efficient frame retrieval. Assuming - of course - your video files have a reasonable distribution of keyframes! If a video is encoded with the first frame being the only keyframe, there is no way to retrieve frames without processing _all_ frames before it. In the video player of your choice there would be noticable delays if you jump to different places of the video. If you want to check your video files, `ffprobe` can be used to [list the timestamps](https://stackoverflow.com/a/18088156) of the keyframes:

```bash
ffprobe -loglevel error -skip_frame nokey -select_streams v:0 -show_entries frame=pkt_pts_time -of csv=print_section=0 some_video.mp4
0.000000
10.010000
20.020000
30.030000
39.039000
46.296244
51.259544
56.598211
61.019289
...
```

It should be clear now that the keyframe distribution defines how efficiently frames can be accessed. Since storing more keyframes likely increases redundancy, it will lead to a larger video file. Anyway, most videos do have a reasonable distribution of keyframes, so let's move on. The concept of frame retrieval is now fairly clear:

1. for a given frame index, find the the closest keyframe _before_ that frame index
2. start decoding from that keyframe until the desired frame is reached

So far, so good. Unfortunately, there is another obstacle in our way. There is no reliable frame index available in the [data structure for video frames](https://libav.org/documentation/doxygen/release/9/structAVFrame.html), see [discussion in pyAV](https://github.com/PyAV-Org/PyAV/issues/33) for more details. One reliable part of the frame data structure is the frame timestamp. We have to update our retrieval algorithm:

1. for a given frame index, find the corresponding frame timestamp
2. find the the closest keyframe _before_ that frame timestamp
3. start decoding from that keyframe until the desired frame is reached

For mapping an index to a timestamp it seems like there is no functionality built into ffmpeg (or pyAV). If the video in question has a _constant frame rate_, the frame timestamp could be computed as `frame_timestamp = frame_index / frame_rate` where `frame_rate` has unit frames per second. For videos of variable frame rate the only option is store the mapping from frame index to frame timestamp separately. For the rest of this post we will assume there is a function available to perform this mapping:

`def map_frame_index_to_ts(video_id: str, frame_index: int) -> float`

&nbsp;

## Seeking in pyAV

For now we will focus on local files, the interface looks like this:

`def get_frame_from_video(video_file: typing.BinaryIO, frame_ts: float) -> npt.NDArray[np.uint8]: ...`

The argument `video_file` is type hinted as a binary IO object, i.e. files opened in binary mode (e.g. `open(video_file_path, "rb")`) or bytes wrapped in a `io.BytesIO` object can be passed here. Apart from that there is not much left to say, here is the implementation:

{{< highlight Python >}}
import typing
import warnings

import av
import numpy.typing as npt


def get_frame_from_video(video_file: typing.BinaryIO,
                         frame_ts: float) -> npt.NDArray[np.uint8]:
    container = av.open(io_obj, mode="r")
    stream = container.streams.video[0]
    offset = int(frame_ts / stream.time_base)

    # offset needs to be in the time base of the stream
    # any_frame=False means seek only to keyframes
    # backward=True means seek before the given offset (not behind)
    container.seek(stream=stream, offset=offset,
                   any_frame=False, backward=True)

    prev_frame = None
    located_frame = None

    for frame in container.decode(stream):
        if frame.time < frame_ts:
            prev_frame = frame
            continue

        elif frame.time == frame_ts or prev_frame is None:
            located_frame = frame

        else:
            warnings.warn("Could not find a frame at exactly "
                          f"{frame_ts}s, picking closest...")
            dist = abs(frame_ts - frame.time)
            dist_prev = abs(frame_ts - prev_frame.time)
            located_frame = frame if dist < dist_prev else prev_frame
        
        break

    if located_frame is None:
        raise RuntimeError(f"Could not get frame at {frame_ts}s")

    f: npt.NDArray[np.uint8]
    f = located_frame.reformat(format="bgr24").to_ndarray()
    return f
{{< / highlight >}}

&nbsp;

## Wrapping a Remote File as a File Like Object

Now that we have the seeking figured out, we can work on applying it on remote files directly. Since it is possible to pass any file-like object to pyAV, literally _anything_ can be passed as long as the object behaves accordingly (:duck: typing, yeah!). But what is a file-like object? From [peeking into the pyAV 8.1.0 code](https://github.com/PyAV-Org/PyAV/blob/f4a9df04dc08d28d1198af7b5550ad1e37b99aa5/av/container/core.pyx#L169-L175) and reading through [Python's I/O docs](https://docs.python.org/3/library/io.html) it can be concluded that the following four methods are required:

---

`def read(self, n: int = -1) -> bytes: ...` ([docs](https://docs.python.org/3/library/io.html#io.RawIOBase.read))

Returns `n` bytes starting at `offset`. If less than `n` bytes are left, only the remaining bytes will be returned. If `-1` is passed, all remaining bytes from `offset` will be returned. Afterwards `offset` is set to the position after the last byte which was returned.

---

`def write(self, b: bytes) -> None: ...` ([docs](https://docs.python.org/3/library/io.html#io.RawIOBase.write))

Replaces `len(b)` bytes starting from `offset`. Afterwards `offset` is set to the position after the last written byte.

---

`def seek(self, delta: int, whence: int) -> None: ...` ([docs](https://docs.python.org/3/library/io.html#io.IOBase.seek))

Updates `offset` depending on `whence`
* `whence == 0`: `offset = delta` (relative to beginning of the file)
* `whence == 1`: `offset = offset + delta` (relative to the current offset)
* `whence == 2`: `offset = n + delta` (relative to the end of the file, usually `delta` is negative in this case)

---

`def tell(self) -> int: ...` ([docs](https://docs.python.org/3/library/io.html#io.IOBase.tell))

Returns the current `offset`.

---

The API of MinIO provides the functionality required to construct a class which behaves like a file-like object for a given MinIO object:
* `get_object` allows to retrieve partial files with `offset` and `length` ([docs](https://docs.min.io/docs/python-client-api-reference.html#get_object))
* `stat_object` allows to retrieve the file size ([docs](https://docs.min.io/docs/python-client-api-reference.html#stat_object))

Files stored on MinIO are also referred to as objects, so the terminology is not clearly separated here, but the implementation below should make it clear. Note that since we are only decoding (reading) videos, it won't be required to implement the `write` method.

{{< highlight Python >}}
from minio import Minio


class MinioFile(object):

    def __init__(self, client: Minio, bucket_name: str,
                 obj_name: str):
        self.client = client
        self.bucket_name = bucket_name
        self.obj_name = obj_name
        self.offset = 0
        self.overall_read = 0
        stat = self.client.stat_object(bucket_name, obj_name)
        self.size = int(stat.size)

    def read(self, size: int = -1) -> bytes:
        if offset == self.size:
            return bytes()
        if size < 0:
            size = self.size - self.offset
        resp = self.client.get_object(self.bucket_name, self.obj_name,
                                      offset=self.offset, length=size)
        self.offset += len(resp.data)

        # # for debugging how much bytes were transferred
        # self.overall_read += len(resp.data)
        # rel_read = self.overall_read / self.size
        # print(f"read {size} bytes (overall {100 * rel_read:.02f}%)")

        return bytes(resp.data)

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> None:
        if whence == io.SEEK_SET:
            self.offset = offset
        elif whence == io.SEEK_CUR:
            self.offset += offset
        elif whence == io.SEEK_END:
            self.offset = self.size + offset
        else:
            raise RuntimeError(f"Unknown whence value: {whence}")

    def tell(self) -> int:
        return self.offset
{{< / highlight >}}

&nbsp;

## Putting Things Together

![https://imgur.com/XtwwylS](data/satisfying_high_precision_machining.gif)

{{< highlight Python >}}
from minio import Minio
import numpy.typing as npt


def get_frame(client: Minio, video_id: str,
              frame_index: int) -> npt.NDArray[np.uint8]:
    bucket, path = video_id.split("/", maxsplit=1)
    video_obj = MinioFile(client, bucket, path)
    frame_timestamp = map_frame_index_to_ts(video_id, frame_index)
    return get_frame_from_video(video_obj, frame_timestamp)
{{< / highlight >}}

Some remarks:

* it is assumed that `video_id` is formatted like `[bucket]/[path/in/bucket]`
* the implementation of `map_frame_index_to_ts` is up to the reader (see options in the section about seeking)
* this was developed and tested with [pyAV 8.1.0](https://github.com/PyAV-Org/PyAV/tree/v8.1.0) and [minIO 7.1.3](https://github.com/minio/minio-py/tree/7.1.3)
* make sure to install the [pyAV dependencies](https://pyav.org/docs/stable/overview/installation.html#dependencies)

That's it, hope it was helpful :slightly_smiling_face:

