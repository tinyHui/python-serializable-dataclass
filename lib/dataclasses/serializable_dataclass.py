from dataclasses import _process_class
from .consts import Lang
from .json_serializer import json_serialize

__SERIALIZABLE_SIGN = "__is_serializable__"


def serializable_dataclass(
    cls,
    /,
    *,
    language=Lang.JSON,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
):
    def wrapper(cls):
        processed_class = _process_class(
            cls, init, repr, eq, order, unsafe_hash, frozen
        )
        if language == Lang.JSON:
            serialize_fn = json_serialize
        else:
            raise NotImplemented(f"language {language} does not supported")
        setattr(processed_class, __SERIALIZABLE_SIGN, True)
        setattr(processed_class, "serialize", serialize_fn)
        return processed_class

    # call with no parameters
    if cls is None:
        return wrapper

    # class with parameters
    return wrapper(cls)
