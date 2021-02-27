from lib.dataclasses.registry import SerializableDataclassRegistry


def test_serializable_dataclass_registry_should_be_singleton():
    return id(SerializableDataclassRegistry()) == id(SerializableDataclassRegistry)


def test_registry_should_registry_class_under_different_package_but_with_same_name():
    registry = SerializableDataclassRegistry()

    class Scope1:
        class AnyClass:
            ...

    class Scope2:
        class AnyClass:
            ...

    registry.register(Scope1.AnyClass)
    registry.register(Scope2.AnyClass)

    assert len(registry) == 2
