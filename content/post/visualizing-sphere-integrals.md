---
title: Visualizing Sphere Integrals
date: 2014-11-18
tags: ["math"]
math: true
markup: "mmark"
---


You know that feeling when you have been using some rule blindly forever and one day you finally spend the time to figure out where this rule comes from? Below is my effort to visualize the integrals which lead to the formulas for surface area and volume of spheres.

<!--more-->

## 2D Prerequisites

### Circle Circumference


![Circle Area and Circumference](/images/visualizing-sphere-integrals/circle-area.png)

The circumference $$U$$ let's chop up the circle in $$n$$ triangles with $$\phi = \frac{2\pi}{n}$$. One of them is highlighted above. The length of side $$u$$ can be computed the following way:

$$
\begin{aligned}
u = r \cdot \tan(\phi)
\end{aligned}
$$

By considering this side $$n$$ times we approximate the circumference:

$$
\begin{aligned}
U = n \cdot u = n \cdot r \cdot \tan\left(\frac{2\pi}{n}\right)
\end{aligned}
$$


Now, with increasing $$n$$ our approximation becomes more precise. In the limit we can drop the tangent because of the [small angle approximation](https://en.wikipedia.org/wiki/Small-angle_approximation).

$$
\begin{aligned}
U = \lim_{n \to \infty} n \cdot r \cdot \tan\left(\frac{2\pi}{n}\right) = \lim_{n \to \infty} n \cdot r \cdot \frac{2\pi}{n} = 2\pi r
\end{aligned}
$$


### Circle Area


The approach to determine area $$A$$ is quite similar. This time the area of the $$n$$ triangles are considered, the area of a single triangle is defined as:

$$
\begin{aligned}
a &= \frac{1}{2} \cdot r \cdot u = \frac{1}{2} \cdot r^2 \cdot \tan(\phi)
\end{aligned}
$$

Analogously we can approximate the area and regard the limit:

$$
\begin{aligned}
A &= n \cdot a = n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) \\ \\
A &= \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \tan\left(\frac{2\pi}{n}\right) = \lim_{n \to \infty} n \cdot \frac{1}{2} \cdot r^2 \cdot \frac{2\pi}{n} = \pi r^2
\end{aligned}
$$

## Surface Area of a Sphere

![Sphere Surface](/images/visualizing-sphere-integrals/sphere-surface.png)

$$
\begin{aligned}
  b &= \frac{d\phi_b}{2\pi} \cdot 2\pi r = d\phi_b \cdot r \\ \\
  a &= \frac{d\phi_a}{2\pi} \cdot 2\pi r_a = d\phi_b \cdot r_a \\ \\
r_a &= r \cdot \cos\left(\phi_b\right) \\ \\
\\ \\
A = a \cdot b &= \int_0^{\frac{1}{2} \pi} \int_0^{\frac{1}{2} \pi} r^2 \cos\left(\phi_b\right) ~ d\phi_b ~ d\phi_a \\ \\
&= r^2 \cdot \int_0^{\frac{1}{2} \pi} \left[ \sin\left(\phi_b \right) \right] _0^{\frac{1}{2}\pi} ~ d\phi_a \\ \\
&= r^2 \cdot \int_0^{\frac{1}{2} \pi} \left(\sin\left(\frac{1}{2}\pi\right) - \sin(0) \right) ~ d\phi_a \\ \\
&= r^2 \cdot \int_0^{\frac{1}{2} \pi} ~ d\phi_a \\ \\
&= r^2 \cdot \frac{1}{2} \pi \\ \\
&\rightarrow 8 \cdot \frac{1}{2} \pi r^2 = 4 \pi r^2
\end{aligned}
$$



## Volume of a Sphere

![Sphere Volumne](/images/visualizing-sphere-integrals/sphere-volume.png)

$$
\begin{aligned}
r_u &= \sqrt{r^2 - u^2} \\ \\
\\ \\
V &= A(r_u) \cdot du = \pi {r_u}^2 \cdot du \\ \\
&= \int_0^r \pi (r^2 - u^2) ~ du \\ \\
&= \pi \left( r^2 \int_0^r du - \int_0^r u^2 ~du \right) \\ \\
&= \pi \left( r^2 \cdot r - \left[ \frac{1}{3} u^3 \right]_0^r \right) \\ \\
&= \pi \left( r^3 - \frac{1}{3} r^3 \right) \\ \\
&= \frac{2}{3} \pi r^3 \\ \\
&\rightarrow 2 \cdot \frac{2}{3} \pi r^3 = \frac{4}{3} \pi r^3 
\end{aligned}
$$


text5