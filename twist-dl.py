import requests
import tqdm
import json
import decrypt
import os
import sys
from PyInquirer import prompt
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


def basic_search(query, response):
    search_results = []
    for title in response:
        name = title['slug']['slug']
        if query.lower() in name.lower():
            title['slug']['title'] = name
            del title['slug']['slug']
            del title['slug']['anime_id']
            search_results.append(title['slug'])
    return search_results


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.realpath(__file__))
    usage = "python twist-dl.py [title] [--range RANGE][--directory DIRECTORY] [-h]"
    parser = ArgumentParser(
        description="Twist-dl is a small python tool for downloading video contents of series available on the website "
                    "twist.moe locally! To download a list of particular series, enter a keyword of the series name. i.e. 'code "
                    "geass' can be found by simply entering 'code'.",
        usage=usage
    )
    parser.add_argument('title')


    parser.add_argument("--directory", dest="directory",
                        help="Directory path to save downloaded contents",
                        required=False,
                        default=""
                        )

    parser.add_argument("--range", dest="range",
                        help="Range of episodes to download. i.e. --range=1-24",
                        required=False,
                        default=""
                        )

    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    # Parse arg vars.
    options = parser.parse_args()
    title = options.title
    episode_range = options.range

    # Configuration variables.
    with open('{}/conf.json'.format(base_dir)) as f:
        configuration = json.loads(f.read())
    base_url = configuration['base_url']
    api_token = configuration['api_token']
    source_key = str(configuration['source_key'])

    # Directory Path Handling.
    if not options.directory:
        if not os.path.isdir('anime'):
            os.mkdir('anime')
        directory = 'anime/{}/'.format(title)
    else:
        directory = options.directory
        if not directory.endswith('/'):
            directory += '/'
    if not os.path.isdir(directory):
        os.makedirs(directory)

    # Search for Anime:
    headers = {'x-access-token': '{}'.format(api_token)}
    r = requests.get(base_url + '/api/anime', headers=headers)
    r = json.loads(r.content)
    found_anime = [result['title'] for result in basic_search(query=title, response=r)]
    if not found_anime:
        print "Error: It looks like the title you entered is not found, please ensure it is a substring " \
              "of the url path listed in twist.moe."
        exit(1)

    # Prompt for found Anime in Search:
    questions = [
        {
            'type': 'list',
            'name': 'title',
            'message': 'Anime found. Please choose a series to download:',
            'choices': found_anime
        }
    ]
    answers = prompt(questions)
    title = str(answers['title'])

    # Get series data, which includes episode data and encrypted sourcefile paths.
    url = '{}/api/anime/{}/sources'.format(base_url, title)
    r = requests.get(url, headers=headers)
    series_data = json.loads(r.content)
    print('Successfully gathered series information.')
    if not episode_range:
        episode_range = raw_input("Episode selection between {}-{}. To select range input range i.e. '1-5'. "
                                  "Press 'Enter' to download all contents. \nInput: ".format('1', str(len(series_data))))

    # Download entire range if range not specified.
    if episode_range:
        episode_begin = validate_episode_input(episode_range.split('-')[0])
        episode_end = validate_episode_input(episode_range.split('-')[1])
    else:
        episode_begin = 1
        episode_end = len(series_data)

    # Decrypt the source url and get a list of source URLs.
    source_url_list = get_series_url_list(series_data)
    print 'Downloading MP4s to Path: {} with episode range of {}-{}.'.format(directory, episode_begin, episode_end)
    headers = {
        'User-Agent': \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Referer': base_url
    }
    for episode in range(episode_begin, episode_end + 1):
        path = '{}{}-episode-{}.mp4'.format(directory, title, episode)
        url = source_url_list[title][episode]
        download_file(url=url, headers=headers, path=path)
    print('Downloads completed!')
