from zi_i18n import I18n
from time import time

i18n = I18n()
print(i18n.translate("func_example.test").format(time(), test="is a unix timestamp"))
i18n.change_lang("id_ID")
print(i18n.translate("example.func_id").format(timestamp=time()))
