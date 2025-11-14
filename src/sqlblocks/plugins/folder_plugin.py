from plugins import BasicSQLScriptLoader
from core.entities import BasicSQLBlock
from pathlib import Path
from typing import List


class FolderPlugin(BasicSQLScriptLoader):

    def __init__(self, base_path = Path):
        self._base_path = base_path

    def load_scripts(self, blocks: List[BasicSQLBlock]):
        result = []

        for block in blocks:
            with open(self._base_path / block.source, 'r') as file:
                result.append(
                    file.read()
                )

        return result

