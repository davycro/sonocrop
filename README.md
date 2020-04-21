# SONOCROP

Computer vision tool to prepare bedside ultrasounds for machine learning and image interpretation. Sonocrop isolates the dynamic component of an ultrasound movie and strips away the rest.


# Usage

Sonocrop runs from the command line:

Automatically crop away static borders
```shell
sonocrop crop inputscan.mp4 out.mp4 --thresh=0.1
```

Blackout static pixels
```shell
sonocrop mask inputscan.mp4 out.mp4
```

# Installation

## Requirements
Requires python 3.7 or higher

```pip3 install sonocrop --upgrade```
