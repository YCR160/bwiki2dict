# https://github.com/outloudvi/mw2fcitx/blob/master/mw2fcitx/dictgen/pinyin.py

import tempfile
import subprocess

# from ..const import LIBIME_BIN_NAME, LIBIME_REPOLOGY_URL
# from ..logger import console
LIBIME_BIN_NAME = "libime_pinyindict"
LIBIME_REPOLOGY_URL = "https://repology.org/project/libime"


def gen(text, **kwargs):
    file = tempfile.NamedTemporaryFile("w+")
    file.write(text)
    # console.info(f"Running {LIBIME_BIN_NAME}...")
    print(f"Running {LIBIME_BIN_NAME}...")
    try:
        subprocess.run([LIBIME_BIN_NAME, file.name, kwargs["output"]],
                       check=True)
    except FileNotFoundError:
        # console.error(
        #     f"The program \"{LIBIME_BIN_NAME}\" is not found. Please install libime: {LIBIME_REPOLOGY_URL}"
        # )
        print(
            f"The program \"{LIBIME_BIN_NAME}\" is not found. Please install libime: {LIBIME_REPOLOGY_URL}"
        )
        raise
    # console.info("Dictionary generated.")
    print("Dictionary generated.")
