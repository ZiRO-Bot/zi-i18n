import os
import re
import time
import random

# en_US.zi.lang (<lang>.zi.lang)
# ------------------------------
# "<!example.test: 'This is a test'>" -> example.test = "This is a test"
# "<!example.test2: 'This also a test'>" -> example.test2 = "This also a test"
#
# Dictionary
# ----------
# ! -> Translation
# example.test -> Name
# 'This is a test' -> Translated Text

class MyTimer():
    def __init__(self):
        self.start = time.time()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = 'The function took {time} seconds to complete'
        print(msg.format(time=runtime))

class Translate:
    def __init__(self, raw, translated):
        self.raw = raw
        self.translated = translated

    def __str__(self):
        return self.translated

    def __repr__(self):
        return f"<translated(raw='{self.raw}', translated='{self.translated}')>"

def get_trans(directory: str = "locale"):
    files = os.listdir(directory)
    locale = []
    for f in files:
        if f.endswith(".zi.lang"):
            with open(f"{directory}/{f}", "r") as read:
                locale = read.readlines()
    return locale

locale = get_trans()

translation = {}
regex = r"<(.)(\S*): '(.*)'>"

for i in locale:
    try:
        match = re.search(regex, i).groups()
    except AttributeError:
        continue
    if match[1] not in translation:
        translation[match[1]] = {"type": match[0], "result": match[2]}

def fetch_func(func: str):
    func = func.replace("{time}", str(time.time()))
    return func

def translate(text: str):
    if text not in translation:
        return text
    raw = text
    t = translation[text]
    if t["type"] == "!":
        text = t["result"]
    elif t["type"] == "?":
        text = fetch_func(t["result"])
    return Translate(raw, text)

untranslate = "example.func"
_ = translate
print(untranslate)
with MyTimer():
    translated = _(untranslate)
print(repr(translated))
