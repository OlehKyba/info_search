import bisect

from info_search.lab_1.lexicon import Lexicon
from info_search.lab_1.preprocessing import WordsNormalizer, WordsTokenizer


class CoordinateIndex:
    def __init__(self):
        self.index: dict[int, list[tuple[int, list[int]]]] = {}

    def add_term(
        self,
        doc_id: int,
        term_id: int,
        position: int,
    ) -> None:
        doc_ids = self.index.setdefault(term_id, [])

        doc_index = bisect.bisect_left(doc_ids, doc_id, key=lambda row: row[0])
        if doc_index == len(doc_ids) or doc_ids[doc_index][0] != doc_id:
            doc_ids.insert(doc_index, (doc_id, [term_id]))
            return

        positions = doc_ids[doc_index][1]
        position_index = bisect.bisect_left(positions, position)
        positions.insert(position_index, position)

    @staticmethod
    def _is_neighbors(
        left_positions: list[int], right_positions: list[int], distance: int
    ) -> bool:
        i, j = 0, 0

        while i < len(left_positions) and j < len(right_positions):
            diff = abs(left_positions[i] - right_positions[j])
            if diff <= distance:
                return True
            elif left_positions[i] < right_positions[j]:
                i += 1
            else:
                j += 1

        return False

    def _merge_doc_ids(
        self,
        left_doc_ids: list[tuple[int, list[int]]],
        right_doc_ids: list[tuple[int, list[int]]],
        distance: int,
    ) -> list[int]:
        i = 0
        j = 0
        common_doc_ids = []

        while i < len(left_doc_ids) and j < len(right_doc_ids):
            left_doc_ids_idx = left_doc_ids[i][0]
            right_doc_ids_idx = right_doc_ids[j][0]
            if left_doc_ids_idx < right_doc_ids_idx:
                i += 1
            elif left_doc_ids_idx > right_doc_ids_idx:
                j += 1
            else:
                if self._is_neighbors(
                    left_doc_ids[i][1],
                    right_doc_ids[j][1],
                    distance,
                ):
                    common_doc_ids.append(left_doc_ids_idx)
                i += 1
                j += 1

        return common_doc_ids

    def search(
        self,
        first_term_id: int,
        second_term_id: int,
        distance: int,
    ) -> list[int]:
        first_doc_ids = self.index[first_term_id]
        second_doc_ids = self.index[second_term_id]
        return self._merge_doc_ids(first_doc_ids, second_doc_ids, distance)


class CoordinateIndexQueryExecutor:
    def __init__(
        self,
        coordinate_index: CoordinateIndex,
        lexicon: Lexicon,
        tokenizer: WordsTokenizer,
        normalizer: WordsNormalizer = None,
    ):
        self._coordinate_index = coordinate_index
        self._lexicon = lexicon
        self._tokenizer = tokenizer
        self._normalizer = normalizer

    def _parse_query(self, query: str) -> tuple[str, str, int]:
        first_word, command, second_word = query.split(" ")

        first_term = self._normalizer.normalize(first_word.lower())
        second_term = self._normalizer.normalize(second_word.lower())
        distance = int(command[1:])

        return first_term, second_term, distance

    def search(self, query: str) -> list[str]:
        first_term, second_term, distance = self._parse_query(query)

        doc_ids = self._coordinate_index.search(
            first_term_id=self._lexicon.get_term_id(first_term),
            second_term_id=self._lexicon.get_term_id(second_term),
            distance=distance,
        )

        return self._lexicon.get_docs(doc_ids)
