# Twist.Moe Downloader Helper

### Description

![](examples/tty.gif)
This is a small python tool for downloading video contents of series available on the website `twist.moe` locally. 
To download a particular series, find the title as defined in twist.moe's url string. 
i.e. `https://twist.moe/a/made-in-abyss/` would need the argument passed as `made-in-abyss`.

Remember to support twist.moe with donations if you can, as they do a great job of operating their site!

### Installation
The associated scripts run in python version 2.7 and has not been tested in python 3. Simply install the 
`requirements.txt` to complete installation. I encourage you to use a virtualenv here if you can.

```bash
$ git clone https://github.com/JFryy/twist-moe-downloader.git
$ cd twist-moe-downloader
$ sudo pip install -r requirements.txt
```

And you're done! You can started with something as simple as the command below.

`$ python twist-dl.py fate`

### Running the script

```bash
$ python twist-dl.py

usage: python twist-dl.py [title] [--range RANGE][--directory DIRECTORY] [-h]

Twist-dl is a small python tool for downloading video contents of series
available on the website twist.moe locally! To download a list of particular
series, enter a keyword of the series name. i.e. 'code geass' can be found by
simply entering 'code'.

positional arguments:
  title

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY
                        Directory path to save downloaded contents
  --range RANGE         Range of episodes to download. i.e. --range=1-24

```

### Example Usage:

##### Download And Search
Download by passing the series title as found from search. Not specifying a range with `--range` will download the entire contents of the series.
```bash
$ python twist-dl.py code
? Anime found. Please choose a series to download:  code-geass-hangyaku-no-lelouch-r2
Successfully gathered series information.
Episode selection between 1-25. To select range input range i.e. '1-5'. Press 'Enter' to download all contents.
Input:
Downloading MP4s to Path: anime/code/ with episode range of 1-25.
anime/code/code-geass-hangyaku-no-lelouch-r2-episode-1.mp4: 489619KB [00:48, 10191.13KB/s]
...

```
##### Disclaimer
Downloading copyright videos may be illegal in your country. This tool is for educational purposes only.
