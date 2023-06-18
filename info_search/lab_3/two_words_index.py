from itertools import pairwise
from typing import Iterable

from info_search.lab_1.lexicon import Lexicon
from info_search.lab_1.preprocessing import WordsNormalizer, WordsTokenizer
from info_search.lab_1.readers import EpubReader
from info_search.lab_2.inverted_index import InvertedIndex

_TWO_WORDS_TERM_SEPARATOR = " "


def join_2_words_term(terms: tuple[str, str]) -> str:
    return _TWO_WORDS_TERM_SEPARATOR.join(terms)


def split_2_words_term(two_words_term: str) -> tuple[str, str]:
    first_word, second_word = two_words_term.split(_TWO_WORDS_TERM_SEPARATOR)
    return first_word, second_word


def _extract_2_words_terms(
    text: str,
    tokenizer: WordsTokenizer,
    normalizer: WordsNormalizer = None,
) -> Iterable[str]:
    terms: list[str] = []

    for word in tokenizer.tokenize(text):
        if normalizer:
            word = normalizer.normalize(word)
        terms.append(word)

    for first_word, second_word in pairwise(terms):
        yield join_2_words_term((first_word, second_word))


def parse_terms_for_2_words_index(
    reader: EpubReader,
    tokenizer: WordsTokenizer,
    normalizer: WordsNormalizer = None,
) -> Iterable[tuple[str, str]]:
    for doc_name, text in reader.read():
        for term in _extract_2_words_terms(text, tokenizer, normalizer):
            yield doc_name, term


class TwoWordsIndexQueryExecutor:
    def __init__(
        self,
        two_words_index: InvertedIndex,
        lexicon: Lexicon,
        tokenizer: WordsTokenizer,
        normalizer: WordsNormalizer = None,
    ):
        self._two_words_index = two_words_index
        self._lexicon = lexicon
        self._tokenizer = tokenizer
        self._normalizer = normalizer

    @staticmethod
    def _merge_doc_ids(left_doc_ids: list[int], right_doc_ids: list[int]) -> list[int]:
        i = 0
        j = 0
        common_doc_ids = []

        while i < len(left_doc_ids) and j < len(right_doc_ids):
            if left_doc_ids[i] < right_doc_ids[j]:
                i += 1
            elif left_doc_ids[i] > right_doc_ids[j]:
                j += 1
            else:
                common_doc_ids.append(left_doc_ids[i])
                i += 1
                j += 1

        return common_doc_ids

    def search(self, query: str) -> list[str]:
        common_doc_ids = list(range(len(self._lexicon.docs)))

        for term in _extract_2_words_terms(query, self._tokenizer, self._normalizer):
            term_id = self._lexicon.get_term_id(term)
            if not term_id:
                return []

            doc_ids = self._two_words_index.search(term_id)
            common_doc_ids = self._merge_doc_ids(common_doc_ids, doc_ids)

        return self._lexicon.get_docs(common_doc_ids)
