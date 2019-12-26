---
title: Using ODEs for Animation Interpolation (Rebuilding Facebook Rebound)
date: 2015-01-03
tags: ["math", "runge-kutta", "ordinary differential equation", "matlab"]
math: true
markup: "mmark"
---


[Rebound](http://facebook.github.io/rebound/) is an open-source project by Facebook. It is used to control the course of animations. In case you are familiar with Android, you might know that Android provides several `Interpolator` classes (`AccelerateInterpolator`, `DecelerateInterpolator`, ...) to handle that task. While most of these provide a rather simple course of animation, Facebook's Rebound is based on _spring dynamics_ which is not trivial to implement. This article describes my attempt to reverse engineer the Rebound library. Of course, it is open source, but I did not take a look at it, you gotta believe me there :grimacing:.

My version of Rebound can be found [here](https://github.com/osanj/spring-interpolator).



## Interpolators in UIs


The task of an animation is to visually transition a graphic object from a start state to an end state. Usually these states differ in the values of an attribute, e.g. scale a button from 50% to 100% to get the user's attention. The transition happens over time from its inital value to its final value. Interpolators encode the mathematical relation which is used to carry out that transition [1]. A linear relation is the most basic one, but there exist more sophisticated interpolators, too.


![Comparison of Interpolators](/data/ode-interpolation/interpolators-comparison.gif)

???

At this point you may think animation and interpolator are interchangable terms, but that is not correct. In programming terms an animation is a controller object which embeds/uses an interpolator object. Input ([i time]) and output ([i scale]) of an interpolator need to be normalized to be adapted to every situation. That means input and output are values between 0 and 1 (sometimes also <0 and/or >1, see the graphs above). To illustrate that, consider following pseudo java code:

[code pseudo animation]

???



## A Mechanical Concept

I started with the characteristic curve of the Rebound interpolator (see animation above). You can reproduce it by clicking the demo on the [website](http://facebook.github.io/rebound/") of Rebound. A different way to experience it, is to maximize/minimize a Chat Head of Facebooks Messenger.

As a starting point I tried to find a mechanical concept which could show a similiar motion. I came up with following configuration:

![Mechanical Concept with Forces](/data/ode-interpolation/mech-concept-labelled.png)

As you can see it's a mass attached to two fixed boards (they won't oscillate). The connections are done with a spring and a damper. To get the system oscillating an external stimulation is necessary. That "input" is realized by instantaneously lowering the the bottom board (Pos B) which causes an imbalance which the system tries to counteract. The motion of the mass (x) then should be the desired curve.

![Mechanical Concept Animation](/data/ode-interpolation/mech-concept-animation.gif)

In the context of an interpolator for animations moving the board from one position to the other is triggered when the animation should start playing, for example the user clicking a button.



## Concept Validation

Simulink ...



## Implementing Runge-Kutta

...


## Mapping Simulation-Time To Real-Time

...


## Implementing A Looper

...







## References

1. Google Inc. [Android API Guides](http://developer.android.com/guide/topics/resources/animation-resource.html#Interpolators)
2. Braack, Malte (2011). [Numerik für Differentialgleichungen](/data/ode-interpolation/lecture_notes_uni_kiel_ode.pdf) (german, lecture notes, RK4-Definition on pdf-page 30)
3. Ziessow, Dieter & Gross, Richard. [Umwandlung in ein System erster Ordnung](http://www.chemgapedia.de/vsengine/vlu/vsc/de/ma/1/mc/ma_13/ma_13_02/ma_13_02_11.vlu/Page/vsc/de/ma/1/mc/ma_13/ma_13_02/ma_13_02_31.vscml.html) (german)
