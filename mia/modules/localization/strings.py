import os
import yaml
import logging

from codecs import decode, encode

locale_codes = []

lang_strings = {}

for lang in os.listdir("locales"):
    if os.path.isdir(f"locales/{lang}"):
        locale_codes.append(lang)
        lang_strings[lang] = {}
        for lang_file in os.listdir(f"locales/{lang}"):
            lang_strings[lang].update(yaml.full_load(open(f"locales/{lang}/{lang_file}", "rb")))


logging.info("Loaded %d languages: %s", len(locale_codes), str(locale_codes))


def tl(chat_id, text):
    language = "en-US"
    if language and language in locale_codes and text in lang_strings[language]:
        result = decode(
            encode(
                lang_strings[language][text],
                'latin-1',
                'backslashreplace'
            ),
            "unicode-escape"
        )
    else:
        if text in lang_strings["en-US"]:
            result = decode(
                encode(
                    lang_strings["en-US"][text],
                    'latin-1',
                    'backslashreplace'
                ),
                "unicode-escape"
            )
        else:
            result = f"No string found for {text}.\nReport it in @KeralasBots."
            logging.warning(result)

    return result
