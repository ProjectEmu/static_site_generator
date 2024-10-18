from enum import Enum
from typing import Optional


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

    @classmethod
    def is_valid(cls, value: object) -> bool:
        return value in cls.__members__.values()


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        self.text: str = text
        if TextType.is_valid(text_type):
            self.text_type: TextType = text_type.value
        else:
            raise ValueError("Not a valid TextType")
        self.url: Optional[str] = url

    def __eq__(self, value: object) -> bool:
        if type(value) is not TextNode:
            return False
        return (
            value.text == self.text
            and value.text_type == self.text_type
            and value.url == self.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
