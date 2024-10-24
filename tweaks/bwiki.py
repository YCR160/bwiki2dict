def tweak_strip(words):
    ret = set()
    for word in words:
        ret.add(word.strip())
    return ret


def tweak_remove_word(items):
    def not_in(word):
        for i in items:
            if word.find(i) != -1:
                return False
        return True

    def cb(words):
        ret = set()
        for word in words:
            if not_in(word):
                ret.add(word)
        return ret

    return cb


def tweak_split_word(spliters):

    def cb(words):
        for i in spliters:
            tmp = set()
            for word in words:
                for j in word.split(i):
                    tmp.add(j)
            words = tmp
        return words

    return cb


def tweak_len_gt(min_length):

    def cb(words):
        filtered_words = set()
        for word in words:
            if len(word) > min_length:
                filtered_words.add(word)
        return filtered_words

    return cb


def tweak_remove_chars(chars):

    def cb(words):
        for char in chars:
            tmp = set()
            for word in words:
                updated_word = word.replace(char, "")
                tmp.add(updated_word)
            words = tmp
        return words

    return cb


def tweak_remove_regex(regexes):
    import re

    compiled_patterns = [re.compile(pattern) for pattern in regexes]

    def cb(words):
        ret = words
        for pattern in compiled_patterns:
            ret = {item for item in ret if not pattern.match(item)}
        return ret

    return cb


tweaks = [
    tweak_strip,
    tweak_remove_word([]),  # 删除包含指定词的词条
    tweak_split_word(["&", "-", "(", ")", "：", "（", "）"]),
    tweak_len_gt(1),
    tweak_remove_chars(["，", "•", "！", "「", "」"]),  # 删除字符
    tweak_remove_regex(["^第.*(次|话)$"]),  # 删除指定正则匹配的词条
]

if __name__ == "__main__":
    filtered_titles = {
        "「我」的诞生",
        "「白日梦」酒店-梦境",
        "「白日梦」酒店-现实",
        "三月七•巡猎",
        "丹恒•饮月",
        "嘿，我在这儿",
        "开拓者•同谐",
        "开拓者•存护",
        "开拓者•毁灭",
        "忍事录•音律狩猎",
        "忍法帖•缭乱破魔",
        "我将，巡征追猎",
        "托帕&账账",
        "模拟宇宙：寰宇蝗灾",
        "模拟宇宙：黄金与机械",
        "汪！散步时间！",
        "点个关注吧！",
        "烦恼着，幸福着",
        "片刻，留在眼底",
        "琥珀（光锥）",
        "舞！舞！舞！",
        "这就是我啦！",
        "阮•梅",
    }

    for func in tweaks:
        filtered_titles = func(filtered_titles)

    print(filtered_titles)
