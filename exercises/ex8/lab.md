# Lab 0x28 : Mobile Security

Welcome to this lab! Today, we will explore mobile security by reverse-engineering several Android apps.

## Credit

This lab was adapted from prof. Fratantonio’s MOBISEC course from EURECOM. We thank him greatly for sharing some of his introductory material with us. If you like the challenges in the exercise session, go check it out [here](https://mobisec.reyammer.io/)! While we will help you find the solutions to the challenges during the lab session, we will not write it up as per the author's request. 

## Setup and installation

Before we jump straight to the topic, we will need some tools:

### java

You probably know what Java is. Any version of the [JRE](https://www.java.com/en/download/manual.jsp) from the past 10 years should work for this lab!

### jadx

[Jadx](https://github.com/skylot/jadx) is a powerful command-line and GUI tool which can produce Java source code from Android Dex and APK files. The latest version can be found [here](https://github.com/skylot/jadx/releases).

In a nutshell, `.dex` are very similar to Java `.class` files - they contain the information about the classes used by a Java Program (with the difference, [amongst others](https://www.boldare.com/blog/differences-between-class-and-dex-files-in-java-android/), that they use the DVM bytecode). `.apk` stands for Android Package and is the filetype used by Android to distribute and install applications. We will give a short explanation of its structure afterwards.  

### [optional] Android Studio

Android Studio is one of the main IDEs used for Android app development. It is developped by IntelliJ, so if you're familiar with any of their products (IntelliJ Idea, PyCharm, CLion, ...), you'll feel right at home.

Aprt from the usual coding features, Android Studio comes with an Android emulator, which enables emulating a wide range of android devices! Namely, this means that you will be able to test your solutions on the applications directly (neat!).

You can download it from [here](https://developer.android.com/studio). 
Note: The installer is 1.1Gb in size, so this might take some time.

## Decompiling and APKs introduction

We will provide several application for you to reverse engineer. Before we start describing what makes each challenge different, we will give a short introduction to what to look out for, as the baseline methodology will be similar for all exercises.

### Decompiling the APK

If you installed jadx with its GUI, you can open the file from the gui itself, or from the terminal using `jadx-gui <.apk file>`. Otherwise, decompile it using `jadx <.apk file>` and open the output folder with the editor of your choice.

### An introduction to APKs

As you saw in the lecture, an APK is not much more than an archive containing various types of files an android app might need. When analyzing an APK, `jadx` will create two folders:

* `sources`: This directory contains the decompiled Java, and this is where you’ll want
to spend most of your time in.
* `resources`: Everything else that composes an apk. In particular, it’s divided in the
following:

  * `AndroidManifest.xml`: This is the main configuration file for an Android app. It contains information about the app’s package name, version, permissions, and
other settings.

  * `classes.dex`: This is the compiled code of the app written in Java. It contains the bytecode that can be executed by the Android runtime.

  * `res/`: This directory contains the app’s resources organized into subdirectories based on their type (e.g. drawable, layout, values).
    
  * `assets/`: This directory contains any additional files that the app needs, such as external libraries or custom fonts.
    
  * `META-INF/`: This directory contains metadata about the APK file, such as its signature and other information.
  * `lib/`: This directory contains any native libraries that the app uses, such as libraries written in C or C++.

Particular interest should also be given to the directory `resources/res/values`: It contains files that define various values used by the app. These files are typically written in XML format and can be accessed by the app’s code.

Some common files that you may find in there are:
* `strings.xml`: This file contains the app’s strings, such as the app’s name, labels, and messages.
* `colors.xml`: This file defines the app’s color values, and can be used to set the app’s color scheme.
* `dimens.xml`: This file defines the app’s dimension values, such as the size of text or margins.
* `styles.xml`: This file defines the app’s styles, which are sets of values that can be applied to views in the app’s layout.
* `attrs.xml`: This file defines the app’s custom attributes, which are values that can be used in the app’s layout files.
* `public.xml`: This file contains entries that define the names and IDs of the app’s public resources.

## Challenges

All the apps included in this homework will ask the user for a flag or a PIN. Your job is to analyze the code of the app to understand what’s the correct input the app expects.

However, the developer of those apps wanted to keep the correct input a secret, so the verification if your input is correct is not a simple string comparison. Try to reverse engineer the code and understand what it is doing!

### babyrev

This is your starting challenge. Look for a function called `checkFlag`. You need to understand which string satisfies all checks to get the correct flag.

### pincode
This challenge is slightly more involved, as it requires a bit more than just reverse engineering. Look for a function called `checkPin`. This time you need to provide a 6-digit PIN code. The check is a bit weird though, right?

### gnirtz (bonus)
Here you have a `checkFlag` like in the first challenge. This time getting the flag will be considerably harder. Some light obfuscation is present. Only for
motivated students.

## HINTS, TIPS AND TRICKS
* You may want to give a closer look at the above mentioned public.xml and strings.xml.

* Educated guesses are a key skill for reversing. It is very often not required to understand every small detail of how a certain piece of code works. Do not follow the rabbit too deep into the hole!
* Make sure you take notes of the things you are confident you understood.
* You do not need to understand how `md5` works to solve `pinhole`.
* Are 6-digit PINs really safe?
* If you can’t make your solution for `pincode` to work, you can always craft another apk or copy and modify the Java code somewhere. Make the check simpler and verify that
your solution works.