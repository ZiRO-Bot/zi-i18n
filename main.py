import os
import re

from fuzzywuzzy import fuzz, process

class Translation:
    def __init__(self, name, translate=None):
        self.name = name
        self.translate = translate or name

    def __str__(self):
        return self.translate

    def __repr__(self):
        return f"<!{self.name}: \"{self.translate}\">"


class I18n:
    def __init__(self, directory: str = "locale", language: str = "en_US"):
        self.dir = directory or "."
        self.languages = []
        self.suffix = ".zi.lang"
        files = os.listdir(self.dir)
        for f in files:
            if f.endswith(self.suffix):
                self.languages.append(f)
        self.translation = {}
        self.change_lang(language)

    def fetch_translations(self, text: str = None):
        if not text:
            return
        lang = self.lang
        if self.lang + self.suffix not in self.languages:
            import warnings

            warnings.warn(f"Language '{self.lang}' Not Found")
            lang = "en_US"

        fallback = open(f"{self.dir}/en_US{self.suffix}", "r")
        fallback = fallback.readlines()

        if lang == "en_US":
            read = fallback
        else:
            read = open(f"{self.dir}/{lang}{self.suffix}", "r")
            read = read.readlines() or fallback
        
        def fetch(query):
            try:
                regex = r"^<(.)(\S*): \"(.*)\">"
                match = re.search(regex, query).groups()
            except AttributeError:
                return

            if match and match[1] == text:
                return Translation(match[1], match[2])
        
        for i in read:
            res = fetch(i)
            if res:
                return res

        test = process.extractOne(text, fallback)
        return fetch(test[0]) or Translation(text)

    def change_lang(self, language: str):
        self.lang = language

    def translate(self, text: str):
        return self.fetch_translations(text)
        
# locale = I18n("locale", "en_US")
# print(locale.translate("example.text"))
# locale.change_lang("id_ID")
# print(locale.translate("example.text"))
# locale.change_lang("pl")
# print(locale.translate("example.test"))
