from decimal import Decimal
from enum import Enum
from typing import Text, Optional, Union, Sequence, Dict, Set

from lib.dataclasses import serializable_dataclass


def test_json_serializer_should_works_when_class_is_simple():
    @serializable_dataclass
    class AnyData:
        field1: int
        field2: str
        field3: Text

    data = AnyData(field1=1, field2="string", field3="another string")
    assert data.serialize() == {
        "field1": 1,
        "field2": "string",
        "field3": "another string",
    }


def test_json_serializer_should_works_when_class_have_decimal_field():
    @serializable_dataclass
    class AnyData:
        field1: Decimal

    data = AnyData(field1=Decimal("1.11101"))
    assert data.serialize() == {"field1": "1.11101"}


def test_json_serializer_should_works_when_class_have_enum_field():
    class E(Enum):
        value = "value"

    @serializable_dataclass
    class AnyData:
        field1: E

    data = AnyData(field1=E.value)
    assert data.serialize() == {"field1": "value"}


def test_json_serializer_should_works_when_class_have_optional_field():
    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Optional[str]
        field3: Text

    data = AnyData(field1=1, field2="string", field3="another string")
    assert data.serialize() == {
        "field1": 1,
        "field2": "string",
        "field3": "another string",
    }

    data = AnyData(field1=1, field2=None, field3="another string")
    assert data.serialize() == {
        "field1": 1,
        "field2": None,
        "field3": "another string",
    }


def test_json_serializer_should_works_when_class_have_union_field():
    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Union[str, int]
        field3: Text

    data = AnyData(field1=1, field2=2, field3="another string")
    assert data.serialize() == {
        "field1": 1,
        "field2": 2,
        "field3": "another string",
    }

    data = AnyData(field1=1, field2=None, field3="another string")
    assert data.serialize() == {
        "field1": 1,
        "field2": None,
        "field3": "another string",
    }


def test_json_serializer_should_works_when_field_is_list():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Sequence[AnyDataInner]

    data = AnyData(field1=1, field2=[AnyDataInner("a"), AnyDataInner("b")])
    assert data.serialize() == {
        "field1": 1,
        "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],
    }


def test_json_serializer_should_works_when_field_is_set():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

        def __hash__(self):
            return id(self.field_inner1_1)

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Set[AnyDataInner]

    data = AnyData(field1=1, field2={AnyDataInner("a"), AnyDataInner("b")})
    assert data.serialize() == {
        "field1": 1,
        "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],
    }


def test_json_serializer_should_works_when_field_is_tuple():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Sequence[AnyDataInner]

    data = AnyData(field1=1, field2=(AnyDataInner("a"), AnyDataInner("b")))
    assert data.serialize() == {
        "field1": 1,
        "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],
    }


def test_json_serializer_should_works_when_field_is_iterator():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Sequence[AnyDataInner]

    def iterator():
        for v in [AnyDataInner("a"), AnyDataInner("b")]:
            yield v

    data = AnyData(field1=1, field2=iterator())
    assert data.serialize() == {
        "field1": 1,
        "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],
    }


def test_json_serializer_should_works_when_field_is_dict():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Dict[str, AnyDataInner]

    class SomeKey:
        def __init__(self, k):
            self.k = k

        def __repr__(self):
            return str(self.k)

        def __str__(self):
            return self.__repr__()

    data = AnyData(
        field1=1,
        field2={SomeKey("v1"): AnyDataInner("a"), SomeKey("v2"): AnyDataInner("b")},
    )
    assert data.serialize() == {
        "field1": 1,
        "field2": {"v1": {"field_inner1_1": "a"}, "v2": {"field_inner1_1": "b"}},
    }


def test_json_serializer_should_works_when_class_is_hierarchy():
    @serializable_dataclass
    class AnyDataInner2:
        field_inner2_1: Text

    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text
        field_inner1_2: AnyDataInner2

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Optional[str]
        field3: Text
        field4: AnyDataInner

    data = AnyData(
        field1=1,
        field2="string",
        field3="another string",
        field4=AnyDataInner(
            field_inner1_1="inner 11",
            field_inner1_2=AnyDataInner2(field_inner2_1="inner 12"),
        ),
    )

    assert data.serialize() == {
        "field1": 1,
        "field2": "string",
        "field3": "another string",
        "field4": {
            "field_inner1_1": "inner 11",
            "field_inner1_2": {"field_inner2_1": "inner 12"},
        },
    }
