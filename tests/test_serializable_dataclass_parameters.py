from dataclasses import FrozenInstanceError
from unittest.mock import patch

import pytest

from lib.dataclasses import serializable_dataclass


def test_should_throw_frozen_instance_error_when_frozen_enabled():
    @serializable_dataclass(frozen=True)
    class AnyData:
        field: str

    v = AnyData.deserialize({"field": "abc"})
    with pytest.raises(FrozenInstanceError):
        v.field = "def"


def test_should_customize_repr_work_when_repr_disabled():
    @serializable_dataclass(repr=False)
    class AnyData:
        field: str

        def __repr__(self):
            return "yes"

    v = AnyData.deserialize({"field": "abc"})
    assert str(v) == "yes"


@patch("lib.dataclasses.entry._process_class")
def test_should_call_dataclass_initial_function_when_give_parameters(mock_process_class):
    kwargs = {
        "init": False,
        "repr": False,
        "eq": False,
        "order": True,
        "unsafe_hash": True,
        "frozen": True,
    }

    @serializable_dataclass(**kwargs)
    class AnyData:
        field: str

    assert mock_process_class.called
    assert mock_process_class.call_args[1:] == (kwargs,)
