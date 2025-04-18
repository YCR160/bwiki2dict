import os
import ahocorasick
from convert import is_preferred_word
from need_to_remove import remove_words


def filter_freq(titles, filtered_titles, **kwargs):
    name = kwargs.get("name") or "bwiki"
    path = f"comment/{name}/"
    fb_path = "comment/bwiki/"

    # 构建 Aho-Corasick 自动机
    automaton = ahocorasick.Automaton()
    for title in titles:
        automaton.add_word(title, title)
    automaton.make_automaton()

    freq = dict.fromkeys(titles, 0)

    def process_files(dir_path):
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                with open(os.path.join(dir_path, file), "r", encoding="utf-8") as f:
                    for line in f:
                        matches = []
                        for end_index, title in automaton.iter(line):
                            matches.append((end_index, title))
                        
                        # 按结束索引和词长排序，确保超集优先
                        matches.sort(key=lambda x: (-x[0], -len(x[1])))

                        counted = set()
                        for _, title in matches:
                            # 检查超集是否已经匹配
                            is_subset = any(
                                title in other and title != other for other in counted
                            )
                            if not is_subset:
                                freq[title] += 1
                                counted.add(title)

    process_files(path)
    if all(value == 0 for value in freq.values()):
        process_files(fb_path)

    # 出现频率高于 0.1 倍平均值的，视为高频词
    sum = 0
    for filtered_title in filtered_titles:
        sum += freq[filtered_title]
    avg = sum / len(filtered_titles)
    base = avg * 0.1

    ret = set()
    for filtered_title in filtered_titles:
        ret.add(filtered_title)
    for title in titles:
        if (
            freq[title] > base
            and title not in remove_words
            and not is_preferred_word(title)
        ):
            ret.add(title)

    with open(name + ".freq.txt", "w", encoding="utf-8") as f:
        freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        for w, fq in freq:
            if w in ret:
                f.write(f"{w} {fq}\n")
        f.write("\n")
        for w, fq in freq:
            if w not in ret:
                f.write(f"{w} {fq}\n")

    return ret

if __name__ == "__main__":
    import time
    start = time.time()
    # titles 是所有词语，filtered_titles 是人物名（要保留的词语）
    with open("titles.txt", "r", encoding="utf-8") as f:
        titles = f.read().splitlines()
    with open("filtered_titles.txt", "r", encoding="utf-8") as f:
        filtered_titles = f.read().splitlines()
    filter_freq(titles, filtered_titles)
    print(time.time() - start)
