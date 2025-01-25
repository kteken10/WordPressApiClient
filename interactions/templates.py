from client import WordPressApiClient
from config import BASE_URL
from ui.button import Button
from endpoints.templates import ThemesEndpoint

# Création du client API et gestion du endpoint des templates

client = WordPressApiClient(base_url=BASE_URL)
templates_endpoint = ThemesEndpoint(client)

def create_template_with_user_buttons():
    """
    Crée un template en demandant à l'utilisateur combien de boutons il souhaite ajouter.
    """
    try:
        num_buttons = int(input("Combien de boutons souhaitez-vous ajouter au template ? "))
        if num_buttons <= 0:
            print("Le nombre de boutons doit être supérieur à zéro.")
            return
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Création du template initial
    template_response = templates_endpoint.create_template(
        name="template_blueprint",
        header_title="Compréhension écrite pro"
    )

    # Vérification de la réponse de création du template
    if template_response['status'] != "success":
        print(f"Erreur lors de la création du template : {template_response['message']}")
        return

    template_id = template_response['data']['id']
    print(f"Template créé avec succès! ID : {template_id}")

    # Récupération des informations pour les boutons
    buttons = []
    for i in range(num_buttons):
        label = input(f"Entrez le texte pour le bouton {i + 1} : ")
        link = input(f"Entrez le lien pour le bouton {i + 1} : ")
        styles = (
            "color: white; background-color: blue; padding: 10px 20px; text-decoration: none; "
            "border-radius: 5px; display: inline-block; margin: 5px;"
        )
        buttons.append(Button(label=label, link=link, styles=styles))

    # Mise à jour du template avec les boutons
    update_template_buttons(template_id, buttons)

def update_template_buttons(template_id, buttons):
    """
    Met à jour le contenu du template avec des boutons dynamiques.
    """
    containers = create_button_containers(buttons)
    content = f"<div>{''.join(containers)}</div>"

    # Mise à jour du template via l'API
    update_response = templates_endpoint.update_template(
        template_id=template_id,
        content=content
    )
    
    # Vérification de la réponse de mise à jour du template
    if update_response['status'] == "success":
        print(f"Template mis à jour avec succès! ID : {template_id}")
    else:
        print(f"Erreur lors de la mise à jour du template : {update_response['message']}")

def create_button_containers(buttons):
    """
    Organise les boutons en containers (3 boutons par ligne).
    """
    containers = []
    while buttons:
        num_in_container = min(3, len(buttons))  # 3 boutons maximum par ligne
        container_buttons = buttons[:num_in_container]
        buttons = buttons[num_in_container:]

        # Création de la structure HTML pour chaque ligne de boutons
        container_html = "<div style='display: flex; justify-content: space-around;'>"
        for button in container_buttons:
            container_html += button.render()
        container_html += "</div>"
        containers.append(container_html)

    return containers

def list_all_templates():
    """
    Liste tous les templates disponibles.
    """
    templates = templates_endpoint.get_all_templates()

    # Gestion de la réponse pour l'affichage des templates
    if templates['status'] == "success":
        print("Liste des templates disponibles :")
        for template in templates['data']:
            print(f"- ID : {template['id']}, Nom : {template['title']}")
    else:
        print(f"Erreur lors de la récupération des templates : {templates['message']}")
