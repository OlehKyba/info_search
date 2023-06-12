from string import punctuation
from typing import Iterable

import nltk
from pymorphy3 import MorphAnalyzer


class WordsTokenizer:
    """
    We must do nltk.download('punkt') before usage!
    """

    _EXTRA_PUNCTUATION = ["—", "«", "»", "–", "...", "''", "``", "„", "”", "©", "“"]

    def __init__(
        self,
        stop_words: list[str],
    ):
        self._stop_words = frozenset(
            stop_words + list(punctuation) + self._EXTRA_PUNCTUATION
        )

    @staticmethod
    def _fix_extra_punctuation(text: str) -> str:
        return (
            text.replace("’", "'")
            .replace("’", "'")
            .replace("…", ".")
            .replace(".—", ". —")
        )

    def tokenize(self, text: str) -> Iterable[str]:
        text = self._fix_extra_punctuation(text)

        for sentence in nltk.sent_tokenize(text):
            for word in nltk.word_tokenize(sentence):
                word = word.lower()

                if word.endswith(".") or word.startswith("."):
                    word = word.replace(".", "")

                if word and word not in self._stop_words:
                    yield word


class WordsNormalizer:
    def __init__(self, morph_analyzer: MorphAnalyzer):
        self._morph_analyzer = morph_analyzer

    def normalize(self, word: str) -> str:
        return self._morph_analyzer.parse(word)[0].normal_form
