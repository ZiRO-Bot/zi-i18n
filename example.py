import os
import re
import time
import random

from main import I18n

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

with MyTimer():
    i18n = I18n()
    i18n.translate("example.test").translated.format(time.time())
    i18n.change_lang("id_ID")
    i18n.translate("example.text")
