import re
import sys
import feedparser
from pathlib import Path
from tqdm import tqdm
import requests
import feedparser
import begin

__author__ = 'lgnus'


@begin.start
@begin.convert(url=str, output=str, start=int, end=int)
def main(url, output='data', start=0, end=-1):
    """ Given an URL to an RSS feed, attempts to download all audio files
    from said feed into the specified folder.

    Parameters
    ----------
        url : str
            URL path to the rss podcast
        output : str
            Path to download directory, creates folders if they don't exist
        start : int
            Start downloading from this number forward (defaults to 0)
        end : int
            Stop downloading at this point (defaults to -1 aka all)
    """

    feed = feedparser.parse(url)
    output_path = Path.cwd() / output

    # if the folder doesn't exist, create it
    if not output_path.is_dir():
        output_path.mkdir()

    # if end is not provided, download all of them
    if end < 0:
        end = len(feed.entries)

    # Obtain each feed entry ordered by date
    reversed_entries = feed.entries[::-1]
    failed = {}
    for n, entry in tqdm(enumerate(reversed_entries[start:end + 1]), total=end - start):

        # Skip iteration if not within bounds
        if not n + start >= start and n + start <= end + 1:
            continue

        # Clean up the title to be used as filename
        title = re.sub(r'\W+', ' ', entry.title).strip()

        try:
            with open(output_path / f'{n + start} - {title}.mp3', 'w+b') as file:

                # Get only audio links from the feed entry
                audio_url = [link.href for link in entry.links if link.type == 'audio/mpeg'][0]

                # Get the audio file and save it
                tqdm.write(f'  Downloading {entry.title}.mp3')
                r = requests.get(audio_url)
                file.write(r.content)
        except KeyboardInterrupt:  # cancel downloads
            print('Downloading canceled by user.')
            sys.exit()
        except:       # Ignore errors and proceed to next file
            failed[n] = entry.title
            continue

    # if it failed to donwload any, print them
    if len(failed > 0):
        print(f'{15*'='}\nFailed to download the following:\n')
        [print(f'{k} - {v}') for k, v in failed.items()]
        print(f'{15*'='}')

    print('Finished!')
