from dataclasses import dataclass

from .utils.metaclasses import FromDictMeta


@dataclass
class DomainCheck(metaclass=FromDictMeta):
    classification: str
    verifiedPhish: bool

    @classmethod
    def from_dict(cls, data: dict) -> "DomainCheck":
        return cls(
            classification=data.get("classification", ""),
            verifiedPhish=data.get("verifiedPhish", False),
        )
