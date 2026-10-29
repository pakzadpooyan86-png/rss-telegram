import requests
import html
import logging

logger = logging.getLogger(__name__)

TRANSLATION_URL = "https://api.mymemory.translated.net/get"
translation_cache = {}


def translate_to_persian(text):
    if not text or not text.strip():
        return text

    if text in translation_cache:
        return translation_cache[text]

    try:
        response = requests.get(
            TRANSLATION_URL,
            params={
                "q": text[:4500],
                "langpair": "en|fa"
            },
            timeout=20
        )

        data = response.json()

        if data.get("responseStatus") == 200:
            translated = data.get("responseData", {}).get("translatedText")

            if translated:
                translated = html.unescape(translated)
                translation_cache[text] = translated
                return translated

    except Exception as error:
        logger.warning("Translation failed: %s", error)

    return text
