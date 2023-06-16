import os
import time

from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer

from info_search.lab_1.lexicon import Lexicon
from info_search.lab_1.nltk_utils import init_nltk
from info_search.lab_1.parsers import parse_terms
from info_search.lab_1.preprocessing import WordsNormalizer, WordsTokenizer
from info_search.lab_1.readers import EpubReader
from info_search.lab_2.incidence_matrix import IncidenceMatrixBuilder, IncidenceMatrixQueryExecutor

init_nltk()
stopwords.words("ukrainian")


def transformation_run(lexicon: Lexicon) -> None:
    print(
        f"Lexicon before operations: "
        f"unique_terms_count={len(lexicon.terms)}. "
        f"total_terms_count={lexicon.total_terms_count}"
    )

    start_time = time.time()

    with open("../data/lexicon.pkl", "wb") as file:
        file.write(lexicon.to_pickle())

    with open("../data/lexicon.pkl", "rb") as file:
        lexicon_from_pickle = Lexicon.from_pickle(file.read())

    print(
        f"Lexicon after pickle: "
        f"unique_terms_count={len(lexicon_from_pickle.terms)}. "
        f"total_terms_count={lexicon_from_pickle.total_terms_count}, "
        f"time={time.time() - start_time}, "
        f"file_size={os.path.getsize('../data/lexicon.pkl')}"
    )

    start_time = time.time()

    with open("../data/lexicon.json", "w") as file:
        file.write(lexicon.to_json())

    with open("../data/lexicon.json", "r") as file:
        lexicon_from_json = Lexicon.from_json(file.read())

    print(
        f"Lexicon after JSON: "
        f"unique_terms_count={len(lexicon_from_json.terms)}. "
        f"total_terms_count={lexicon_from_json.total_terms_count}, "
        f"time={time.time() - start_time}, "
        f"file_size={os.path.getsize('../data/lexicon.json')}"
    )

    start_time = time.time()

    with open("../data/lexicon.protobuf", "wb") as file:
        file.write(lexicon.to_proto())

    with open("../data/lexicon.protobuf", "rb") as file:
        lexicon_from_proto = Lexicon.from_proto(file.read())

    print(
        f"Lexicon after Protobuff: "
        f"unique_terms_count={len(lexicon_from_proto.terms)}. "
        f"total_terms_count={lexicon_from_proto.total_terms_count}, "
        f"time={time.time() - start_time}, "
        f"file_size={os.path.getsize('../data/lexicon.protobuf')}"
    )


paths = (
    # "../books/451-za-farengeytom.epub",
    "../books/1984.epub",
    "../books/atlant-rozpraviv-pliechi-1.epub",
    # "../books/atlant-rozpraviv-pliechi-2.epub",
    # "../books/atlant-rozpraviv-pliechi-3.epub",
    # "../books/haksli-oldos-prekrasnyy-novyy-svit.epub",
    # "../books/kulbabove-vino.epub",
    # "../books/na-zakhidnomu-fronti-bez-zmin.epub",
    # "../books/proshchavai-zbroie.epub",
    # "../books/sapients-istoriya-lyudstva.epub",
)

reader = EpubReader(paths)
tokenizer = WordsTokenizer(stopwords.words("ukrainian"))
normalizer = WordsNormalizer(MorphAnalyzer(lang="uk"))
lexicon = Lexicon()
builder = IncidenceMatrixBuilder()

start_time = time.time()

for doc_name, term in parse_terms(reader, tokenizer, normalizer):
    doc_id, term_id = lexicon.add_term(doc_name, term)
    builder.add_term(doc_id, term_id)

print(len(lexicon.terms), lexicon.total_terms_count)


transformation_run(lexicon)

matrix_index = builder.build()

print(time.time() - start_time)


query_exec = IncidenceMatrixQueryExecutor(lexicon, matrix_index)
docs = query_exec.execute("міністерство OR (таґґарт AND NOT джеймс)")

print(docs)
