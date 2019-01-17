## General Utils
General utilities and scrips I developed for personal use. 

### rss_podcast_downloader.py : 
Given an URL to an RSS feed, attempts to download all audio files from said feed.

Sample usage: `python rss_podcast_downloader.py "http://dataskeptic.com/feed.rss"`

### pdf_merge.py:
Given a path to a folder containing several pdfs, attempts to merge them in order to a single pdf.

Sample usage: `python pdf_merge.py '/book_chapters/' 'book_name' --filename 'best_book'`

### audio_convert.py:
Given a path to a file or folder with audio files, attempts to scale the dBFS volume to a defined range and optionally to a particular file extension.

Sample usage: `python audio_convert.py '/my_music/' -30`