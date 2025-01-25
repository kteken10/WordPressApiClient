from ui.element import HTMLElement
from ui.container import Container

class Button(HTMLElement):
    def __init__(self, label: str, link: str, css_class: str = "", styles: str = "", target: str = "_self"):
        super().__init__(tag="a", content=label, css_class=css_class, styles=styles, href=link, target=target)

class ButtonContainer(HTMLElement):
    def __init__(self, buttons: list[Button], styles: str = ""):
        self.buttons = buttons
        super().__init__(tag="div", styles=styles)

    def render(self) -> str:
        rows = []
        for i in range(0, len(self.buttons), 3):
            row_buttons = self.buttons[i:i + 3]
            row = Container(
                content="".join([button.render() for button in row_buttons]),
                styles="display: flex; justify-content: space-between; margin-bottom: 20px;"
            )
            rows.append(row.render())
        return "".join(rows)
