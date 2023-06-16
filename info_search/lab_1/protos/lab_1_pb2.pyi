from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Lexicon(_message.Message):
    __slots__ = ["docs", "terms"]
    DOCS_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedScalarFieldContainer[str]
    terms: _containers.RepeatedCompositeFieldContainer[Term]
    def __init__(
        self,
        terms: _Optional[_Iterable[_Union[Term, _Mapping]]] = ...,
        docs: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class Term(_message.Message):
    __slots__ = ["frequency", "id", "name"]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    frequency: int
    id: int
    name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        id: _Optional[int] = ...,
        frequency: _Optional[int] = ...,
    ) -> None: ...
