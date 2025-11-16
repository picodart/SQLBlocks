from abc import ABC, abstractmethod
from sqlblocks.core.entities import BasicSQLBlock
from typing import List, Tuple
from collections.abc import Generator


class BasicSQLScriptLoader(ABC):
    @abstractmethod
    def load_scripts(self, sources: List[BasicSQLBlock]) -> List[str]:
        pass

    @abstractmethod
    def extract_blocks(self) -> Generator[Tuple[str, str], None, None]:
        pass