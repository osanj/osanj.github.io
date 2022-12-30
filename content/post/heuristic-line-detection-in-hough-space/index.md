---
title: A Heuristic Method to Find Multiple Lines in a Hough Space
date: 2022-12-29
tags: ["math", "computer vision"]
markup: "mmark"
use_math: true
use_justify: true
---

The Hough Transform is great. Detecting the longest line in an Hough accumulator is easy (the global maximum), but detecting multiple lines (local maxima) is not so trivial.

<!--more-->



### Hough Transform Recap

bla


example binarized image

example hough accumulator image (with python code)


### OpenCV Implementation


doc 4.7.0
https://docs.opencv.org/4.7.0/dd/d1a/group__imgproc__feature.html#ga46b4e588934f6c8dfd509cc6e0e4545a

HoughLinesStandard
https://github.com/opencv/opencv/blob/725e440d278aca07d35a5e8963ef990572b07316/modules/imgproc/src/hough.cpp#L119-L124

findLocalMaximums
https://github.com/opencv/opencv/blob/725e440d278aca07d35a5e8963ef990572b07316/modules/imgproc/src/hough.cpp#L95-L108


### Pick and Erase

bla


