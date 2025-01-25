# image.py
from ui.element import HTMLElement

class Image(HTMLElement):
    def __init__(self, src: str, alt: str = "", css_class: str = "", styles: str = ""):
        content = f'<img src="{src}" alt="{alt}" />'
        super().__init__(tag="img", content=content, css_class=css_class, styles=styles)

    def render(self) -> str:
        return super().render()
