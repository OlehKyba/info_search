from typing import Iterable

from info_search.lab_1.preprocessing import WordsNormalizer, WordsTokenizer
from info_search.lab_1.readers import EpubReader


def parse_terms(
    reader: EpubReader,
    tokenizer: WordsTokenizer,
    normalizer: WordsNormalizer = None,
) -> Iterable[tuple[str, str]]:
    for doc_id, text in reader.read():
        for word in tokenizer.tokenize(text):
            if normalizer:
                word = normalizer.normalize(word)
            yield doc_id, word