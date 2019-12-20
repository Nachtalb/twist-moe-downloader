from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='twistdl',
      version='1.01',
      description='CLI Tool/Client Library for twist.moe',
      url='https://github.com/JFryy/twist-moe-downloader',
      author='JFryy',
      author_email='fotherby1@gmail.com',
      license='BSD',
      packages=find_packages(),
      install_requires=[
            'requests',
            'pycryptodomex==3.9.4',
            'PyInquirer==1.0.3',
            'tqdm==4.40.2',
            'six==1.13.0',
            'pathlib2==2.3.5',
      ],
      include_package_data=True,
      zip_safe=False,
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            "Programming Language :: Python :: 2",
            "Operating System :: OS Independent",
      ],
      scripts=['cli/twistdl']
      )
