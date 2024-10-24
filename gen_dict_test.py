from fetch import fetch_all_titles
from filter import filter_titles
from tweaks.bwiki import tweaks
from convert import export
from dictgen import *

api_url = "https://wiki.biligame.com/sr/api.php"

all_data = fetch_all_titles(api_url)

part_categories = {
    "分类:角色",  # ["三月七", "三月七•巡猎", ...]
    "分类:光锥",  # ["「我」的诞生", "一场术后对话", ...]
    "分类:地区",  # ["「白日梦」酒店-梦境", "「白日梦」酒店-现实", ...]
    "分类:扩展装置",  # ["模拟宇宙：寰宇蝗灾", "模拟宇宙：黄金与机械"]
    "分类:稀有货币",  # ["古老梦华", "星琼"]
    "分类:跃迁道具",  # ["星轨专票", "星轨通票"]
    "分类:消耗品（道具）",  # ["燃料", "自塑尘脂", "遗器残骸"]
}

filtered_titles = filter_titles(all_data, part_categories)

for func in tweaks:
    filtered_titles = func(filtered_titles)

pinyin_titles = export(filtered_titles)

rime(pinyin_titles, name="sr")
