import json
import pickle
from typing import Iterable

from ordered_set import OrderedSet

from info_search.lab_1.protos.lab_1_pb2 import Lexicon as ProtoLexicon
from info_search.lab_1.protos.lab_1_pb2 import Term


class Lexicon:
    def __init__(
        self,
        terms: dict[str, list[int]] = None,
        docs: list[str] = None,
    ):
        self.terms: dict[str, list[int]] = terms if terms else {}
        self.docs: OrderedSet[str] = OrderedSet(docs)

    def _set_term(self, term: str) -> int:
        if row := self.terms.get(term):
            row[1] += 1
            return row[0]

        term_id = len(self.terms)
        self.terms[term] = [term_id, 1]
        return term_id

    def _set_doc(self, doc_name: str) -> int:
        return self.docs.add(doc_name)

    def add_term(self, doc_name: str, term: str) -> tuple[int, int]:
        doc_id = self._set_doc(doc_name)
        term_id = self._set_term(term)
        return doc_id, term_id

    def add_terms(self, terms: Iterable[tuple[str, str]]) -> None:
        for doc_name, term in terms:
            self.add_term(doc_name, term)

    def get_docs(self, doc_ids: Iterable[int]) -> list[str]:
        return [self.docs[doc_id] for doc_id in doc_ids]

    def get_term_id(self, term: str) -> int | None:
        if row := self.terms.get(term):
            return row[0]
        return None

    @classmethod
    def from_dict(cls, lexicon_dict: dict) -> "Lexicon":
        return cls(**lexicon_dict)

    @property
    def total_terms_count(self) -> int:
        total_count = 0

        for _, frequency in self.terms.values():
            total_count += frequency

        return total_count

    # Pickle
    def to_pickle(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def from_pickle(data: bytes) -> "Lexicon":
        return pickle.loads(data)

    # JSON
    def to_json(self) -> str:
        return json.dumps({"terms": self.terms, "docs": self.docs.items})

    @classmethod
    def from_json(cls, data: str) -> "Lexicon":
        return cls.from_dict(json.loads(data))

    # Protobuf
    def to_proto(self) -> bytes:
        proto = ProtoLexicon(
            terms=[
                Term(
                    name=term,
                    id=term_id,
                    frequency=frequency,
                )
                for term, (term_id, frequency) in self.terms.items()
            ],
            docs=self.docs.items,
        )
        return proto.SerializePartialToString()

    @classmethod
    def from_proto(cls, proto_bytes) -> "Lexicon":
        proto = ProtoLexicon.FromString(proto_bytes)
        return cls(
            terms={term.name: [term.id, term.frequency] for term in proto.terms},
            docs=list(proto.docs),
        )
