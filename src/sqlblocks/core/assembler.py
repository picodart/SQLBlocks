from sqlblocks.core.registry import SQLBlockRegistry
from sqlblocks.core.entities import BasicSQLBlock
from sqlblocks.core.parser import SQLBlockParser
from sqlblocks.plugins import BasicSQLScriptLoader
from sqlblocks import exceptions
from typing import List, Optional
import yaml
from pathlib import Path
import shutil


class SQLAssembler:

    def __init__(
            self, 
            base_path: Path = Path.cwd(),
            sql_loader: Optional[BasicSQLScriptLoader] = None,
            registry: SQLBlockRegistry = SQLBlockRegistry(), 
            sql_block_parser: SQLBlockParser = SQLBlockParser(),
        ):
        self._base_path = base_path
        self._sql_loader = sql_loader
        self._registry = registry
        self._sql_block_parser = sql_block_parser

    @property
    def work_dir(self):
        return self._base_path / '.sql_blocks'
    
    @property
    def blocks_dir(self):
        return self.work_dir / 'blocks'

    def recreate_work_dir(self) -> Optional[Path]:
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)
        
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.blocks_dir.mkdir(parents=True, exist_ok=True)

        return self.work_dir

    def build(self) -> None:
        print("Import blocks START")

        for source, item in self._sql_loader.extract_blocks():
            result = self._sql_block_parser.parse(item)

            if result.success:
                block = result.data
                self._registry.add_block(block)
                print(f"[{source}]: SUCCES")
                continue
        
            print(f"[{source}]: ERROR: {result.error}")

        print("Import blocks DONE")
        print("Create blocks depends START")
        work_dir = self.recreate_work_dir()
        blocks_depends = {}
        
        for block in self._registry.all_blocks:
            try: 
                execute_plan = self._build_execute_plan(block.name)
                path = f"blocks/{block.name}.sql"
                blocks_depends[block.name] = {
                    "depends": [i.name for i in execute_plan[:-1]],
                    "sql": path
                }
                with open(work_dir / path, 'w') as file:
                    file.write(block.sql)

                print(f'Block "{block.name}" create depends SUCCESS')
            except exceptions.NonExistentLink as e:
                print(f'Block "{block.name}" refers to a non-existent block {e}')
            except Exception as e:
                print(f'Block "{block.name}" error: {e}')

        with open(work_dir / "blocks.toml", 'w') as file:
            yaml.dump(blocks_depends, file, default_flow_style=False)
        

        print("Create blocks depends DONE")
        
    def assemble_sql(
            self, 
            target_name: str, 
        ) -> str:
        with open(self.work_dir / "blocks.toml") as f:
            config: dict = yaml.safe_load(f)

        result = 'WITH\n'

        if not (target_block := config.get(target_name)):
            raise ValueError(f'{target_block} not exist')
        
        depends = target_block.get("depends")

        for i in depends:
            if not (current_block := config.get(i)):
                raise ValueError(f'{current_block} not exist')
            

            with open(self.work_dir / current_block.get('sql'), 'r') as file:
                result += f"{i} AS (\n{file.read()}\n),\n"

        with open(self.work_dir / target_block.get('sql'), 'r') as file:
            result += f"{target_name} AS (\n{file.read()}\n)\nSELECT * FROM {target_name}"
    
        return result
    

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
                raise exceptions.NonExistentLink(f'block "{name}" not found')
            
            if name in visited:
                continue

            visited.add(name)
            execute_order.append(block)

            for i in block.depends:
                order.append(i)

        return execute_order[::-1]


            
