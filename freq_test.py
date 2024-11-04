with open('sr.dict.txt', 'r', encoding='utf-8') as f:
    sr_dict = f.read().splitlines()

with open('comment/sr.comment.txt', 'r', encoding='utf-8') as f:
    sr_comment = f.read().splitlines()

# 统计sr_dict每一个词在sr_comment中出现的次数
sr_freq = {}
for word in sr_dict:
    sr_freq[word] = 0
    for comment in sr_comment:
        sr_freq[word] += comment.count(word)

sr_freq = sorted(sr_freq.items(), key=lambda x: x[1], reverse=True)

with open('sr.freq.txt', 'w', encoding='utf-8') as f:
    for word, freq in sr_freq:
        f.write(f'{word} {freq}\n')
