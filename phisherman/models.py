from dataclasses import dataclass

from .utils.metaclasses import FromDictMeta


@dataclass
class DomainCheck(metaclass=FromDictMeta):
    classification: str
    verified_phish: bool

    @classmethod
    def from_dict(cls, data: dict) -> "DomainCheck":
        return cls(
            classification=data.get("classification", ""),
            verified_phish=data.get("verifiedPhish", False),
        )
