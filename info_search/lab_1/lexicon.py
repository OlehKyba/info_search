import json
import pickle
from typing import Iterable

from info_search.entities import Term
from info_search.lab_1.protos.lab_1_pb2 import Lexicon as ProtoLexicon
from info_search.lab_1.protos.lab_1_pb2 import TermFrequency


class Lexicon:
    def __init__(
        self,
        init_terms: Iterable[Term] = None,
    ):
        self._term_to_frequency = {}

        if init_terms:
            self.add_terms(init_terms)

    @classmethod
    def from_dict(cls, term_to_frequency: dict[str, int]):
        lexicon = cls()
        lexicon._term_to_frequency = term_to_frequency
        return lexicon

    def __iter__(self) -> Iterable[tuple[str, int]]:
        return iter(self._term_to_frequency.items())

    def __len__(self) -> int:
        return len(self._term_to_frequency)

    @property
    def total_terms_count(self) -> int:
        total_count = 0

        for _, term_frequency in self:
            total_count += term_frequency

        return total_count

    def add_term(self, term: Term):
        frequency = self._term_to_frequency.get(term.value, 0)
        self._term_to_frequency[term.value] = frequency + 1

    def add_terms(self, terms: Iterable[Term]) -> None:
        for term in terms:
            frequency = self._term_to_frequency.get(term.value, 0)
            self._term_to_frequency[term.value] = frequency + 1

    def get_term_frequency(self, term_value: str):
        return self._term_to_frequency.get(term_value, 0)

    # Pickle
    def to_pickle(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def from_pickle(data: bytes) -> "Lexicon":
        return pickle.loads(data)

    # JSON
    def to_json(self) -> str:
        return json.dumps(self._term_to_frequency)

    @classmethod
    def from_json(cls, data: str) -> "Lexicon":
        return cls.from_dict(json.loads(data))

    # Protobuf
    def to_proto(self) -> bytes:
        proto = ProtoLexicon(
            terms_frequency=[
                TermFrequency(
                    term=term,
                    frequency=frequency,
                )
                for term, frequency in self
            ]
        )
        return proto.SerializePartialToString()

    @classmethod
    def from_proto(cls, proto_bytes) -> "Lexicon":
        proto = ProtoLexicon.FromString(proto_bytes)

        return cls.from_dict(
            {
                term_frequency.term: term_frequency.frequency
                for term_frequency in proto.terms_frequency
            }
        )
