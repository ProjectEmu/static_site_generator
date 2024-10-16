from enum import Enum
from typing import Optional


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: Optional[str] = url

    def __eq__(self, value: object) -> bool:
        if (
            isinstance(value, TextNode)
            and value.text == self.text
            and value.text_type == self.text_type
            and value.url == self.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
