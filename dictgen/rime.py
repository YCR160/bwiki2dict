# https://github.com/outloudvi/mw2fcitx/blob/master/mw2fcitx/dictgen/rime.py

import re
from datetime import datetime
# from ..logger import console


def gen(text, **kwargs):
    name = kwargs.get("name") or "bwiki"
    version = kwargs.get("version") or datetime.now().strftime("%Y-%m-%d")
    text = re.sub(r"[ ][ ]*", "\t", text)
    text = text.replace("\t0", "")
    text = text.replace("'", " ")
    text = f'---\nname: {name}\nversion: "{version}"\nsort: by_weight\n...\n' + text
    with open(name + ".dict.yaml", "w", encoding="utf-8") as file:
        file.write(text)
    # console.info("Dictionary generated.")
    print("Dictionary generated.")
    return text
