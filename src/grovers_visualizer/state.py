from collections.abc import Iterable, Iterator
from typing import Self, override


class QubitState:
    def __init__(self, bits: Iterable[int]) -> None:
        bits_tuple = tuple(bits)  # Convert to not consume it
        if not all(b in (0, 1) for b in bits_tuple):
            raise ValueError(f"{self.__class__.__name__} must be a tuple of `0`s and `1`s")
        self._bits: tuple[int, ...] = tuple(bits_tuple)

    @property
    def bits(self) -> tuple[int, ...]:
        return self._bits

    @property
    def bitsring(self) -> str:
        return "".join(str(b) for b in self._bits)

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(int(b) for b in s)

    @classmethod
    def from_int(cls, value: int, num_qubits: int) -> Self:
        bits = (int(x) for x in format(value, f"0{num_qubits}b"))
        return cls(bits)

    @override
    def __str__(self) -> str:
        return self.bitsring

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.bitsring}')"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, QubitState):
            return self.bitsring == value.bitsring
        if isinstance(value, str):
            return self.bitsring == value
        if isinstance(value, (list, tuple)):
            return self.bits == tuple(value)
        return NotImplemented

    def __lt__(self, value: object, /) -> bool:
        if isinstance(value, QubitState):
            return int(self.bitsring, 2) < int(value.bitsring, 2)
        if isinstance(value, str) and all(b in "01" for b in value):
            return int(self.bitsring, 2) < int(value, 2)
        if isinstance(value, (list, tuple)):
            return self.bits < tuple(value)
        return NotImplemented

    @override
    def __hash__(self) -> int:
        return hash(self.bitsring)

    def __len__(self) -> int:
        return len(self._bits)

    def __getitem__(self, idx: int | slice) -> int | tuple[int, ...]:
        return self._bits[idx]

    def __iter__(self) -> Iterator[int]:
        return iter(self._bits)


Ket = QubitState
