import numpy as np


class IncidenceMatrixIndex:
    def __init__(self, matrix: np.ndarray):
        self._matrix = matrix

    def search_doc_ids(self, term_id: int | None) -> np.ndarray[int]:
        if not term_id:
            return np.zeros(shape=self._matrix.shape[1], dtype=np.int8)

        return self._matrix[term_id]


class IncidenceMatrixBuilder:
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
