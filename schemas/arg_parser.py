from enum import Enum
from typing import TypedDict, Any, Tuple


Long = str
Short = str


class SubCommand(TypedDict):
    name: str
    help: str


class Argument(TypedDict):
    flags: Tuple[Long, Short]
    type: Any
    help: str
    required: bool


class Arguments(Enum):
    file = Argument(flags=("--file", "-f"), type=str, help="", required=True)
    path = Argument(flags=("--path", "-p"), type=str, help="", required=True)
    width = Argument(flags=("--width", "-w"), type=int, help="")
    output = Argument(flags=("--output", "-o"), type=str, help="")
    language = Argument(flags=("--language", "-l"), type=str, help="")
