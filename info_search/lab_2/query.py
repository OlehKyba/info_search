from collections import deque

import numpy as np
from luqum.parser import parser
from luqum.tree import AndOperation, Not, OrOperation, Word
from luqum.visitor import TreeTransformer

from info_search.lab_1.lexicon import Lexicon
from info_search.lab_2.incidence_matrix import IncidenceMatrixIndex


class OperationVisitor(TreeTransformer):
    def visit_and_operation(self, node: AndOperation, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].and_()

    def visit_or_operation(self, node: OrOperation, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].or_()

    def visit_not(self, node: Not, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].not_()

    def visit_word(self, node: Word, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].term(node.value)


class QueryContext:
    def __init__(
        self,
        incidents_matrix_idx: IncidenceMatrixIndex,
        lexicon: Lexicon,
    ):
        self.incidents_matrix = incidents_matrix_idx
        self.lexicon = lexicon
        self.stack = deque()

    def term(self, term: str) -> None:
        term_id = self.lexicon.get_term_id(term)
        doc_vector = self.incidents_matrix.search_doc_ids(term_id)
        self.stack.append(doc_vector)

    def not_(self):
        docs_vector = self.stack.pop()
        self.stack.append(np.logical_not(docs_vector).astype(np.int8))

    def and_(self):
        left_docs_vector = self.stack.pop()
        right_docs_vector = self.stack.pop()

        self.stack.append(
            np.logical_and(left_docs_vector, right_docs_vector).astype(np.int8)
        )

    def or_(self):
        left_docs_vector = self.stack.pop()
        right_docs_vector = self.stack.pop()

        self.stack.append(
            np.logical_or(left_docs_vector, right_docs_vector).astype(np.int8)
        )

    @property
    def result(self) -> list[str]:
        docs_vector = self.stack.pop()
        assert len(self.stack) == 0
        return self.lexicon.get_docs(docs_vector)


class QueryExecutor:
    def __init__(
        self,
        lexicon: Lexicon,
        index: IncidenceMatrixIndex,
    ):
        self.lexicon = lexicon
        self.index = index

    def execute(self, query: str) -> list[str]:
        tree = parser.parse(query)
        context = QueryContext(self.index, self.lexicon)
        visitor = OperationVisitor()

        visitor.visit(tree, context={"query_context": context, "lexicon": self.lexicon})

        return context.result
