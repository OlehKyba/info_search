from pymorphy3 import MorphAnalyzer

from info_search.lab_1.lexicon import Lexicon
from info_search.lab_1.nltk_utils import init_nltk
from info_search.lab_1.preprocessing import WordsNormalizer, WordsTokenizer
from info_search.lab_1.readers import EpubReader
from info_search.lab_2.inverted_index import InvertedIndexBuilder
from info_search.lab_3.two_words_index import parse_terms_for_2_words_index

init_nltk()

books = (
    # "../../books/451-za-farengeytom.epub",
    # "../../books/1984.epub",
    "../../books/atlant-rozpraviv-pliechi-1.epub",
    # "../../books/atlant-rozpraviv-pliechi-2.epub",
    # "../../books/atlant-rozpraviv-pliechi-3.epub",
    # "../../books/haksli-oldos-prekrasnyy-novyy-svit.epub",
    # "../../books/kulbabove-vino.epub",
    # "../../books/na-zakhidnomu-fronti-bez-zmin.epub",
    # "../../books/proshchavai-zbroie.epub",
    # "../../books/sapients-istoriya-lyudstva.epub",
)

reader = EpubReader(books)
tokenizer = WordsTokenizer(stop_words=[])
normalizer = WordsNormalizer(MorphAnalyzer(lang="uk"))
lexicon = Lexicon()
two_words_idx_builder = InvertedIndexBuilder()

for doc_name, term in parse_terms_for_2_words_index(reader, tokenizer, normalizer):
    doc_id, term_id = lexicon.add_term(doc_name, term)
    two_words_idx_builder.add_term(doc_id, term_id)

two_words_idx = two_words_idx_builder.build()

from info_search.lab_3.two_words_index import TwoWordsIndexQueryExecutor

executor = TwoWordsIndexQueryExecutor(two_words_idx, lexicon, tokenizer, normalizer)

doc_ids_1 = executor.search("Даґні Таґґарт")
doc_ids_2 = executor.search("міс Таґґарт")
doc_ids_3 = executor.search("Міс Таґґарт, цей світ тримається на самих лише м’язах")

# print(f"Документи, де є 'Даґні Таґґарт': {doc_ids_1}")
# print(f"Документи, де є 'міс Таґґарт': {doc_ids_2}")
print(
    f"Документи, де є 'Міс Таґґарт, цей світ тримається на самих лише м’язах': {doc_ids_3}"
)
