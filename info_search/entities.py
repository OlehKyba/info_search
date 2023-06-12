from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    doc_id: str
    value: str
