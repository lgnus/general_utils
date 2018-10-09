__author__ = 'lgnus'

import begin
import feedparser
import requests
import re
import os
from tqdm import tqdm


@begin.start
@begin.convert(url=str, output=str, start=int, end=int)
def main(url, output='data', start=0, end=-1):
    """ Given an URL to an RSS feed, attempts to download all audio files
    from said feed into the specified folder. """
    feed = feedparser.parse()

    # if the folder doesn't exist, create it
    if not os.path.isdir(f'{os.getcwd()}\\{output}\\'):
        os.mkdir(f'{os.getcwd()}\\{output}\\')

    # if end is not provided, download all of them
    if end < 0:
        end = len(feed.entries)

    # Obtain each feed entry ordered by date
    reversed_entries = feed.entries[::-1]
    for n, entry in tqdm(enumerate(reversed_entries[start:end + 1]), total=end - start):

        # Skip iteration if not within bounds
        if not n + start >= start and n + start <= end + 1:
            continue

        # Clean up the title to be used as filename
        title = re.sub(r'\W+', ' ', entry.title).strip()

        try:
            with open(f'{os.getcwd()}\\{output}\\{n + start} - {title}.mp3', 'w+b') as file:

                # Get only audio links from the feed entry
                audio_url = [link.href for link in entry.links if link.type == 'audio/mpeg'][0]

                # Get the audio file and save it
                tqdm.write(f'  Downloading {entry.title}.mp3')
                r = requests.get(audio_url)
                file.write(r.content)

        except BaseException:  # Ignore errors and proceed to next file
            continue

    print('Finished!')