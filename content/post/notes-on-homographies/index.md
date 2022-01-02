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

## Solving for a Homography Given 2D Correspondences

To solve for a homography 4 correspondences are required. Given the locations of these points it is possible to construct a linear
equation system and solve for the entries of the homography matrix. The relation between the image points and the homography is given by:

$$
\begin{aligned}
b_i &= \Pi \left( H \begin{pmatrix} a_i \\ 1 \end{pmatrix} \right)
\end{aligned}
$$

The homography is a 3x3 matrix which maps from the domain of $$a_i$$ to $$b_i$$. It works on homogeneous coordinates which is why $$a_1$$
is extended with a third entry above. $$\Pi$$ denotes the perspective projection which maps 3d vectors into 2d by dividing by its third component:

$$
\begin{aligned}
\Pi \left( \begin{pmatrix} x \\ y \\ z \end{pmatrix} \right) &= \frac{1}{z} \begin{pmatrix} x \\ y \end{pmatrix} \\
\end{aligned}
$$


For our derivation we expect the homography to map the z component of $$y_i$$ to 1. This way the projection is not necessary and can be skipped.
Furthermore only 8 unknowns can be found with 4 correspondences (of dimension 2 each) which is why one of the matrix elements has to be fixed,
$$h_{33} = 1$$ is common.

$$
\begin{aligned}
\begin{pmatrix} b_{ix} \\ b_{iy} \\ b_{iz} \end{pmatrix} &= 
\begin{pmatrix} h_{11} a_{ix} + h_{12} a_{iy} + h_{13} a_{iz} \\ h_{21} a_{ix} + h_{22} a_{iy} + h_{23} a_{iz} \\ h_{31} a_{ix} + h_{32} a_{iy} + h_{33} a_{iz} \end{pmatrix} \\
\\
\begin{pmatrix} b_{ix} \\ b_{iy} \\ 1 \end{pmatrix} &= 
\begin{pmatrix} h_{11} a_{ix} + h_{12} a_{iy} + h_{13} \\ h_{21} a_{ix} + h_{22} a_{iy} + h_{23} \\ h_{31} a_{ix} + h_{32} a_{iy} + 1 \end{pmatrix} \\
\end{aligned}
$$





$$
\begin{aligned}
A &= n \cdot a = n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) \\
A &= \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) = \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \frac{2\pi}{n} = \pi r^2
\end{aligned}
$$


## Transforming Existing Homographies


This section is an extension on [one](https://stackoverflow.com/a/48915151) of my answers that I gave on stackoverflow. If a homography was computed for a certain set of
correspondences, but needs to be used on a different scale or relative to a different coordinate frame there are ways to modify it accordingly instead of recomputing it.

### Scale and Translation

$$
\begin{aligned}
A &= n \cdot a = n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) \\
A &= \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) = \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \frac{2\pi}{n} = \pi r^2
\end{aligned}
$$


It is possible to include rotation as well, however since the equations got massive and there was no obvious usecase, it was excluded. Do these formulas lead to improvmenets w.r.t. runtime? Probably not, as solving for a homography with new correspondences is not very expensive either.
It was a nice exercise, anyway. Check the next sections for shorthands on the specific cases and some usecases.

### Only Scale


usecase: do tracking on lower scale, but visualization on original scale


### Only Translation

usecase: solve for homography, but use cv warp to warp image which is to the left and top of origin


