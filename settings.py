import re


READ = "r"
WRITE = "w"
ENCODING = "utf-8"

NEWLINE = "\n"
SPACE = " "
PLUS = "+"
MINUS = "-"
EMPTY = ""
ELLIPSIS = "..."

BOX_DRAWINGS_LIGHT_HORIZONTAL = "\u2500"
BOX_DRAWINGS_LIGHT_VERTICAL = "\u2502"
BOX_DRAWINGS_LIGHT_VERTICAL_AND_RIGHT = "\u251C"
BOX_DRAWINGS_LIGHT_VERTICAL_AND_LEFT = "\u2524"
BOX_DRAWINGS_LIGHT_DOWN_AND_HORIZONTAL = "\u252C"
BOX_DRAWINGS_LIGHT_UP_AND_HORIZONTAL = "\u2534"
BOX_DRAWINGS_LIGHT_VERTICAL_AND_HORIZONTAL = "\u253C"
BOX_DRAWINGS_LIGHT_ARC_DOWN_AND_RIGHT = "\u256D"
BOX_DRAWINGS_LIGHT_ARC_DOWN_AND_LEFT = "\u256E"
BOX_DRAWINGS_LIGHT_ARC_UP_AND_LEFT = "\u256F"
BOX_DRAWINGS_LIGHT_ARC_UP_AND_RIGHT = "\u2570"

LIGHT_SHADE = "\u2591"
MEDIUM_SHADE = "\u2592"
DARK_SHADE = "\u2593"

RED = "\u001b[31m"
RESET = "\u001b[0m"
BACKGROUND_LIGHT_GREEN = "\u001b[42m"
BACKGROUND_DARK_GREEN = "\u001b[102m"
BACKGROUND_LIGHT_RED = "\u001b[41m"
BACKGROUND_DARK_RED = "\u001b[101m"

NAMED_FORMAT_PATTERN = re.compile(r"(\{[_a-z]+\})")

DELETION_PATTERN = re.compile(r"^-")
ADDITION_PATTERN = re.compile(r"^\+")
WELL_KNOWN_DELETION_PATTERN = r"-(?P<deletion_start>\d{1,}),?(?P<deletion_end>\d{1,})?"
WELL_KNOWN_ADDITION_PATTERN = r"\+(?P<addition_start>\d{1,}),?(?P<addition_end>\d{1,})?"
WELL_KNOWN_SYMBOLS_PATTERN = re.compile(
    r"^@@ {deletion} {addition} @@".format(
        deletion=WELL_KNOWN_DELETION_PATTERN,
        addition=WELL_KNOWN_ADDITION_PATTERN,
    )
)
