from fetch import fetch_all_titles
from filter import filter_titles
from tweaks.bwiki import tweaks
from convert import export
from dictgen import *

from config import configs

for game, data in configs.items():
    api_url = data["api_url"]
    part_categories = data["part_categories"]

    all_data = fetch_all_titles(api_url)
    filtered_titles = filter_titles(all_data, part_categories)
    for func in tweaks:
        filtered_titles = func(filtered_titles)
    pinyin_titles = export(filtered_titles)

    txt(pinyin_titles, name=game)
