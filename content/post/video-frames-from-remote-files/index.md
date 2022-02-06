---
title: How to Retrieve Video Frames Efficiently from S3 Buckets
date: 2022-02-06
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

...

> `def write(self, b: bytes) -> None: ...`

...

> `def seek(self, delta: int, whence: int) -> None: ...`


sets `offset` of the object depending on `whence`
* `offset = delta` for `whence == 0` (relative to beginning of the file)
* `offset = offset + delta` for `whence == 1` (relative to the current offset)
* `offset = n + delta` for `whence == 2` (relative to the end of the file, usually `delta` is negative in this case)


> `def tell(self) -> int: ...`

...

