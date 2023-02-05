from abc import ABCMeta, abstractclassmethod


class CodeSnippetFrameInterface(metaclass=ABCMeta):
    @abstractclassmethod
    def set_initial_line(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def set_code(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def set_final_line(self) -> None:
        raise NotImplementedError


class CodeSnippetInterface(metaclass=ABCMeta):
    @abstractclassmethod
    def generate(self) -> str:
        raise NotImplementedError
