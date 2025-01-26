import sqlite3
from client import WordPressApiClient
from config import BASE_URL
from endpoints.pages import PagesEndpoint
from ui.button import Button, ButtonContainer
import re

# Initialiser le client WordPress et l'endpoint des pages
client = WordPressApiClient(base_url=BASE_URL)
pages_endpoint = PagesEndpoint(client)

# Fonction pour se connecter à la base de données SQLite
def connect_to_db():
    conn = sqlite3.connect('pages.db')
    return conn

# Fonction pour créer la table si elle n'existe pas
def create_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Fonction pour enregistrer une page dans la base de données
def save_page_to_db(page_id, title, content):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pages (id, title, content) VALUES (?, ?, ?)", (page_id, title, content))
    conn.commit()
    conn.close()

# Fonction pour créer la page initiale avec des boutons
def create_page_with_buttons():
    # Demander à l'utilisateur le titre de la page
    title = input("Entrez le titre de la page à créer: ")

    # Ajouter le style personnalisé pour le titre
    content = f"""
    <h1 style="position: relative; text-align: center; font-size: 2.5rem;">
        {title}
        <span style="position: absolute; top: 50%; transform: translateY(-50%); width: 40%; height: 2px; background-color: #2674F0; left: 0px;"></span>
        <span style="position: absolute; top: 50%; transform: translateY(-50%); width: 40%; height: 2px; background-color: #2674F0; right:0px;"></span>
    </h1>
    """

    # Demander à l'utilisateur combien de boutons il veut publier
    try:
        num_buttons = int(input("Combien de boutons souhaitez-vous ajouter à la page ? "))
        if num_buttons <= 0:
            print("Le nombre de boutons doit être supérieur à zéro.")
            return
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Demander si l'utilisateur veut définir les labels et styles pour chaque bouton
    define_custom_labels = input("Souhaitez-vous définir le label pour chaque bouton ? (oui/non) : ").strip().lower()

    buttons = []
    for i in range(num_buttons):
        if define_custom_labels == 'oui':
            label = input(f"Entrez le label du bouton {i+1} : ")
        else:
            label = f"Compréhension Ecrite Série {i + 1}"

        link = input(f"Entrez le lien pour le bouton {i+1} : ")

        # Ajouter le bouton à la liste
        buttons.append(Button(
            label=label,
            link=link,
            styles=""
        ))

    # Créer un container pour les boutons avec un maximum de 3 boutons par ligne
    containers = ButtonContainer(buttons)
    content += containers.render()

    # Créer la page initiale avec ces boutons
    create_response = pages_endpoint.create_page(
        title="Compréhension écrite Pro",
        content=content,
        status="publish"
    )
    if create_response['status'] == "success":
        page_id = create_response['data']['id']
        print(f"Page créée avec succès! ID de la page : {page_id}")

        # Sauvegarder la page dans la base de données
        save_page_to_db(page_id, title, content)

        # Demander à l'utilisateur s'il souhaite ajouter encore des boutons
        add_more_buttons(page_id, buttons)  # Passer l'ID de la page créée
    else:
        print(f"Erreur lors de la création de la page: {create_response['message']}")

# Fonction pour lister toutes les pages disponibles
def list_all_pages():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM pages")
    pages = cursor.fetchall()

    if pages:
        print("\nPages disponibles :")
        for page in pages:
            print(f"ID: {page[0]} | Titre: {page[1]}")
    else:
        print("Aucune page disponible.")
    conn.close()

# Fonction pour ajouter, mettre à jour ou supprimer des boutons d'une page existante
def modify_existing_page():
    # Lister toutes les pages existantes
    list_all_pages()

    page_id = int(input("Entrez l'ID de la page à modifier : "))

    # Demander à l'utilisateur ce qu'il souhaite faire
    operation = input("\nQue souhaitez-vous faire ? (a pour ajouter / m pour mettre à jour un bouton / s pour supprimer un bouton) : ").strip().lower()

    if operation == "a":
        add_more_buttons(page_id, [])
    elif operation == "m":
        update_button(page_id)
    elif operation == "s":
        delete_button(page_id)
    else:
        print("Option invalide.")

# Fonction pour ajouter plus de boutons à une page existante
def add_more_buttons(page_id, existing_buttons):
    # Récupérer le contenu existant de la page
    page_response = pages_endpoint.get_page(page_id)
    
    if page_response['status'] != "success":
        print(f"Erreur lors de la récupération de la page : {page_response['message']}")
        return

    # Récupérer le contenu rendu de la page
    existing_content = page_response['data']['content']
    
    # Extraire les boutons existants
    existing_buttons = extract_existing_buttons(existing_content)
    
    # Demander combien de boutons ajouter
    try:
        num_buttons = int(input("Combien de boutons supplémentaires souhaitez-vous ajouter ? "))
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Ajouter de nouveaux boutons
    for i in range(num_buttons):
        label = input(f"Entrez le label du bouton {i+1} : ")
        link = input(f"Entrez le lien pour le bouton {i+1} : ")
        
        existing_buttons.append(Button(
            label=label,
            link=link,
            styles=""
        ))

    # Créer un container pour tous les boutons avec un maximum de 3 boutons par ligne
    containers = ButtonContainer(existing_buttons)
    updated_content = containers.render()

    # Mettre à jour la page avec le nouveau contenu
    update_response = pages_endpoint.update_page(page_id, content=updated_content)

    if update_response['status'] == "success":
        print(f"Les boutons ont été ajoutés avec succès à la page {page_id}")
    else:
        print(f"Erreur lors de l'ajout des boutons : {update_response['message']}")

