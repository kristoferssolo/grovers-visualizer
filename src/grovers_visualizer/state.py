from collections.abc import Iterator
from typing import Final, Self, override


class QubitState:
    def __init__(self, bits: str) -> None:
        if not all(b in "01" for b in bits):
            raise ValueError(f"{self.__class__.__name__} must be a string of '0' and '1'")
        self._bits: Final[str] = bits

    @property
    def bits(self) -> str:
        return self._bits

    @classmethod
    def from_int(cls, value: int, num_qubits: int) -> Self:
        bits = format(value, f"0{num_qubits}b")
        return cls(bits)

    @override
    def __str__(self) -> str:
        return self._bits

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.bits}')"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, QubitState):
            return self.bits == value.bits
        return False

    @override
    def __hash__(self) -> int:
        return hash(self.bits)

    def __len__(self) -> int:
        return len(self.bits)

    def __getitem__(self, idx: int | slice) -> str:
        return self.bits[idx]

    def __iter__(self) -> Iterator[str]:
        return iter(self.bits)
