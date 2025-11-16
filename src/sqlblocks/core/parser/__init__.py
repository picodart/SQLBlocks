from sqlblocks.core.entities import Result, BasicSQLBlock
from sqlblocks.core.consts import ParseErrors
from sqlblocks.core.parser.parser_by_type import TYPE_PARSERS
from dataclasses import fields


class SQLBlockParser:

    def __init__(self):
        self._metadata_fields = {field.name: field.type for field in fields(BasicSQLBlock)}

    def parse(self, str_block: str) -> Result[BasicSQLBlock]:
        """ 
        Parse str to BasicSQLBlock
        Extract name, depends, etc
        """
        metadata = {}
        is_sql = False
        sql = ''

        try:
            for i in str_block.split('\n'):
                if is_sql:
                    sql += f"\n{i.rstrip()}"
                    continue

                current_string = i.strip()

                if not current_string:
                    continue

                if not current_string.startswith('--'):
                    is_sql = True
                    sql += i.rstrip()
                    continue
                
                index_dots = current_string.find(':')
                field = current_string[2:index_dots].strip()

                if not (field_type := self._metadata_fields.get(field, None)):
                    return Result.err(ParseErrors.INVALID_NAME)
                
                if metadata.get(field):
                    return Result.err(ParseErrors.DUBLICATE_NAME)
                
                data = TYPE_PARSERS[field_type](current_string[index_dots:])
                metadata[field] = data

            metadata['sql'] = sql

            return Result.ok(
                BasicSQLBlock(**metadata)
            )
        
        except Exception as e:
            return Result.err(f"Parse error: {e}")