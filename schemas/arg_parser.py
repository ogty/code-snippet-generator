from enum import Enum
from typing import TypedDict, Any, Tuple


Long = str
Short = str


class Actions(Enum):
    store = "store"
    count = "count"
    append = "append"
    append_const = "append_const"
    store_const = "store_const"
    store_true = "store_true"
    store_false = "store_false"


class SubCommand(TypedDict):
    name: str
    help: str


class Argument(TypedDict):
    flags: Tuple[Long, Short]
    type: Any
    help: str
    required: bool
    action: Actions


class Arguments(Enum):
    file = Argument(flags=("--file", "-f"), type=str, help="")
    path = Argument(flags=("--path", "-p"), type=str, help="", required=True)
    width = Argument(flags=("--width", "-w"), type=int, help="")
    output = Argument(flags=("--output", "-o"), type=str, help="")
    prefix = Argument(flags=("--prefix", "-x"), type=str, help="")
    language = Argument(flags=("--language", "-l"), type=str, help="")
    line_number = Argument(
        flags=("--line-number", "-n"),
        action=Actions.store_true.value,
    )
    start_line = Argument(flags=("--start-line", "-s"), type=int, help="")
    current_file = Argument(
        flags=("--current-file", "-c"),
        action=Actions.store_true.value,
    )
    command_prompt = Argument(
        flags=("--command-prompt", "-m"),
        action=Actions.store_true.value,
    )
