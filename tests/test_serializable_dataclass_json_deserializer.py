from typing import Text, Optional, Union, Sequence, List, Set, Tuple

from lib.dataclasses import serializable_dataclass


def test_json_deserializer_should_works_when_class_is_simple():
    @serializable_dataclass
    class AnyData:
        field1: int
        field2: str
        field3: Text

    assert AnyData.deserialize(
        {"field1": 1, "field2": "string", "field3": "another string"}
    ) == AnyData(field1=1, field2="string", field3="another string")


def test_json_deserializer_should_works_when_class_have_optional_field():
    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Optional[str]
        field3: Text

    assert AnyData.deserialize(
        {"field1": 1, "field2": "string", "field3": "another string",}
    ) == AnyData(field1=1, field2="string", field3="another string")

    assert AnyData.deserialize(
        {"field1": 1, "field2": None, "field3": "another string",}
    ) == AnyData(field1=1, field2=None, field3="another string")


def test_json_deserializer_should_works_when_class_have_union_field():
    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Union[str, int, bool]
        field3: Text

    assert AnyData.deserialize(
        {"field1": 1, "field2": 2, "field3": "another string",}
    ) == AnyData(field1=1, field2=2, field3="another string")

    assert AnyData.deserialize(
        {"field1": 1, "field2": None, "field3": "another string",}
    ) == AnyData(field1=1, field2=None, field3="another string")


def test_json_deserializer_should_works_when_field_is_sequence():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Sequence[AnyDataInner]

    assert AnyData.deserialize(
        {"field1": 1, "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],}
    ) == AnyData(field1=1, field2=[AnyDataInner("a"), AnyDataInner("b")])


def test_json_deserializer_should_works_when_field_is_list():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: List[AnyDataInner]

    assert AnyData.deserialize(
        {"field1": 1, "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],}
    ) == AnyData(field1=1, field2=[AnyDataInner("a"), AnyDataInner("b")])


def test_json_deserializer_should_works_when_field_is_set():
    @serializable_dataclass(unsafe_hash=True)
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Set[AnyDataInner]

    assert AnyData.deserialize(
        {"field1": 1, "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],}
    ) == AnyData(field1=1, field2={AnyDataInner("a"), AnyDataInner("b")})


def test_json_deserializer_should_works_when_field_is_tuple():
    @serializable_dataclass
    class AnyDataInner:
        field_inner1_1: Text

    @serializable_dataclass
    class AnyData:
        field1: int
        field2: Tuple[AnyDataInner]

    assert AnyData.deserialize(
        {"field1": 1, "field2": [{"field_inner1_1": "a"}, {"field_inner1_1": "b"}],}
    ) == AnyData(field1=1, field2=(AnyDataInner("a"), AnyDataInner("b")))


def test_json_deserializer_should_works_when_class_is_hierarchy():
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

    assert AnyData.deserialize(
        {
            "field1": 1,
            "field2": "string",
            "field3": "another string",
            "field4": {
                "field_inner1_1": "inner 11",
                "field_inner1_2": {"field_inner2_1": "inner 12"},
            },
        }
    ) == AnyData(
        field1=1,
        field2="string",
        field3="another string",
        field4=AnyDataInner(
            field_inner1_1="inner 11",
            field_inner1_2=AnyDataInner2(field_inner2_1="inner 12"),
        ),
    )
