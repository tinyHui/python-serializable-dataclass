from types import GeneratorType
from typing import Text, Dict, Union, Sequence, List, Any


def __serialize_value(value: Any):
    if getattr(value, "__is_serializable__", False):
        return value.serialize()
    elif (
        isinstance(value, list)
        or isinstance(value, tuple)
        or isinstance(value, GeneratorType)
    ):
        return [__serialize_value(v) for v in value]
    elif isinstance(value, dict):
        return {str(k): __serialize_value(value[k]) for k in value}
    else:
        return value


def json_serialize(self):
    cls_annotations = self.__annotations__
    result = {}

    for field_name in cls_annotations:
        desired_type = cls_annotations[field_name]
        value = getattr(self, field_name)
        result[field_name] = __serialize_value(value)

    return result
