---
title: Just Put all Your Sh!t in Docker Images 🐋
date: 2022-02-06
tags: ["software engineering", "build processes"]
markup: "mmark"
use_math: false
use_justify: true
---

Docker is awesome. It is even more awesome if you embrace it. So why stop at using it for production images?

<!--more-->


Containerization is one of the puzzle piece in the big scheme of abstracting hardware. You have written your code on a unix machine, but need to run it on a Microsoft server farm? Don't worry, as long as you use agnostic protocols for interfacing with your code (usually HTTP), you are golden.

There are some obvious and some less obvious usecases for containers, to the experienced folks out there these might be all no-brainers, but I feel like some really carry home that perspective of containerization, so it seems worth sharing this list anyway. Also, this article is written in the context of Docker since I am familiar with it plus I wanted to put a 🐋 in the title, but the ideas apply to other [OCI](https://opencontainers.org/) systems as well.



### Production Images

> **Imagine** running some kind of web service before containers and virtual machines.

> **Imagine** scaling it to multiple nodes with a load balancer in front of it to manage the new users.

> **Imagine** having more than 1 person with `ssh` and `sudo` rights maintaining them.

> **Imagine** having duplicated and unversioned shell scripts on all machines.

> **Imagine** doing a release by compiling code directly on the production servers.

> **Imagine** after a release, stuff is broken on 1 machine, but works on the others.

> **Imagine** doing any kind of rollback.


![make it stop](https://www.meme-arsenal.com/memes/407c34ee2ace7621d4b816cea92e6078.jpg)


Ok, ok, ok, yes that sounds like a house of cards. Using Docker images to serve code in production is probably the easiest of the bunch (of usecases) and the reason why containers are so popular.

It moves the responsibility of defining the dependencies to the developer who knows about them naturally since the code supposedly was tested _on his/her machine_. The people running and maintaining the production servers only need to setup their system to run the Docker image, with `docker run`, `docker-compose`, in a Kubernetes setup or whatever they deem reasonable. They no longer need to know about certain dependencies of some software that they have not written themselves and can focus on the other aspects of delivering code.



### Development Setups

> **Imagine** your code requires services from other teams.

> **Imagine** the other teams do not provide Docker images.

> **Imagine** you need to work through their (hopefully existent and up-to-date) documentation to build and run everything on your system.

> **Imagine** needing to launch all these services everytime you do basic development and testing.


Ok, first of all it's the other teams' fault or the person that decided not to use Docker images. Go tell them to change this. Once that is done, write yourself a docker compose file which defines all images you need, how you need them run and check this into your git repo.


Docker Compose is your friend



### Testing

> **Imagine** running a test on your machine and everything passes.

> **Imagine** running the _same_ test on the _same_ code in a continuous integration pipeline and some test fail.


Local and CI machine will do the _same_ stuff


### Native Build Processes

> **Imagine** you need to install 3 software packages and compile 2 native libraries to even compile your own code

> **Imagine** all of this only works on a specific linux distro with some backported gcc

Don't write all that stuff in a documentation for everyone to struggle and ask you anyway, just write a freaking Dockerfile.

Turn your `cmake bla bla` into `docker run xyz bla bla`

note cross compilation

Packaging systems do emerge in C++, but wrapping your build with a Docker image is still worth the effort.


### Platform Independent Command Line Tools

> **Imagine** you have written an awesome script and it would help your co-workers as well

> **Imagine** you have the human decency to share it with them

> **Imagine** it requires them to install Python `X.Y` and 3 other dependencies

> **Imagine** having to _sell_ your script to your co-workers although it would ease their workflow


![slug life](https://i.chzbgr.com/full/9190240512/h3F011B10/snail-meme-slug-ididnt-choose-the-slug-life-the-slug-life-chose-me)


How about 1 dependency? That seems okay, they will get some benefit from it after going through the pain of installing that 1 dependency after all. What if I told you there was a way where it is likely that this 1 dependency is already installed. No, I do not mean using Go binaries, these require 0 dependencies (LINK?). But how about putting your script into a Docker container and setting the `ENTRYPOINT`?

If you wanna be fancy you can wrap it with a shell script in `/usr/local/bin`, so it feels less Docker


