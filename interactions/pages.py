import json
from client import WordPressApiClient
from config import BASE_URL
from endpoints.pages import PagesEndpoint
from ui.button import Button, ButtonContainer

# Initialiser le client WordPress et l'endpoint des pages
client = WordPressApiClient(base_url=BASE_URL)
pages_endpoint = PagesEndpoint(client)

# Fonction pour créer la page initiale avec des boutons
def create_page_with_buttons():
    # Demander à l'utilisateur combien de boutons il veut publier
    try:
        num_buttons = int(input("Combien de boutons souhaitez-vous ajouter à la page ? "))
        if num_buttons <= 0:
            print("Le nombre de boutons doit être supérieur à zéro.")
            return
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Créer les boutons dynamiquement
    buttons = [
        Button(
            label=f"Compréhension écrite Série {i + 1}",
            link=f"https://example{i + 1}.com",
            styles="color: white; background-color: blue; padding: 10px 20px; text-decoration: none; border-radius: 30px;"
        )
        for i in range(num_buttons)
    ]

    # Créer un container pour les boutons
    containers = ButtonContainer(buttons)
    content = containers.render()

    # Créer la page initiale avec ces boutons
    create_response = pages_endpoint.create_page(
        title="Compréhension écrite Pro",
        content=content,
        status="publish"
    )
    if create_response['status'] == "success":
        page_id = create_response['data']['id']
        print(f"Page créée avec succès! ID de la page : {page_id}")

        # Demander à l'utilisateur s'il souhaite ajouter encore des boutons
        add_more_buttons(page_id, buttons)  # Passer l'ID de la page créée
    else:
        print(f"Erreur lors de la création de la page: {create_response['message']}")

# Fonction pour ajouter, mettre à jour ou supprimer des boutons d'une page existante
def add_more_buttons(page_id, existing_buttons):
    while True:
        operation = input("\nQue souhaitez-vous faire ? (ajouter/mettre à jour/supprimer/fin) : ").strip().lower()

        if operation == "ajouter":
            try:
                num_new_buttons = int(input("Combien de nouveaux boutons souhaitez-vous ajouter ? "))
                if num_new_buttons <= 0:
                    print("Le nombre de boutons doit être supérieur à zéro.")
                    continue
            except ValueError:
                print("Veuillez entrer un nombre valide.")
                continue

            # Ajouter les nouveaux boutons
            new_buttons = [
                Button(
                    label=f"Bouton {len(existing_buttons) + i + 1}",
                    link=f"https://example{len(existing_buttons) + i + 1}.com",
                    styles="color: white; background-color: blue; padding: 10px 20px; text-decoration: none; border-radius: 30px;"
                )
                for i in range(num_new_buttons)
            ]
            existing_buttons.extend(new_buttons)

        elif operation == "mettre à jour":
            if not update_button(existing_buttons):
                continue

        elif operation == "supprimer":
            if not delete_button(existing_buttons):
                continue

        elif operation == "fin":
            print("Aucune modification supplémentaire effectuée.")
            break

        else:
            print("Réponse invalide. Veuillez répondre par 'ajouter', 'mettre à jour', 'supprimer' ou 'fin'.")

        # Mettre à jour la page avec les modifications
        containers = ButtonContainer(existing_buttons)
        new_content = containers.render()
        update_response = pages_endpoint.update_page(page_id=page_id, content=new_content)

        if update_response['status'] == "success":
            print(f"Page mise à jour avec succès! ID de la page : {page_id}")
        else:
            print(f"Erreur lors de la mise à jour de la page: {update_response['message']}")

# Fonction pour mettre à jour un bouton existant
def update_button(existing_buttons):
    try:
        print("\nListe des boutons existants :")
        for index, button in enumerate(existing_buttons):
            print(f"{index + 1}. {button.label} - {button.link}")

        button_index = int(input("\nQuel bouton souhaitez-vous mettre à jour ? (Entrez le numéro) ")) - 1

        if 0 <= button_index < len(existing_buttons):
            button = existing_buttons[button_index]
            button.label = input(f"Nouveau texte du bouton (actuel: {button.label}): ") or button.label
            button.link = input(f"Nouveau lien du bouton (actuel: {button.link}): ") or button.link
            button.styles = input(f"Nouveaux styles CSS (actuel: {button.styles}): ") or button.styles
            print("Le bouton a été mis à jour avec succès.")
            return True
        else:
            print("Index invalide.")
            return False
    except ValueError:
        print("Entrée invalide.")
        return False

# Fonction pour supprimer un bouton
def delete_button(existing_buttons):
    try:
        print("\nListe des boutons existants :")
        for index, button in enumerate(existing_buttons):
            print(f"{index + 1}. {button.label} - {button.link}")

        button_index = int(input("\nQuel bouton souhaitez-vous supprimer ? (Entrez le numéro) ")) - 1

        if 0 <= button_index < len(existing_buttons):
            deleted_button = existing_buttons.pop(button_index)
            print(f"Bouton '{deleted_button.label}' supprimé avec succès.")
            return True
        else:
            print("Index invalide.")
            return False
    except ValueError:
        print("Entrée invalide.")
        return False

# Lancer la création de la page avec des boutons
create_page_with_buttons()
