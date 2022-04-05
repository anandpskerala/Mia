import os
import yaml
import logging

from codecs import decode, encode

from pyrogram.types import InlineKeyboardButton

from mia.database.langs import get_lang_code

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
    language = get_lang_code(str(chat_id))
    if language and language in locale_codes and lang_strings[language].get(text) is not None:
        result = decode(
            encode(
                lang_strings[language][text],
                'latin-1',
                'backslashreplace'
            ),
            "unicode-escape"
        )
    else:
        if lang_strings["en-US"].get(text) is not None:
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


def gen_langs_kb():
    keyboards = [InlineKeyboardButton(
            f'{lang_strings[x]["language_flag"]} {lang_strings[x]["language_name"]}',
            callback_data=f"setlang_{x}") for x in locale_codes]
    
    kb = list(zip(keyboards[::2], keyboards[1::2]))

    if len(keyboards) %2 == 1:
        kb.append((keyboards[-1],))

    return kb
