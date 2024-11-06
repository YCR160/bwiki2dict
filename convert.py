# https://github.com/outloudvi/mw2fcitx/blob/master/mw2fcitx/exporters/opencc.py

import json
import requests
from pypinyin import lazy_pinyin

DEFAULT_PLACEHOLDER = "_ERROR_"
session = requests.Session()


def hanzi_to_pinyin(word):
    pinyins = lazy_pinyin(word)
    return "".join(pinyins)


def pinyin_to_hanzi(pinyin):
    url = "https://inputtools.google.com/request"
    params = {
        "text": pinyin,
        "ime": "zh-t-i0-pinyin",
        "oe": "utf-8",
        "num": 3,
        "app": "bwiki2dict",
    }
    response = session.post(url, data=params)
    if response.status_code == 200:
        return response.json()[1][0][1]
    else:
        return None


def is_preferred_word(word):
    pinyin = hanzi_to_pinyin(word)
    preferred_words = pinyin_to_hanzi(pinyin)
    if preferred_words:
        return word in preferred_words  # 判断输入的词是否为候选词
    return False


def manual_fix(text, table):
    if text in table:
        return table[text]
    return None


def export(words, **kwargs):
    result = ""
    fixfile = kwargs.get("fixfile")
    if fixfile is not None:
        table = json.load(open(fixfile, "r", encoding="utf-8"))
    count = 0
    words = sorted(words)
    for word in words:
        # line = line.rstrip("\n")
        pinyins = lazy_pinyin(word, errors=lambda x: DEFAULT_PLACEHOLDER)
        # print(pinyins)
        if DEFAULT_PLACEHOLDER in pinyins:
            # 存在无法转换的字符
            print("Failed to convert, ignoring:", word)
            continue
        pinyin = "'".join(pinyins)
        # if pinyin == word:
        #     print("Failed to convert, ignoring:", pinyin)
        #     continue

        if fixfile is not None:
            fixed_pinyin = manual_fix(word, table)
            if fixed_pinyin is not None:
                pinyin = fixed_pinyin
                print(f"Fixing {word} to {pinyin}")

        result += "\t".join((word, pinyin, "0"))
        result += "\n"
        count += 1

    print(str(count) + " converted")
    return result


if __name__ == "__main__":
    filtered_titles = {
        "我将巡征追猎",
        "梦境",
        "这就是我啦",
        "黄金与机械",
        "寰宇蝗灾",
        "忍法帖缭乱破魔",
        "我的诞生",
        "烦恼着幸福着",
        "汪散步时间",
        "现实",
        "开拓者同谐",
        "账账",
        "片刻留在眼底",
        "舞舞舞",
        "开拓者存护",
        "光锥",
        "忍事录音律狩猎",
        "白日梦酒店",
        "模拟宇宙",
        "开拓者毁灭",
        "托帕",
        "阮梅",
        "点个关注吧",
        "丹恒饮月",
        "琥珀",
        "嘿我在这儿",
        "三月七巡猎",
    }
    pinyin_titles = export(filtered_titles)
    print(pinyin_titles)
