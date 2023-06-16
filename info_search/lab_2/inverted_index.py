import bisect

from info_search.lab_2.abc import Index, IndexBuilder, QueryContext, QueryExecutor


class InvertedIndex(Index):
    def __init__(self):
        self.inverted_index: dict[int, list[int]] = {}

    def add_term(self, doc_id: int, term_id: int) -> None:
        doc_ids = self.inverted_index.setdefault(term_id, [])

        index = bisect.bisect_left(doc_ids, doc_id)
        if index == len(doc_ids) or doc_ids[index] != doc_id:
            doc_ids.insert(index, doc_id)

    def search(self, term_id: int) -> list[int]:
        return self.inverted_index[term_id]


class InvertedIndexBuilder(IndexBuilder):
    def __init__(self):
        self._inverted_index = InvertedIndex()

    def add_term(self, doc_id: int, term_id: int) -> None:
        self._inverted_index.add_term(doc_id, term_id)

    def build(self) -> Index:
        return self._inverted_index


class InvertedIndexQueryContext(QueryContext):
    def term(self, term: str) -> None:
        term_id = self.lexicon.get_term_id(term)
        doc_ids = self.index.search(term_id)
        self.stack.append(doc_ids)

    def not_(self):
        doc_ids = self.stack.pop()
        all_doc_ids = list(range(len(self.lexicon.docs.items)))

        not_doc_ids = []
        j = 0
        i = 0

        while i < len(all_doc_ids) and j < len(doc_ids):
            if all_doc_ids[i] < doc_ids[j]:
                not_doc_ids.append(all_doc_ids[i])
                i += 1
            elif all_doc_ids[i] > doc_ids[j]:
                j += 1
            else:
                i += 1
                j += 1

        while i < len(all_doc_ids):
            not_doc_ids.append(all_doc_ids[i])
            i += 1

        self.stack.append(not_doc_ids)

    def and_(self):
        left_doc_ids = self.stack.pop()
        right_doc_ids = self.stack.pop()

        i = 0
        j = 0
        common_doc_ids = []

        while i < len(left_doc_ids) and j < len(right_doc_ids):
            if left_doc_ids[i] < right_doc_ids[j]:
                i += 1
            elif left_doc_ids[i] > right_doc_ids[j]:
                j += 1
            else:
                common_doc_ids.append(left_doc_ids[i])
                i += 1
                j += 1

        self.stack.append(common_doc_ids)

    def or_(self):
        left_doc_ids = self.stack.pop()
        right_doc_ids = self.stack.pop()

        i = 0
        j = 0
        all_doc_ids = []

        while i < len(left_doc_ids) and j < len(right_doc_ids):
            if left_doc_ids[i] < right_doc_ids[j]:
                all_doc_ids.append(left_doc_ids[i])
                i += 1
            elif left_doc_ids[i] > right_doc_ids[j]:
                all_doc_ids.append(right_doc_ids[j])
                j += 1
            else:
                all_doc_ids.append(left_doc_ids[i])
                i += 1
                j += 1

        while i < len(left_doc_ids):
            all_doc_ids.append(left_doc_ids[i])
            i += 1

        while j < len(right_doc_ids):
            all_doc_ids.append(right_doc_ids[j])
            j += 1

        self.stack.append(all_doc_ids)

    @property
    def result(self) -> list[str]:
        doc_ids = self.stack.pop()
        assert len(self.stack) == 0
        return self.lexicon.get_docs(doc_ids)


class InvertedIndexQueryExecutor(QueryExecutor):
    QUERY_CONTEXT_CLASS = InvertedIndexQueryContext
