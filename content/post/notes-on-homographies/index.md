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

It is based on some notes I made along the last few years. I apologize upfront for missing references and bad notation.


## Solving for a Homography Given 2D Correspondences

To solve for a homography 4 correspondences are required. Given the locations of these points it is possible to construct a linear
equation system and solve for the entries of the homography matrix. The relation between the image points and the homography is given by:

$$
\begin{aligned}
\begin{pmatrix} X_i \\ Y_i \end{pmatrix} = \Pi \left( H \begin{pmatrix} x_i \\ y_i \\ 1 \end{pmatrix} \right)
 = \Pi \left( \begin{pmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{pmatrix} \begin{pmatrix} x_i \\ y_i \\ 1 \end{pmatrix} \right)
\end{aligned}
$$

The homography is a 3x3 matrix which maps from the domain of $$\left(\begin{smallmatrix} x_i \\ y_i \end{smallmatrix}\right)$$ to $$\left(\begin{smallmatrix} X_i \\ Y_i \end{smallmatrix}\right)$$. It works on homogeneous coordinates which is why a 1 was added above. $$\Pi$$ denotes the perspective projection which maps 3d vectors into 2d by dividing by its third component:

$$
\begin{aligned}
\Pi \left( \begin{pmatrix} x \\ y \\ z \end{pmatrix} \right) &= \frac{1}{z} \begin{pmatrix} x \\ y \end{pmatrix} \\
\end{aligned}
$$

To use the correspondences of the target domain the perspective projection needs to be undone. Therefore we consider the direct output of the matrix multiplication with $$H$$:

$$
\begin{aligned}
\begin{pmatrix} \tilde{X}_i \\ \tilde{Y}_i \\ \tilde{Z}_i \end{pmatrix} = \begin{pmatrix} X_i \cdot \tilde{Z}_i \\ Y_i \cdot \tilde{Z}_i \\ \tilde{Z}_i \end{pmatrix} = H \begin{pmatrix} x_i \\ y_i \\ 1 \end{pmatrix}
\end{aligned}
$$

Now it is time to expand the matrix multiplication, so we get 3 equations:

$$
\begin{aligned}
X_i \cdot \tilde{Z}_i &= h_{11} x_i + h_{12} y_i + h_{13} \\
Y_i \cdot \tilde{Z}_i &= h_{21} x_i + h_{22} y_i + h_{23} \\
\tilde{Z}_i &= h_{31} x_i + h_{32} y_i + h_{33}
\end{aligned}
$$

The next steps are not that obvious IMO:

1. Since the correspondences are only available in the 2d space the third equation above itself does not help to solve for unknowns, this means we have 2x4 equations for 9 unknowns and the solution is up to scale. In this case we can just fix one of the matrix values and be done with it, a common choice is $$h_{33} = 1$$

2. With this additional constraint we can plug the equation for $$\tilde{Z}_i$$ in the other equations and arrange them in a way that all $$H$$ related terms are on one side and all other terms are on the opposite side

$$
\begin{aligned}
\\
X_i \cdot \left( h_{31} x_i + h_{32} y_i + 1 \right) &= h_{11} x_i + h_{12} y_i + h_{13} \\
h_{31} x_i X_i + h_{32} y_i X_i + X_i &= h_{11} x_i + h_{12} y_i + h_{13} \\
X_i &= h_{11} x_i + h_{12} y_i + h_{13} - h_{31} x_i X_i - h_{32} y_i X_i \\ \\
Y_i \cdot \left( h_{31} x_i + h_{32} y_i + 1 \right) &= h_{21} x_i + h_{22} y_i + h_{23} \\
h_{31} x_i Y_i + h_{32} y_i X_i + Y_i &= h_{21} x_i + h_{22} y_i + h_{23} \\
Y_i &= h_{21} x_i + h_{22} y_i + h_{23} - h_{31} x_i Y_i - h_{32} y_i Y_i
\\
\end{aligned}
$$

With all four pairs of equations ($$i = 1, 2, 3, 4$$), it is possible to construct one large linear equation system where the unknown entries of the homography are stacked in a vector:

$$
\begin{pmatrix} X_1 \\ X_2 \\ X_3 \\ X_4 \\ Y_1 \\ Y_2 \\ Y_3 \\ Y_4 \end{pmatrix} =
\begin{pmatrix}
x_1 & y_1 & 1 & 0 & 0 & 0 & -x_1 X_1 & -y_1 X_1 \\
x_2 & y_2 & 1 & 0 & 0 & 0 & -x_2 X_2 & -y_2 X_2 \\
x_3 & y_3 & 1 & 0 & 0 & 0 & -x_3 X_3 & -y_3 X_3 \\
x_4 & y_4 & 1 & 0 & 0 & 0 & -x_4 X_4 & -y_4 X_4 \\
0 & 0 & 0 & x_1 & y_1 & 1 & -x_1 Y_1 & -y_1 Y_1 \\
0 & 0 & 0 & x_2 & y_2 & 1 & -x_2 Y_2 & -y_2 Y_2 \\
0 & 0 & 0 & x_3 & y_3 & 1 & -x_3 Y_3 & -y_3 Y_3 \\
0 & 0 & 0 & x_4 & y_4 & 1 & -x_4 Y_4 & -y_4 Y_4 \\
\end{pmatrix} \cdot
\begin{pmatrix} h_{11} \\ h_{12} \\ h_{13} \\ h_{21} \\ h_{22} \\ h_{23} \\ h_{31} \\ h_{32} \end{pmatrix}
$$

This is nice because now common math machinery can be thrown at this problem. The matrix needs to be inverted, then only a matrix multiplication is left to solve for the homography entries:

$$
\begin{aligned}
\vec{k} &= M \vec{h} \\
M^{-1}\vec{k} &= \vec{h}
\end{aligned}
$$

Once this is done the elements of $$\vec{h}$$ and $$h_{33}$$ (or whatever element was fixed) can be arranged into a matrix again. Then the homography can be used to project points from one domain to another. Of course, the usual requirements for matrix inversion also apply here, i.e. $$M$$ needs to exhibit linear independence, for instance this is not given if two correspondence pairs are identical.

This kind of approach is called _Direct Linear Transform_ in literature.

To conclude, here is a simple python implementation:

{{< highlight Python >}}
from typing import Optional
import numpy as np

def dlt(src: np.ndarray, dst: np.ndarray) -> Optional[np.ndarray]:
    assert src.shape == (4, 2)
    assert dst.shape == (4, 2)

    m = np.zeros((8, 8))
    m[0:4, 0] = m[4:8, 3] = src[:, 0]
    m[0:4, 1] = m[4:8, 4] = src[:, 1]
    m[0:4, 2] = m[4:8, 5] = src[:, 2]
    m[0:4, 6] = - src[:, 0] * dst[:, 0]
    m[0:4, 7] = - src[:, 1] * dst[:, 0]
    m[4:8, 6] = - src[:, 0] * dst[:, 1]
    m[4:8, 7] = - src[:, 1] * dst[:, 1]

    try:
        m_inv = np.linalg.inv(m)
    except np.linalg.LinAlgError:
        return None

    k = np.concatenate((dst[:, 0], dst[:, 1]))
    h = np.dot(m_inv, k)
    return np.reshape(np.concatenate((h, [1])), (3, 3))
{{< / highlight >}}


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


