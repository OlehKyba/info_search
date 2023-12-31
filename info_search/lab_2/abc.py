import abc
from collections import deque
from typing import Any, Type

from luqum.parser import parser

from info_search.lab_1.lexicon import Lexicon
from info_search.lab_1.preprocessing import WordsNormalizer
from info_search.lab_2.query import OperationVisitor


class Index(abc.ABC):
    @abc.abstractmethod
    def search(self, term_id: int) -> list[int]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def data_struct(self) -> Any:
        raise NotImplementedError


class IndexBuilder(abc.ABC):
    @abc.abstractmethod
    def add_term(self, doc_id: int, term_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def build(self) -> Index:
        raise NotImplementedError


class QueryContext(abc.ABC):
    def __init__(self, index: Index, lexicon: Lexicon):
        self.index = index
        self.lexicon = lexicon
        self.stack = deque()

    @abc.abstractmethod
    def term(self, term: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def not_(self):
        raise NotImplementedError

    @abc.abstractmethod
    def and_(self):
        raise NotImplementedError

    @abc.abstractmethod
    def or_(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def result(self) -> list[str]:
        raise NotImplementedError


class QueryExecutor:
    QUERY_CONTEXT_CLASS: Type[QueryContext]

    def __init__(
        self,
        lexicon: Lexicon,
        index: Index,
        normalizer: WordsNormalizer = None,
    ):
        self.lexicon = lexicon
        self.index = index
        self.normalizer = normalizer
        self.stack = deque()

    def execute(self, query: str) -> list[str]:
        tree = parser.parse(query)
        context = self.QUERY_CONTEXT_CLASS(self.index, self.lexicon)
        visitor = OperationVisitor()

        visitor.visit(
            tree,
            context={
                "query_context": context,
                "lexicon": self.lexicon,
                "normalizer": self.normalizer,
            },
        )

        return context.result
