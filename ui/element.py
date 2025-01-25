class HTMLElement:
    def __init__(self, tag: str, content: str = "", css_class: str = "", styles: str = "", **attributes):
        self.tag = tag
        self.content = content
        self.css_class = css_class
        self.styles = styles
        self.attributes = attributes  

    def render(self) -> str:
        """
        Génère l'élément HTML.
        """
        class_attr = f' class="{self.css_class}"' if self.css_class else ""
        style_attr = f' style="{self.styles}"' if self.styles else ""
        other_attrs = " ".join(f'{key}="{value}"' for key, value in self.attributes.items())
        return f'<{self.tag}{class_attr}{style_attr} {other_attrs}>{self.content}</{self.tag}>'
