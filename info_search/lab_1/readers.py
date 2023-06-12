from typing import Iterable

from tqdm import tqdm
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


def _create_doc_id(file_name: str, page: str) -> str:
    return f"{file_name}/{page}"


class EpubReader:
    def __init__(self, file_paths: Iterable[str]):
        self._file_paths = file_paths

    def read(self) -> Iterable[tuple[str, str]]:
        for file_path in tqdm(self._file_paths):
            file_name = file_path.split("/")[-1]
            book = epub.read_epub(file_path)
            for doc in book.get_items_of_type(ITEM_DOCUMENT):
                doc_id = _create_doc_id(file_name, doc.get_name())
                soup = BeautifulSoup(doc.get_content(), features="xml")

                for child in soup.descendants:
                    if child.name and child.string:
                        yield doc_id, child.string
