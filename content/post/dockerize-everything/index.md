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

It moves the responsibility of defining the dependencies to the developer who knows about them naturally since the code supposedly was tested _on his/her machine_. The people running and maintaining the production servers only need to care about how they run the Docker images, with plain `docker run` / `docker-compose`, in a Kubernetes setup or whatever they deem reasonable. They no longer need to know about certain dependencies of some software that they have not written themselves and can focus on the other aspects of delivering code.



### Development Setups

> **Imagine** your code requires services from other teams.

> **Imagine** the other teams do not provide Docker images.

> **Imagine** you need to work through their (hopefully existent and up-to-date) documentation to build and run everything on your system.

> **Imagine** needing to launch all these services everytime you do basic development and testing.


Ok, first of all it's the other teams' fault or the person that decided not to use Docker images. Go tell them to change this. Also tell them to use some registry to share the Docker images with other teams. Once that is done, write yourself a docker compose file which defines all images you need, how you need them to be started and check this into your git repo. Before developing run `docker-compose up` to get your dependencies running. If you need them running all the time, you might as well add a [turn the restart policy to always](https://docs.docker.com/compose/compose-file/compose-file-v3/#restart), this way the services are started together with Docker itself (i.e. when your machine starts - yes, I shutdown my notebook everyday).



### Testing

> **Imagine** running a test on your machine and everything passes.

> **Imagine** running the _same_ test on the _same_ code in a continuous integration pipeline and some test fail.


Local and CI machine will do the _same_ stuff


### Native Build Processes

> **Imagine** you need to install 3 software packages and compile 2 native libraries to even compile your own code

> **Imagine** all of this only works on a specific linux distro with some backported gcc

Compiling native projects is never easy. There are packaging systems like [conan](https://github.com/conan-io/conan) becoming more commonly used, but in my experience it is still a pain.
Writing documentation about the build process is good, but making the build work _everywhere_ is even better. For this add two components:

* a docker image which defines the build environment
* a script which as single point of entry for the build process which does the following:
  * runs the Docker image
  * mounts (`-v`!) all project files into the image and adds volumes so build artifacts persist after the container is stopped
  * triggers the build

This will turn your `cmake bla bla` into `docker run -v $(pwd):/source my_build_image bla bla` and allows for consistent and reproducible builds.


### Platform Independent Command Line Tools

> **Imagine** you have written an awesome script and it would help your co-workers as well

> **Imagine** you want to share it with them

> **Imagine** it requires them to install Python `X.Y` and 3 other dependencies

> **Imagine** having to _sell_ your script to your co-workers although it would ease their workflow

How about 1 dependency? That seems okay, they will get some benefit from it after going through the pain of installing that 1 dependency after all. What if I told you a way where this dependency is likely to already be installed on your co-workers' systems. How about putting your script into a Docker container and setting the `ENTRYPOINT`?

{{< highlight Docker >}}
FROM python:3.10-buster
COPY script.py /script.py
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt # installing all dependencies
ENTRYPOINT ["python3", "/script.py"]
{{< / highlight >}}

The docker image can now be used like the script itself without worrying about the installation, `docker run my_script_dockerized argument --option`. If you want it to feel less Docker, you could add a simple script in `/usr/local/bin` which starts the image and [forwards](https://stackoverflow.com/a/1537695) all inputs to the container:

{{< highlight Bash >}}
#!/bin/bash
docker run my_script_dockerized $@
{{< / highlight >}}

There are some caveats here, though:

* File paths for both input and output need to be mounted in the image otherwise the script within the container will not find the input file and, respectively, store output inside the container which will be gone once it is stopped. One could mount the entire root directory with `-v /:/host` and develop have corresponding logic in the script, but tbh I am not sure about the security implications of this mount
* You might want to specify a host mode if the script is supposed to reach services which are running on the host machine

You see that this is admittedly not the best way of distributing a script. But it certainly has its benefits and skips a lot of hurdles when building full-fledged packages, e.g. for the [Python Package Index](https://pypi.org/) or even on an OS level (e.g. Debian). 

Another option might be to learn Go, rewrite your script and [cross-compile](https://golangcookbook.com/chapters/running/cross-compiling/) it into self-contained executables (one for each platform) :upside_down:

