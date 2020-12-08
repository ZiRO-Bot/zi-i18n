import os
import re


class Translate:
    def __init__(self, raw, translated):
        self.raw = raw
        self.translated = translated

    def __str__(self):
        return self.translated

    def __repr__(self):
        return f"<translated(raw='{self.raw}', translated='{self.translated}')>"


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

    def fetch_translations(self):
        lang = self.lang
        if self.lang + self.suffix not in self.languages:
            import warnings

            warnings.warn(f"Language '{self.lang}' Not Found")
            lang = "en_US"

        self.locale = {}
        with open(f"{self.dir}/{lang}{self.suffix}", "r") as read:
            if lang in self.locale:
                self.locale[lang] += read.readlines()
            else:
                self.locale[lang] = read.readlines()

        regex = r"^<(.)(\S*): \"(.*)\">"

        for i in self.locale:
            for x in self.locale[i]:
                try:
                    match = re.search(regex, x).groups()
                except AttributeError:
                    continue
                if match[1] not in self.translation:
                    if i not in self.translation:
                        self.translation[i] = {}
                    self.translation[i][match[1]] = {"type": match[0], "result": match[2]}

    def change_lang(self, language: str):
        self.lang = language
        self.fetch_translations()

    def translate(self, text: str):
        lang = self.lang
        if lang not in self.translation:
            return text

        if text not in list(self.translation[lang].keys()):
            lang = "en_US"
            
        try:
            t = self.translation[lang][text]
        except KeyError:
            return Translate(text, text)

        if t["type"] == "!":
            return Translate(text, t["result"])
        return Translate(text, text)


# locale = I18n("locale", "en_US")
# print(locale.translate("example.text"))
# locale.change_lang("id_ID")
# print(locale.translate("example.text"))
