from zi_i18n import I18n

i18n = I18n("locale", "en_US")
print(i18n.latency*1000, "ms")
print(i18n.translate("example.test_id"))
print(i18n.translate("example.plural", count=0))
i18n.change_lang("id_ID")
print(i18n.translate("example.test_id"))
