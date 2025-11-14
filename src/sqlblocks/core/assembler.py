from sqlblocks.core.registry import SQLBlockRegistry
from core.entities import BasicSQLBlock
from plugins import BasicSQLScriptLoader
from typing import Tuple, List


class SQLAssembler:

    def __init__(
            self, 
            registry: SQLBlockRegistry, 
            sql_loader: BasicSQLScriptLoader,
        ):
        self._registry = registry
        self._sql_loader = sql_loader
        
    def assemble_sql(
            self, 
            target_name: str, 
        ) -> str:
        execute_plan = self._build_execute_plan(target_name)
        sql_scripts = self._sql_loader.load_scripts(execute_plan)
        assembled = "WITH\n"
        ctes = []

        for i in range(len(execute_plan) - 1):
            block = execute_plan[i]
            ctes.append(
                f"-- Block: {block.name}"
                f"{block.name} AS (\n{sql_scripts[i]}\n)"
            )
        
        assembled += ',\n'.join(ctes)
        assembled += f"\n-- Main query\n{sql_scripts[-1]}"

        return assembled


    def _build_execute_plan(self, target_name: str) -> List[BasicSQLBlock]:
        visited = set()
        order = [target_name]
        execute_order = []

        while order:
            name = order.pop(0)
            block = self._registry.get_block(name)

            if block is None:
                raise ValueError("block not found")
            
            if name in visited:
                continue

            visited.add(name)
            execute_order.append(block)

            for i in block.depends:
                order.append(i)

        return execute_order[::-1]


            
