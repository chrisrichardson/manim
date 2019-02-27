try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

if sys.version_info < (3, 7):
    print("Python 3.7 or higher required, please upgrade.")
    sys.exit(1)

version = "1.0"

setup(name="manim",
      description="Maths Anmiation",
      version=version,
      author="3Blue1Brown",
      author_email="",
      license="MIT",
      zip_safe=False,
      package_data={'manimlib': ['files/*', 'files/*/*']},
      include_package_data=True,
      packages=["manimlib", "manimlib.camera", "manimlib.scene",
                "manimlib.mobject", "manimlib.mobject.types","manimlib.mobject.svg",
                "manimlib.for_3b1b_videos", "manimlib.once_useful_constructs",
                "manimlib.utils", "manimlib.animation"],
      install_requires=["argparse==1.4.0",
                        "colour==0.1.5",
                        "numpy==1.15.0",
                        "Pillow==5.2.0",
                        "progressbar==2.5",
                        "scipy==1.1.0",
                        "tqdm==4.24.0",
                        "opencv-python==3.4.2.17",
                        "pycairo==1.17.1",
                        "pydub==0.23.0"])
