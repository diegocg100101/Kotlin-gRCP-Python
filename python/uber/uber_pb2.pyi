from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class tipoUber(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UBER_PLANET: _ClassVar[tipoUber]
    UBER_XL: _ClassVar[tipoUber]
    UBER_BLACK: _ClassVar[tipoUber]
UBER_PLANET: tipoUber
UBER_XL: tipoUber
UBER_BLACK: tipoUber

class Vacio(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TerminarViajeRequest(_message.Message):
    __slots__ = ("posicion", "costo", "placa")
    POSICION_FIELD_NUMBER: _ClassVar[int]
    COSTO_FIELD_NUMBER: _ClassVar[int]
    PLACA_FIELD_NUMBER: _ClassVar[int]
    posicion: Posicion
    costo: float
    placa: str
    def __init__(self, posicion: _Optional[_Union[Posicion, _Mapping]] = ..., costo: _Optional[float] = ..., placa: _Optional[str] = ...) -> None: ...

class Posicion(_message.Message):
    __slots__ = ("X", "Y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    X: float
    Y: float
    def __init__(self, X: _Optional[float] = ..., Y: _Optional[float] = ...) -> None: ...

class infoAuto(_message.Message):
    __slots__ = ("disponibilidad", "posXY", "tipo", "placa")
    DISPONIBILIDAD_FIELD_NUMBER: _ClassVar[int]
    POSXY_FIELD_NUMBER: _ClassVar[int]
    TIPO_FIELD_NUMBER: _ClassVar[int]
    PLACA_FIELD_NUMBER: _ClassVar[int]
    disponibilidad: bool
    posXY: Posicion
    tipo: tipoUber
    placa: str
    def __init__(self, disponibilidad: bool = ..., posXY: _Optional[_Union[Posicion, _Mapping]] = ..., tipo: _Optional[_Union[tipoUber, str]] = ..., placa: _Optional[str] = ...) -> None: ...

class infoServicio(_message.Message):
    __slots__ = ("viajes", "autosLibres", "ganancia")
    VIAJES_FIELD_NUMBER: _ClassVar[int]
    AUTOSLIBRES_FIELD_NUMBER: _ClassVar[int]
    GANANCIA_FIELD_NUMBER: _ClassVar[int]
    viajes: int
    autosLibres: int
    ganancia: float
    def __init__(self, viajes: _Optional[int] = ..., autosLibres: _Optional[int] = ..., ganancia: _Optional[float] = ...) -> None: ...