# Fonction pour mettre à jour un bouton existant
def update_button(page_id):
    # Récupérer le contenu de la page existante
    page_response = pages_endpoint.get_page(page_id)
    
    if page_response['status'] != "success":
        print(f"Erreur lors de la récupération de la page : {page_response['message']}")
        return

    existing_content = page_response['data']['content']
    buttons = extract_existing_buttons(existing_content)
    
    if not buttons:
        print("Aucun bouton n'a été trouvé sur cette page.")
        return

    # Lister les boutons disponibles
    print("\nBoutons disponibles sur la page :")
    for i, button in enumerate(buttons):
        print(f"{i + 1}. Label : {button.label}, Lien : {button.link}")

    # Demander à l'utilisateur quel bouton modifier
    try:
        button_index = int(input("Entrez le numéro du bouton à modifier : ")) - 1
        if button_index < 0 or button_index >= len(buttons):
            print("Numéro invalide.")
            return
    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return

    # Demander les nouvelles informations pour le bouton sélectionné
    new_label = input("Entrez le nouveau label du bouton : ")
    new_link = input("Entrez le nouveau lien du bouton : ")

    # Mettre à jour le bouton dans le contenu HTML
    button_to_update = buttons[button_index]
    updated_content = re.sub(
        rf'<a[^>]*href="{re.escape(button_to_update.link)}"[^>]*>{re.escape(button_to_update.label)}<\/a>',
        f'<a href="{new_link}">{new_label}</a>',
        existing_content
    )

    # Mettre à jour la page avec le nouveau contenu
    update_response = pages_endpoint.update_page(page_id, content=updated_content)

    if update_response['status'] == "success":
        print(f"Le bouton a été mis à jour avec succès!")
    else:
        print(f"Erreur lors de la mise à jour du bouton : {update_response['message']}")

#Fonction pour supprimer un bouton d'une page
def delete_button(page_id):
    # Récupérer le contenu de la page existante
    page_response = pages_endpoint.get_page(page_id)
    
    if page_response['status'] != "success":
        print(f"Erreur lors de la récupération de la page : {page_response['message']}")
        return

    existing_content = page_response['data']['content']['rendered']

    # Extraire les boutons existants
    import re
    button_pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
    buttons = []
    
    for match in re.finditer(button_pattern, existing_content):
        link, label = match.groups()
        buttons.append({'link': link, 'label': label})

    if not buttons:
        print("Aucun bouton n'a été trouvé sur cette page.")
        return

    # Lister les boutons disponibles
    print("\nBoutons disponibles sur la page :")
    for i, button in enumerate(buttons):
        print(f"{i + 1}. Label : {button['label']}, Lien : {button['link']}")

    # Demander à l'utilisateur quel bouton supprimer
    try:
        button_index = int(input("Entrez le numéro du bouton à supprimer : ")) - 1
        if button_index < 0 or button_index >= len(buttons):
            print("Numéro invalide.")
            return
    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return

    # Supprimer le bouton du contenu
    button_to_remove = buttons[button_index]
    updated_content = re.sub(
        rf'<a[^>]*href="{re.escape(button_to_remove["link"])}"[^>]*>{re.escape(button_to_remove["label"])}</a>',
        '',
        existing_content
    )

    # Mettre à jour la page avec le nouveau contenu
    update_response = pages_endpoint.update_page(page_id, content=updated_content)

    if update_response['status'] == "success":
        print(f"Le bouton '{button_to_remove['label']}' a été supprimé avec succès de la page {page_id}.")
    else:
        print(f"Erreur lors de la mise à jour de la page : {update_response['message']}")

# Fonction pour supprimer une page
def delete_page():
    page_id = int(input("Entrez l'ID de la page à supprimer : "))

    # Supprimer la page
    delete_response = pages_endpoint.delete_page(page_id)
    
    if delete_response['status'] == "success":
        print(f"Page {page_id} supprimée avec succès!")
        
        # Supprimer de la base de données
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pages WHERE id = ?", (page_id,))
        conn.commit()
        conn.close()
    else:
        print(f"Erreur lors de la suppression de la page: {delete_response['message']}")
    
def extract_existing_buttons(content):
        # Vérifier si content est un dictionnaire avec 'rendered'
        if isinstance(content, dict):
            content = content.get('rendered', '')
        
        # Convertir en chaîne si ce n'est pas déjà le cas
        content = str(content)
        
        # Chercher tous les boutons existants dans le contenu HTML
        button_pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        buttons = []
        
        for match in re.finditer(button_pattern, content):
            link, label = match.groups()
            buttons.append(Button(
                label=label,
                link=link,
                styles=""
            ))
        
        return buttons

create_table()