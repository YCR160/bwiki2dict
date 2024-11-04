from fetch import fetch_all_titles
from filter import all_titles, filter_titles
from tweaks.bwiki import tweaks
from freq import filter_freq
from convert import export
from dictgen import *

from config import configs

for game, data in configs.items():
    api_url = data["api_url"]
    part_categories = data["part_categories"]

    all_data = fetch_all_titles(api_url)
    titles = all_titles(all_data)
    filtered_titles = filter_titles(all_data, part_categories)
    for func in tweaks:
        titles = func(titles)
        filtered_titles = func(filtered_titles)
    words = filter_freq(titles, filtered_titles, name=game)
    pinyin_titles = export(words)

    txt(pinyin_titles, name=game)
