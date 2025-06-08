from enum import StrEnum


class ModeEnum(StrEnum):
    DEV = "DEV"
    TEST = "TEST"
    PROD = "PROD"


class LogLevelEnum(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LanguageEnum(StrEnum):
    EN = "en"
