# SONOCROP [![PyPI](https://img.shields.io/pypi/pyversions/sonocrop.svg?style=plastic)](https://github.com/davycro/sonocrop)

Prepare bedside ultrasounds for machine learning and image interpretation. Sonocrop isolates the dynamic component of an ultrasound movie and strips away the rest.

![Example video](https://davycro.s3.amazonaws.com/sonocrop-readme-sidebyside.gif)

## Installation

Requires python 3.7 or higher

Install with pip: ```pip3 install sonocrop --upgrade```


## Basic usage

Sonocrop runs from the command line:

#### crop

Automatically crop away static borders
```shell
$ sonocrop crop inputscan.mp4 out.mp4 --thresh=0.1
```

#### mask

Blackout static pixels
```shell
$ sonocrop mask inputscan.mp4 out.mp4
```

#### edges

Extracts the edges around an ultrasound

Returns the distance in pixels in the form:
left,right,top,bottom

```shell
$ sonocrop edges inputscan.mp4
$ > 100,500,10,700
```

#### summary

Command | Input | Output
------- | ----- | ------
crop | ![Input](https://davycro.s3.amazonaws.com/sonocrop-readme-in.png) | ![Out](https://davycro.s3.amazonaws.com/sonocrop-readme-cropped.png)
mask | ![Input](https://davycro.s3.amazonaws.com/sonocrop-readme-in.png) | ![Out](https://davycro.s3.amazonaws.com/sonocrop-readme-mask.png)
edges | ![Input](https://davycro.s3.amazonaws.com/sonocrop-readme-in.png) | 237,717,72,518
