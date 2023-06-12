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
    __slots__ = ["terms_frequency"]
    TERMS_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    terms_frequency: _containers.RepeatedCompositeFieldContainer[TermFrequency]
    def __init__(
        self,
        terms_frequency: _Optional[_Iterable[_Union[TermFrequency, _Mapping]]] = ...,
    ) -> None: ...

class TermFrequency(_message.Message):
    __slots__ = ["frequency", "term"]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    frequency: int
    term: str
    def __init__(
        self, term: _Optional[str] = ..., frequency: _Optional[int] = ...
    ) -> None: ...
