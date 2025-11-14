from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class BasicSQLBlock:
    name: str
    source: str  
    depends: Optional[Tuple[str, ...]] = None

    def __post_init__(self):
        self.depends = self.depends or ()
