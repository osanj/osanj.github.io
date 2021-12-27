---
title: Notes on Homographies
date: 2021-12-27
tags: ["math"]
markup: "mmark"
use_math: true
use_justify: true
---

This is writeup of some formulas that proofed to be helpful understanding and working with homographies.

<!--more-->

## Solving for a Homography Given 4 Pairs of 2D Correspondences

$$
\begin{aligned}
A &= n \cdot a = n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) \\
A &= \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) = \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \frac{2\pi}{n} = \pi r^2
\end{aligned}
$$


## Transforming Existing Homographies


I wanted to extend upon the [answer](https://stackoverflow.com/a/48915151) that I gave on stackoverflow. If a homography was computed for a certain set of
correspondences, but needs to be used on a different scale or relative to a different coordinate frame there are ways to modify it accordingly instead of recomputing it.

### General Form


I initially included rotation, but the equations got massive and I could not really find a usecase for it. Do these formulas lead to improvmenets w.r.t. runtime? Probably not, as solving for a homography with new correspondences is not very expensive either.
It was a nice exercise, anyway. Check the next sections for shorthands on the specific cases and some usecases.

### Only Scale


usecase: do tracking on lower scale, but visualization on original scale


### Only Translation

usecase: solve for homography, but use cv warp to warp image which is to the left and top of origin


