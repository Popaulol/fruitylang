from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class Unit:
    magnitude: float | int = 0
    s: float | int = 0
    m: float | int = 0
    kg: float | int = 0
    A: float | int = 0
    K: float | int = 0
    mol: float | int = 0
    cd: float | int = 0

    def __str__(self) -> str:
        for name, value in UNIT_MAP.items():
            if value[0] == self and value[1]:
                return name

        return " ".join(
            " ".join(
                (
                    (
                        (
                            "10"
                            + ("^" + str(self.magnitude) if self.magnitude != 1 else "")
                        )
                        if self.magnitude != 0
                        else ""
                    ),
                    (
                        ("s" + ("^" + str(self.s) if self.s != 1 else ""))
                        if self.s != 0
                        else ""
                    ),
                    (
                        ("m" + ("^" + str(self.m) if self.m != 1 else ""))
                        if self.m != 0
                        else ""
                    ),
                    (
                        ("kg" + ("^" + str(self.kg) if self.kg != 1 else ""))
                        if self.kg != 0
                        else ""
                    ),
                    (
                        ("A" + ("^" + str(self.A) if self.A != 1 else ""))
                        if self.A != 0
                        else ""
                    ),
                    (
                        ("K" + ("^" + str(self.K) if self.K != 1 else ""))
                        if self.K != 0
                        else ""
                    ),
                    (
                        ("mol" + ("^" + str(self.mol) if self.mol != 1 else ""))
                        if self.mol != 0
                        else ""
                    ),
                    (
                        ("cd" + ("^" + str(self.cd) if self.cd != 1 else ""))
                        if self.cd != 0
                        else ""
                    ),
                )
            )
            .strip()
            .split(" ")
        )

    def combined(self, other: Unit) -> Unit:
        return Unit(
            self.magnitude * other.magnitude,
            self.s + other.s,
            self.m + other.m,
            self.kg + other.kg,
            self.A + other.A,
            self.K + other.K,
            self.mol + other.mol,
            self.cd + other.cd,
        )


UNIT_MAP: dict[str, Tuple[Unit, bool]] = {
    # SI Base Units
    "s": (Unit(s=1), True),
    "m": (Unit(m=1), True),
    "kg": (Unit(kg=1), True),
    "A": (Unit(A=1), True),
    "K": (Unit(K=1), True),
    "mol": (Unit(mol=1), True),
    "cd": (Unit(cd=1), True),
    # Combined Units
    "Hz": (Unit(s=-1), True),
    "rad": (Unit(), False),
    "sr": (Unit(), False),
    "N": (Unit(kg=1, m=1, s=-1), True),
    "Pa": (Unit(kg=1, m=-1, s=-2), True),
    "J": (Unit(kg=1, m=2, s=-2), True),
    "W": (Unit(kg=1, m=2, s=-3), True),
    "C": (Unit(A=1, s=-1), True),
    "V": (Unit(kg=1, m=2, s=-3, A=-1), True),
    "F": (Unit(kg=-1, m=-2, s=4, A=2), True),
    "O": (
        Unit(kg=1, m=2, s=-3, A=-2),
        True,
    ),  # Ohm, since the Omega symbol isn't available on most keyboards
    "S": (Unit(kg=-1, m=-2, s=3, A=2), True),
    "Wb": (Unit(kg=1, m=2, s=-2, A=-1), True),
    "T": (Unit(kg=1, s=-2, A=-1), True),
    "H": (Unit(kg=1, m=2, s=-2, A=-2), True),
    "lm": (Unit(cd=1), False),
    "lx": (Unit(cd=1, m=-2), True),
    "Bq": (Unit(s=-1), False),
    "Gy": (Unit(m=2, s=-2), True),
    "Sv": (Unit(m=2, s=2), True),
    "kat": (Unit(s=-1, mol=1), True),
}
