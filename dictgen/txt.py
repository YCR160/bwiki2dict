def gen(text, **kwargs):
    name = kwargs.get("name") or "bwiki"
    lines = text.split("\n")
    text = [line.split("\t")[0] for line in lines]
    text = "\n".join(text)
    with open(name + ".dict.txt", "w", encoding="utf-8") as file:
        file.write(text)
    print("Dictionary generated.")
    return text
