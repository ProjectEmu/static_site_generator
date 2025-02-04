from functools import reduce
from typing import List, Dict, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        self.tag: str = tag
        self.value: Optional[str] = value
        self.children: List["HTMLNode"] = children if children is not None else []
        self.props: Dict[str, str] = props if props is not None else {}

    def __repr__(self) -> str:
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={len(self.children)} children, props={self.props})"

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: str = None,
        props: Optional[Dict[str, str]] = None,
    ):
        if value is None:
            raise ValueError()
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        props = ""
        if self.value is None:
            raise ValueError()
        if not self.tag:
            return self.value
        if self.props:
            props = " " + self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        children: List["HTMLNode"] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        if not children:
            raise ValueError("INIT: Children are required for ParentNode")
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        props = ""
        children_html = ""
        if not self.tag:
            raise ValueError("Tag is required for ParentNode")
        if self.children:
            children_html = children_html = "".join(
                child.to_html() for child in self.children
            )
        else:
            raise ValueError("Children are required for ParentNode")
        if self.props:
            props = " " + self.props_to_html()
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"
