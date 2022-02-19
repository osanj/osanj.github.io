---
title: How to Retrieve Video Frames Efficiently from S3 Buckets
date: 2022-02-18
tags: ["software engineering", "python"]
markup: "mmark"
use_math: false
use_justify: true
---

Let's say you have lot's of video files stored in a S3 Bucket and you want to retrieve specific frames from these. How could it be done efficiently?

<!--more-->

## The Problem

Some kind of service which serves the correct frame for a given frame index from a remotely stored file and uses a minimum amount of bandwidth

will be using MinIO and pyAV in this example.


## Keyframes in Videos



## Seeking in Videos




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


