# text.py
from ui.element import HTMLElement

class Text(HTMLElement):
    def __init__(self, content: str, css_class: str = "", styles: str = ""):
        super().__init__(tag="p", content=content, css_class=css_class, styles=styles)

    def render(self) -> str:
        return super().render()  
