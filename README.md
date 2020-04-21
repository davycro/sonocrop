# SONOCROP [![PyPI](https://img.shields.io/pypi/pyversions/sonocrop.svg?style=plastic)](https://github.com/davycro/sonocrop)

Prepare bedside ultrasounds for machine learning and image interpretation. Sonocrop isolates the dynamic component of an ultrasound movie and strips away the rest.

## Installation

Requires python 3.7 or higher

Install with pip: ```pip3 install sonocrop --upgrade```


## Basic usage

Sonocrop runs from the command line:

Automatically crop away static borders
```shell
sonocrop crop inputscan.mp4 out.mp4 --thresh=0.1
```

Blackout static pixels
```shell
sonocrop mask inputscan.mp4 out.mp4
```



