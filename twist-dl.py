import requests
import tqdm
import json
import decrypt
import os
import sys
from argparse import ArgumentParser

def download_file(url, path, headers=None):
    r = requests.get(url=url, stream=True, headers=headers)
    file_size = int(r.headers['Content-Length'])
    chunk_size = 1024
    num_bars = int(file_size / chunk_size)
    with open(path, 'wb') as fp:
        for chunk in \
                tqdm.tqdm(r.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc=path, leave=True):
            fp.write(chunk)
    return

def get_series_url_list(series_data):
    source_url_list = {title: {}}
    for entry in series_data:
        decrypted_source = decrypt.decrypt(entry['source'].encode('utf-8'), source_key).decode('utf-8').lstrip(' ')
        video_url = configuration["base_url"] + decrypted_source
        source_url_list[title][entry['number']] = video_url
    return source_url_list

def validate_episode_input(s):
    try:
        if 0 < int(s) < 100:
            return int(s)
        else:
            print 'Invalid input, exiting...'
            exit(1)
    except Exception:
        exit(1)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.realpath(__file__))
    usage = "python twist-dl.py title [--directory DIRECTORY] [-h]"
    parser = ArgumentParser(
        description="Twist-dl is a small python tool for downloading video contents of series available on the website "
                    "twist.moe locally! To download a particular series, find the title as defined in twist.moe's url string."
                    " i.e. 'https://twist.moe/a/made-in-abyss/' would need the argument passed as 'made-in-abyss'.",
        usage=usage
    )
    parser.add_argument('title')

    parser.add_argument("--directory", dest="directory",
                        help="Directory path to save downloaded contents",
                        required=False,
                        default=""
                        )

    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    options = parser.parse_args()
    title = options.title
    if not options.directory:
        if not os.path.isdir('{}/anime'.format(base_dir)):
            os.mkdir('{}/anime'.format(base_dir))
        directory = '{}/anime/{}/'.format(base_dir, title)
    else:
        directory = options.directory
        if not directory.endswith('/'):
            directory += '/'

    with open('{}/conf.json'.format(base_dir)) as f:
        configuration = json.loads(f.read())
    base_url = configuration['base_url']
    api_url = '{}/api/anime/{}/sources'.format(base_url, title)
    api_token = configuration['api_token']
    source_key = str(configuration['source_key'])

    # Get series data, which includes episode data and encrypted sourcefile paths
    headers = {'x-access-token': '{}'.format(api_token)}
    r = requests.get(api_url, headers=headers)
    if r.status_code == 404:
        print "Error, it looks like the title you entered is not found, " \
              "please ensure it is identical to the url path listed in twist.moe"
        exit(1)
    series_data = json.loads(r.content)
    print('Successfully gathered series information.')

    episode_range_begin = validate_episode_input(raw_input('Beginning Episode Range:'))
    episode_range_end = validate_episode_input(raw_input('Ending Episode Range:'))

    # Decrypt the source url and get a list of source URLs
    source_url_list = get_series_url_list(series_data)


    # Download files to user specified path
    headers = {
        'User-Agent': \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Referer': 'https://twist.moe/'
    }

    if not os.path.isdir(directory):
        os.mkdir(directory)

    print 'Downloading MP4s to Path: {}.'.format(directory)
    for episode in range(episode_range_begin, episode_range_end + 1):
        path = '{}{}-episode-{}.mp4'.format(directory, title, episode)
        url = source_url_list[title][episode]
        download_file(url=url, headers=headers, path=path)
