import numpy as np

from info_search.lab_2.abc import Index, IndexBuilder, QueryContext, QueryExecutor


class IncidenceMatrixIndex(Index):
    def __init__(self, matrix: np.ndarray):
        self._matrix = matrix

    def search(self, term_id: int | None) -> np.ndarray[int]:
        if not term_id:
            return np.zeros(shape=self._matrix.shape[1], dtype=np.int8)

        return self._matrix[term_id]


class IncidenceMatrixBuilder(IndexBuilder):
    def __init__(self):
        self.unique_term_ids: set[int] = set()
        self.unique_doc_ids: set[int] = set()
        self.doc_ids_to_term_ids: list[tuple[int, int]] = []

    def add_term(self, doc_id: int, term_id: int) -> None:
        self.unique_term_ids.add(term_id)
        self.unique_doc_ids.add(doc_id)
        self.doc_ids_to_term_ids.append((doc_id, term_id))

    def build(self) -> IncidenceMatrixIndex:
        term_ids = sorted(self.unique_term_ids)
        doc_ids = sorted(self.unique_doc_ids)

        incidence_matrix = np.zeros(
            shape=(len(term_ids), len(doc_ids)),
            dtype=np.int8,
        )

        for doc_id, term_id in self.doc_ids_to_term_ids:
            incidence_matrix[term_id][doc_id] = 1

        incidence_matrix = incidence_matrix.astype(dtype=np.int8)
        return IncidenceMatrixIndex(incidence_matrix)


class IncidenceMatrixQueryContext(QueryContext):
    def term(self, term: str) -> None:
        term_id = self.lexicon.get_term_id(term)
        doc_vector = self.index.search(term_id)
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
        doc_ids = np.nonzero(docs_vector)[0]
        return self.lexicon.get_docs(doc_ids)


class IncidenceMatrixQueryExecutor(QueryExecutor):
    QUERY_CONTEXT_CLASS = IncidenceMatrixQueryContext
