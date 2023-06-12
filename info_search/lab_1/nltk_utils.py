import os

import nltk
import requests

_UA_STOP_WORDS_URL = "https://raw.githubusercontent.com/skupriienko/Ukrainian-Stopwords/master/stopwords_ua.txt"


def init_nltk() -> None:
    # need this for info_search.lab_1.preprocessing.WordsTokenizer
    nltk.download("punkt")
    load_nltk_ua_stop_words()


def load_nltk_ua_stop_words() -> None:
    resp = requests.get(_UA_STOP_WORDS_URL)
    dir_path = f"{nltk.data.path[1]}/corpora/stopwords"
    stopwords_path = f"{dir_path}/ukrainian"

    # if os.path.exists(stopwords_path):
    #     return

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(stopwords_path, "wb") as f:
        f.write(resp.content)
