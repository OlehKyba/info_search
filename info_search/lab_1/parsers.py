from typing import Iterable, Optional

from info_search.lab_1.preprocessing import WordsNormalizer, WordsTokenizer
from info_search.lab_1.readers import EpubReader


def parse_terms(
    reader: EpubReader,
    tokenizer: WordsTokenizer,
    normalizer: WordsNormalizer = None,
) -> Iterable[tuple[str, str, int]]:
    position = 0
    prev_doc_name: Optional[str] = None
    for doc_name, text in reader.read():
        if prev_doc_name is not None and prev_doc_name != doc_name:
            position = 0

        for word in tokenizer.tokenize(text):
            if normalizer:
                word = normalizer.normalize(word)

            yield doc_name, word, position

            position += 1

        prev_doc_name = doc_name
