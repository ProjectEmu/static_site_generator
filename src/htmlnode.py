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
        if not value:
            raise ValueError()
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        props = ""
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        if self.props:
            props = " " + self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
