---
title: How Denormal Floats Slow Down ML Inference
date: 2023-07-18
tags: ["software engineering", "math"]
markup: "mmark"
use_math: true
use_justify: true
---

Recently when converting a PyTorch checkpoint for CPU inference with ONNX throughput fell off a cliff. Of course, runtime on CPU is generally expected to be slower than on GPU, however something was off. Turns out a particular case of floating values was to blame.

<!--more-->


### What are Subnormals?

_Normal_ floating point numbers are [representated](https://en.wikipedia.org/wiki/IEEE_754-1985#Representation_of_numbers) in base 2 in scientific format "normalized" to `<sign> 1.<fraction> * 2^(<exponent> + bias)`. In memory it is stored as `[sign|exponent|fraction]`, e.g. for 32-bit floats the exponent is represented with 8 bits and the fraction with 23 bits (and the sign with 1 bit).

When the floating point number that is supposed to be encoded becomes so small that (with the available bits for fraction and exponent) it's no longer possible to reach a `1.` leading representation, the floating number is considered [subnormal, denormalized or denormal](https://en.wikipedia.org/wiki/Subnormal_number).


### Why is this an Issue?

Processing subnormals requires additional logic for basic handling and arithmetic operations. In the case of the x86 instruction set architecture this additional logic seems to be [usually not implemented in silicon and instead handled in software](https://stackoverflow.com/a/54938328) which leads to significant slowdowns. The same post also notes that Nvidia GPUs generally implement this in hardware which is consistent with my experience: No problems on Nvidia GPUs, but performance drop on a x86 CPU 💁


### How to Resolve it?

Fortunately, the remedy to this problem is a quick one: Setting the denormal floats to actual zeros. In PyTorch one achieves this by calling `torch.set_flush_denormal(True)` ([docs](https://pytorch.org/docs/stable/generated/torch.set_flush_denormal.html)) before creating/loading tensors that may contain denormal floats.

Generally, minor changes to model weights should have negligible impact on model outputs, however in case denormals of existing weights get zero'ed it's advisable to rerun tests and confirm there is no impact on model accuracy.


