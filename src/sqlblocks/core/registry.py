from sqlblocks.core.entities import BasicSQLBlock
from sqlblocks import exceptions
from typing import Dict
from collections.abc import Generator


class SQLBlockRegistry:

    def __init__(self):
        self._blocks:  Dict[str, BasicSQLBlock] = {}

    def add_block(self, block: BasicSQLBlock) -> None:
        if block.name in self._blocks:
            raise exceptions.DuplicateNameError(
                f'a block named "{block.name}" has already been added'
            )

        self._blocks[block.name] = block
        self._check_loop_exist()

    def get_block(self, name: str) -> BasicSQLBlock:
        return self._blocks.get(name)

    @property
    def all_blocks(self) -> Generator[BasicSQLBlock, None, None]:
        for _, block in self._blocks.items():
            yield block

    def _check_loop_exist(self):
        depends_count = {
            i: 0 for i in self._blocks
        }
        count = 0
        order = []

        for i in self._blocks:
            for neighbor in self._blocks[i].depends:
                if neighbor in depends_count:
                    depends_count[neighbor] += 1

        for i in depends_count:
            if depends_count[i] == 0:
                order.append(i)

        while order:
            current = order.pop(0)
            count += 1
            block = self.get_block(current)

            for neighbor in block.depends:
                if neighbor not in depends_count:
                    continue
                
                depends_count[neighbor] -= 1

                if depends_count[neighbor] == 0:
                    order.append(neighbor)

        if count != len(self._blocks):
            raise exceptions.CyclicalAddictionError("Blocks have circular references")
    