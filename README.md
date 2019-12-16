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

and you're done!!
`$ python twist-dl.py shingeki-no-kyojin`

### Running the script

```bash
$ python twist-dl.py 
Twist-dl is a small python tool for downloading video contents of series
available on the website twist.moe locally! To download a particular series,
find the title as defined in twist.moe's url string. i.e. 'https://twist.moe/a
/made-in-abyss/' would need the argument passed as 'made-in-abyss'.

positional arguments:
  title

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY
                        Directory path to save downloaded contents

```

Example Usage:
```bash
$ python twist-dl.py shingeki-no-kyojin
Successfully gathered series information.
Beginning Episode Range:1
Ending Episode Range:2
Downloading MP4s to Path: /Users/jfotherby/Desktop/projects/twist.moe-dl/anime/shingeki-no-kyojin/.
/Users/jfotherby/Desktop/projects/twist.moe-dl/anime/shingeki-no-kyojin/shingeki-no-kyojin-episode-1.mp4:   7%|▋         | 45351/662939 [00:04<00:49, 12597.16KB/s]
```
