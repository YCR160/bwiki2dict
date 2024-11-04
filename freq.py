import os
from need_to_remove import common_words, remove_words

def filter_freq(titles, filtered_titles, **kwargs):
    name = kwargs.get("name") or "bwiki"
    path = f'comment/{name}/'

    comment = ''
    if os.path.exists(path):
        for file in os.listdir(path):
            with open(path + file, 'r', encoding='utf-8') as f:
                comment += f.read()

    freq = {}
    for title in titles:
        freq[title] = comment.count(title)

    # 出现频率高于 0.1 倍平均值的，视为高频词
    sum = 0
    for filtered_title in filtered_titles:
        sum += freq[filtered_title]
    avg = sum / len(filtered_titles)
    base = avg * 0.1

    ret = set()
    remove = set(common_words + remove_words)
    for filtered_title in filtered_titles:
        ret.add(filtered_title)
    for title in titles:
        if freq[title] > base and title not in remove:
            ret.add(title)

    with open(name + '.freq.txt', 'w', encoding='utf-8') as f:
        freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        for w, fq in freq:
            if w in ret:
                f.write(f'{w} {fq}\n')
        f.write('\n')
        for w, fq in freq:
            if w not in ret:
                f.write(f'{w} {fq}\n')

    return ret
