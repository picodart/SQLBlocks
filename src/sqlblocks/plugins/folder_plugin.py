from sqlblocks.plugins import BasicSQLScriptLoader
from sqlblocks.core.entities import BasicSQLBlock
from pathlib import Path
from typing import Tuple, List
from collections.abc import Generator


class FolderPlugin(BasicSQLScriptLoader):

    def __init__(self, base_path: Path):
        self._base_path = base_path

    def load_scripts(self, blocks: List[BasicSQLBlock]):
        result = []

        for block in blocks:
            with open(self._base_path / block.source, 'r') as file:
                result.append(
                    file.read()
                )

        return result
    
    def _inspect_folder(self, path: Path) -> Tuple[List, List]:
        pass
    
    def extract_blocks(self) -> Generator[Tuple[str, str], None, None]:
        order = [self._base_path]

        while order:
            current_path = order.pop(0)
            current_path.glob
            
            for item in current_path.iterdir():
                if item.is_file() and item.suffix == ".sql":
                    with open(item, "r", encoding="utf-8") as file:
                        yield item.name, file.read()

                if item.is_dir():
                    order.append(item)


        

