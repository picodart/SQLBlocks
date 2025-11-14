from abc import ABC, abstractmethod
from core.entities import BasicSQLBlock
from typing import List


class BasicSQLScriptLoader(ABC):
    @abstractmethod
    def load_scripts(self, sources: List[BasicSQLBlock]) -> List[str]:
        pass