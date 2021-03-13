---
title: Quick and Dirty Gradle Task for Android Projects Using Swig
date: 2021-03-21
tags: ["code", "build"]
markup: "mmark"
use_math: true
use_justify: true
---

Swig is really great to wrap native projects. I have been working on wrapping native code in an Android app, figuring out how to run swig as part of the gradle build pipeline took me way too many google queries. Below is the code I added to the respective `build.gradle`. Certainly not my proudest work and not a pro level gradle implementation for sure, but it gets the job done.
Swig should be installed, for Windows you might need to update the `commandLine` block and there is no autodetect for an outdated build, so clean the project if you modify your swig or native code :shower:


{{< highlight Java >}}
def cppDir = "${project.projectDir}/src/main/cpp"
ext.swigFile = "${cppDir}/mylib.i"
ext.swigOutputSourceFile = "${cppDir}/mylib.cpp"
ext.swigOutputJavaPackage = 'com.my.lib'
ext.swigOutputJavaPackageDir = "${project.projectDir}/src/main/java/" + swigOutputJavaPackage.replace(".", "/")

task swig {
    doLast {
        println "Removing ${swigOutputSourceFile}"
        delete swigOutputSourceFile
        println "Removing ${swigOutputJavaPackageDir}/*"
        delete fileTree(swigOutputJavaPackageDir) {
            include '*'
        }
        def cmd = "swig -v -java -c++ -package ${swigOutputJavaPackage} -outdir ${swigOutputJavaPackageDir} -o ${swigOutputSourceFile} ${swigFile}"
        println "Running \"${cmd}\""
        exec {
            commandLine 'sh', '-c', "mkdir -p ${swigOutputJavaPackageDir} && ${cmd}"
        }
    }
}
tasks.whenTaskAdded { task ->
    if (task.name.tokenize(":").last() in ['externalNativeBuildCleanDebug', 'externalNativeBuildCleanRelease']) {
        task.dependsOn swig
    }
}
{{< / highlight >}}


