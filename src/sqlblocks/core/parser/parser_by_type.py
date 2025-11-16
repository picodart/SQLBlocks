from typing import Optional, Tuple, Any, Dict, Type, Callable
import re


TYPE_PARSERS: Dict[Type, Callable[[str], Any]] = {}

def register_parser(type_hint: Type):
    """Декоратор для регистрации парсеров"""
    def decorator(func: Callable[[str], Any]):
        TYPE_PARSERS[type_hint] = func
        return func
    return decorator


@register_parser(str)
def parse_string(value: str) -> str:
    matches = re.findall(r'"([^"]*)"', value.strip())
    return matches[0] if matches else None

@register_parser(Optional[str])
def parse_optional_string(value: str) -> Optional[str]:
    return parse_string(value) if value.strip() else None

@register_parser(Tuple[str, ...])
def parse_string_tuple(value: str) -> Tuple[str, ...]:
    items = re.findall(r'["\']([^"\']*)["\']', value)
    return tuple(items)

@register_parser(Optional[Tuple[str, ...]])
def parse_optional_string_tuple(value: str) -> Optional[Tuple[str, ...]]:
    return parse_string_tuple(value) if value.strip() else None