---
title: How to Efficiently Retrieve Video Frames from MinIO using pyAV
date: 2022-02-18
tags: ["software engineering", "python"]
markup: "mmark"
use_math: false
use_justify: true
---

A video is made up of frames, but retrieving a specific frame from a video file is not straight forward.

<!--more-->

## The Problem

Let's say you have a dataset of video files stored in some kind of object storage. Also, in some script you need to access specific frames and now you want to build a service which provides the following interface:

> `def get_frame(self, video_path: str, frame_index: int) -> npt.NDArray[np.uint8]: ...`

In words: for a given video and frame number the decoded frame (3 channel matrix) should be returned.

In this article the storage solution is [MinIO](https://min.io) ([which uses the same interface like S3 buckets on AWS](https://min.io/product/s3-compatibility)). For video decoding [pyAV](https://github.com/PyAV-Org/PyAV) is used which is one of the few libraries that provides _native_ bindings to libAV, many other packages [provide a glorified ffmpeg interface using `subprocess`](https://github.com/kkroening/ffmpeg-python/blob/f3079726fae7b7b71e4175f79c5eeaddc1d205fb/ffmpeg/_run.py#L288-L291).  (which is like starting a shell and printing a generated command in there, meh).


## A Basic Solution

Some kind of service which serves the correct frame for a given frame index from a remotely stored file and uses a minimum amount of bandwidth

will be using MinIO and pyAV in this example.


{{< highlight Python >}}
pass
{{< / highlight >}}


## Keyframes in Videos



## Seeking in Videos

{{< highlight Python >}}
pass
{{< / highlight >}}


## Wrapping a Remote File as a File Like Object

reference to the pyAV docs

reference to Python IO docs

reference to AWS Rest API

reference to MinIO Rest API


> `def read(self, n: int = -1) -> bytes: ...`

Returns `n` bytes starting at `offset`. If less than `n` bytes are left, only the remaining bytes will be returned. If `-1` is passed, all remaining bytes from `offset` will be returned. Afterwards `offset` is set to the position after the last byte which was returned.


> `def write(self, b: bytes) -> None: ...`

Replaces `len(b)` bytes starting from `offset`. Afterwards `offset` is set to the position after the last written byte.



> `def seek(self, delta: int, whence: int) -> None: ...`:

Updates `offset` depending on `whence`
* `whence == 0`: `offset = delta` (relative to beginning of the file)
* `whence == 1`: `offset = offset + delta` (relative to the current offset)
* `whence == 2`: `offset = n + delta` (relative to the end of the file, usually `delta` is negative in this case)


> `def tell(self) -> int: ...`

Returns the current `offset`.


{{< highlight Python >}}
pass
{{< / highlight >}}


## Putting Things Together

{{< highlight Python >}}
pass
{{< / highlight >}}


