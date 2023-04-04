from abc import ABCMeta
from typing import Any


class CodeSnippetFrameInterface(metaclass=ABCMeta):
    def set_initial_line(self) -> None:
        raise NotImplementedError

    def set_code(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def set_final_line(self) -> None:
        raise NotImplementedError


class CodeSnippetInterface(metaclass=ABCMeta):
    def generate(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError
