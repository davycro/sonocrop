from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = {}
with open(path.join(here, "sonocrop", "__version__.py")) as f:
    exec(f.read(), version)

setup(

  name='sonocrop',

  version=version["__version__"],

  description='Prepare ultrasound videos for machine learning-- crop and remove static clutter from ultrasound video.',

  long_description=long_description,

  long_description_content_type='text/markdown',

  url='https://github.com/davycro/sonocrop',

  author='David Crockett, MD',

  author_email='davycro1@gmail.com',

  license = "Apache Software License 2.0",


  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Healthcare Industry',
    'Topic :: Multimedia :: Video',
    'Topic :: Scientific/Engineering :: Medical Science Apps.',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],

  keywords='ultrasound bedside ultrasound pocus ffmpeg opencv echo cardiac',

  packages=find_packages(),

  python_requires='>=3.6',

  install_requires=[
    'numpy',
    'opencv-python',
    'fire',
    'rich',
  ],

  entry_points={  # Optional
      'console_scripts': [
          'sonocrop=sonocrop.cli:main',
      ],
  },

)
