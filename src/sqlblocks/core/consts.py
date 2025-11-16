from enum import Enum


class ParseErrors(str, Enum):
    INVALID_NAME = 'invalid'
    DUBLICATE_NAME = 'duplicate'