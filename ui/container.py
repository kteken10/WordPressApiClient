# container.py
from ui.element import HTMLElement

class Container(HTMLElement):
    def __init__(self, content: str = "", css_class: str = "", styles: str = "", children: list = None):
        """
        Initialisation du container (div).
        
        :param content: Le contenu HTML à inclure dans le div.
        :param css_class: La classe CSS à appliquer au div.
        :param styles: Les styles CSS en ligne à appliquer au div.
        :param children: Liste des éléments enfants (autres objets HTMLElement).
        """
        if children is None:
            children = []
         # Appliquer un margin-bottom de 20 par défaut, en combinant avec d'autres styles existants
        default_styles = "margin-bottom: 20px;"
        combined_styles = f"{default_styles} {styles}".strip()

        # Initialiser la balise div avec le contenu, la classe et les styles combinés
        super().__init__(tag="div", content=content, css_class=css_class, styles=combined_styles)    

        
        # Ajouter les enfants au container
        self.children = children

    def add_child(self, child: HTMLElement):
        """
        Ajouter un enfant à ce container.
        
        :param child: Un objet HTMLElement à ajouter comme enfant.
        """
        self.children.append(child)

    def render_children(self) -> str:
        """
        Générer le code HTML pour tous les enfants du container.
        
        :return: Le HTML de tous les enfants sous forme de chaîne.
        """
        return "".join([child.render() for child in self.children])

    def render(self) -> str:
        """
        Générer le code HTML complet du container, y compris les enfants.
        
        :return: Le HTML du container avec les enfants intégrés.
        """
        # Ajouter les enfants au contenu avant de générer le HTML
        self.content += self.render_children()
        
        # Appeler la méthode render() de la classe parente pour générer le HTML complet
        return super().render()
