---
title: Build Numbers are the Better Release Candidates
date: 2024-04-07
tags: ["software engineering"]
markup: "mmark"
use_math: false
use_justify: true
---

Releasing a new version of a web application or larger software project usually involves some sort of build-deploy-test-fix cycle until it passes QA. A common approach is to have release candidates, however this implies re-building the last RC with the final tag which can be avoided with build numbers.

<!--more-->


## The Typical Release Candidate Flow

Let's say our next release version is `1.3.0`, as we go along new features/fixes/etc. were developed and make it into the codebase. Depending on the process, we may create a release candidate tag after every merge or only once we reach the "release preparation stage". Either way the first build will be `1.3.0-RC.1`, it should be deployed and tested by the QA suite. After more features and fixes, it may be `1.3.0-RC.4` that passes all tests :green_circle: and is ready to move to production.

Now, to get a clean final build, the same commit from which `1.3.0-RC.4` was built, needs to be tagged and built once again with `1.3.0`. This seems like a minuscule step, but technically it invalidates the tests that have been performed before since the build pipeline could lead to another artifact, e.g. if dependency versions are not properly pinned.

One may say "ok, then let's only use RCs", but then why do "normal" version strings not have "RC"? It doesn't seem consistent. Other things to consider are:
* having proper tags in the repository boosts developer experience and allows for straightforward comparison of versions
* if the build should be aware of its own tag (e.g. an app having an endpoint serving its own version) it needs to be added as part of the build pipeline (and previous builds will have RC tags)


## Extend SemVer to Skip the Final Rebuild

Sofar we sticked to [SemVer](https://semver.org/). By adding another number we can get rid of the retagging and rebuilding implied by the release candidate naming scheme: `MAJOR.MINOR.PATCH.BUILD` where `BUILD` is the build number for certain version. In our example from before the RCs would become `1.3.0.1` ... `1.3.0.4`. With that formality the "ok, then let's only use RCs" mindset becomes consistent with the versioning scheme - we can just move on with the last build and deploy it on prod.

A word of caution: for software libraries it should be checked if this scheme is compatible with the eco system (for Python this is the case). Alternatively, if consistency with SemVer is required `MAJOR.MINOR.PATCH-BUILD` may be used (see [specification point 10 on build metadata](https://semver.org/#spec-item-10)). However, also note that the spec says:

> Build metadata MUST be ignored when determining version precedence.

And finally, removing non-prod tags is still recommended for a clean git repo :wink:

