def json_serialize(self):
    cls_annotations = self.__annotations__
    result = {}

    for field in cls_annotations:
        field_type = cls_annotations[field]
        value = getattr(self, field)
        if getattr(value, "__is_serializable__", False):
            result[field] = value.serialize()
        else:
            result[field] = value
    return result
