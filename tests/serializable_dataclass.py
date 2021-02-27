from typing import Text, Optional, Union

from lib.dataclasses import serializable_dataclass


def test_should_serialize_works_when_class_is_simple():
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


def test_should_serialize_works_when_class_have_optional_field():
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


def test_should_serialize_works_when_class_have_union_field():
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


def test_should_serialize_works_when_class_is_hierarchy():
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
