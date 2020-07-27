import fire


def dir(input_directory, output_directory):
  """Crop away static pixels from all video files in a directory

  Examples

  sonocrop dir input-dataset output-dataset


  Args:
      input_directory: Directory of video files
      output_directory: Directory of output, must be empty
  """

  import os
  import rich
  from pathlib import Path
  if not os.path.exists(output_directory):
    os.makedirs(output_directory)

  paths = Path(input_directory).glob('**/*.mp4')
  for path in paths:
    output_file = Path(output_directory)/path.name
    crop(path, output_file)



def crop(input_file, output_file, thresh=0.1):
  """Crop away static pixels from an ultrasound

  This function isolates the moving video in the center of an ultrasound clip and
  removes static borders that often contains patient information.

  Examples

  sonocrop crop in.mp4 out.mp4 --thresh=0.05


  Args:
      input_file: Path to input video (must be mp4, mov, or avi)
      output_file: File path for video output
      thresh (float, optional): Defaults to 0.1
  """

  import numpy as np
  import cv2
  from pathlib import Path
  from sonocrop import vid

  import rich
  from rich.progress import Progress

  v, fps, f, height, width = vid.loadvideo(input_file)

  rich.print(f'Auto cropping: [underline]{input_file}[/underline]')
  rich.print(f'  Frames: {f}')
  rich.print(f'  FPS: {fps}')
  rich.print(f'  Width x height: {width} x {height}')
  rich.print(f'  Thresh: {thresh}')

  # Count unique pixels
  with Progress() as progress:
    task = progress.add_task("[green] Finding static video pixels...", total=height)
    u = np.zeros((height, width), np.uint8)
    for i in range(height):
        u[i] = np.apply_along_axis(vid.countUniquePixels, 0, v[:,i,:])
        progress.update(task, advance=1)

  u_avg = u/f

  rich.print(' Finding edges')

  maxW = np.max(u_avg, axis=0)
  left,right = vid.findEdges(maxW, thresh=thresh)
  maxH = np.max(u_avg, axis=1)
  top,bottom = vid.findEdges(maxH, thresh=thresh)

  rich.print(f'  Top: {top}')
  rich.print(f'  Bottom: {bottom}')
  rich.print(f'  Left: {left}')
  rich.print(f'  Right: {right}')

  cropped = v[:,top:bottom,left:right]

  rich.print(f' Saving to file: "{output_file}"')
  vid.savevideo(output_file, cropped, fps)

  rich.print(' DONE')


def edges(input_file, thresh=0.1):
  """Extracts the edges around an ultrasound

  Returns the distance in pixels in the form:
  left,right,top,bottom

  Args:
      input_file: Path to input video (must be mp4, mov, or avi)
      thresh (float, optional): Defaults to 0.1
  """

  import numpy as np
  import cv2
  from pathlib import Path
  from sonocrop import vid
  v, fps, f, height, width = vid.loadvideo(input_file)

  u = vid.countUniquePixelsAlongFrames(v)
  u_avg = u/f

  maxW = np.max(u_avg, axis=0)
  left,right = vid.findEdges(maxW, thresh=thresh)
  maxH = np.max(u_avg, axis=1)
  top,bottom = vid.findEdges(maxH, thresh=thresh)

  return (f'{left},{right},{top},{bottom}')


def mask(input_file, output_file, thresh=0.05):
  """Blackout static pixels in an ultrasound

  Examples

  sonocrop mask in.mp4 out.mp4 --thresh=0.05

  Args:
      input_file: Path to input video (must be mp4, mov, or avi)
      output_file: File path for video output
      thresh (float, optional): Defaults to 0.05
  """

  import numpy as np
  import cv2
  from pathlib import Path
  from sonocrop import vid

  import rich
  from rich.progress import Progress

  v, fps, f, height, width = vid.loadvideo(input_file)

  rich.print(f'Mask video: [underline]{input_file}[/underline]')
  rich.print(f'  Frames: {f}')
  rich.print(f'  FPS: {fps}')
  rich.print(f'  Width x height: {width} x {height}')
  rich.print(f'  Thresh: {thresh}')

  # Count unique pixels
  with Progress() as progress:
    task = progress.add_task("[green] Finding static video pixels...", total=height)
    u = np.zeros((height, width), np.uint8)
    for i in range(height):
        u[i] = np.apply_along_axis(vid.countUniquePixels, 0, v[:,i,:])
        progress.update(task, advance=1)

  u_avg = u/f
  mask = u_avg > thresh
  y = vid.applyMask(v, mask)
  rich.print(f' Saving to file: "{output_file}"')
  vid.savevideo(output_file, y, fps)
  return ('Done')


def main():
  fire.Fire()

if __name__ == '__main__':
  main()
