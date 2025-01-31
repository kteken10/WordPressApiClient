from ui.element import HTMLElement

class Button(HTMLElement):
    def __init__(self, label: str, link: str, css_class: str = "", styles: str = "", target: str = "_self"):
        # Spécifie la largeur et le centrage pour chaque bouton
        button_styles = f"{styles} width: 320px; color: white; background-color: blue; padding: 10px 20px; text-decoration: none; border-radius: 30px; display: flex; justify-content: center; align-items: center; text-align: center; height: 50px;"
        super().__init__(tag="a", content=label, css_class=css_class, styles=button_styles, href=link, target=target)


class ButtonContainer(HTMLElement):
    def __init__(self, buttons: list[Button], styles: str = ""):
        self.buttons = buttons
        super().__init__(tag="div", styles=styles)

    def render(self) -> str:
        rows = []
        for i in range(0, len(self.buttons), 3):
            row_buttons = self.buttons[i:i + 3]
            row_content = "".join([button.render() for button in row_buttons])

            # Gestion de l'alignement pour une ou deux colonnes
            if len(row_buttons) == 1:
                row = f'<div style="display: flex; justify-content: center; margin: 20px auto; width: 1000px; align-items: center;">{row_content}</div>'
            elif len(row_buttons) == 2:
                row = f'<div style="display: flex; justify-content: space-between; margin: 20px auto; width: 1000px; align-items: center;">{row_content}</div>'
            else:
                # 3 boutons, alignés avec de l'espace entre eux
                row = f'<div style="display: flex; justify-content: space-between; margin: 20px auto; width: 1000px; align-items: center;">{row_content}</div>'

            rows.append(row)
        return "".join(rows)
