import typing as t


class FromDictMeta(type):
    """Metaclass to ensure inherited classes have `from_dict` class method."""
    def __new__(
        cls,
        name: str,
        bases: t.Tuple[type, ...],
        attrs: t.Dict[str, t.Any],
    ):
        if "from_dict" not in attrs:
            raise TypeError(f"{name} must implement `from_dict` class method.")

        # If exists, ensure callable function
        if not callable(attrs["from_dict"]):
            raise TypeError(f"{name}.from_dict must be callable.")

        return super().__new__(cls, name, bases, attrs)
