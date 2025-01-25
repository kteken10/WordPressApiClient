import json
import sqlite3
from client import WordPressApiClient
from config import BASE_URL
from endpoints.pages import PagesEndpoint
from ui.button import Button, ButtonContainer

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
    <h1 style="
        position: relative;
        text-align: center;
        font-size: 2.5rem;
    ">
        {title}
        <span style="
            content: '';
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 40%; 
            height: 2px;
            background-color: #2674F0;
            left: 0px;
        "></span>
        <span style="
            content: '';
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 40%; 
            height: 2px;
            background-color: #2674F0;
            right:0px;
        "></span>
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
        title="Compréhension écrite Pro ",
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

# Fonction pour ajouter, mettre à jour ou supprimer des boutons d'une page existante
def modify_existing_page():
    # Lister toutes les pages existantes
    list_all_pages()

    page_id = int(input("Entrez l'ID de la page à modifier : "))

    # Demander à l'utilisateur ce qu'il souhaite faire
    operation = input("\nQue souhaitez-vous faire ? (ajouter/mettre à jour/supprimer un bouton) : ").strip().lower()

    if operation == "ajouter":
        add_more_buttons(page_id, [])
    elif operation == "mettre à jour":
        add_more_buttons(page_id, [])
    elif operation == "supprimer":
        delete_button(page_id)
    else:
        print("Option invalide.")

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

def add_more_buttons(page_id, existing_buttons):
    # Demander combien de boutons ajouter
    num_buttons = int(input("Combien de boutons supplémentaires souhaitez-vous ajouter ? "))
    
    buttons = []
    for i in range(num_buttons):
        label = input(f"Entrez le label du bouton {i+1} : ")
        link = input(f"Entrez le lien pour le bouton {i+1} : ")
        
        # Ajouter le bouton à la liste
        buttons.append(Button(
            label=label,
            link=link,
            styles=""
        ))

    # Créer un container pour les nouveaux boutons avec un maximum de 3 boutons par ligne
    containers = ButtonContainer(existing_buttons + buttons)
    additional_content = containers.render()

    # Ajouter les boutons à la page existante
    page_content = f" {additional_content}"
    update_response = pages_endpoint.update_page(page_id, content=page_content)

    if update_response['status'] == "success":
        print(f"Les boutons ont été ajoutés avec succès à la page {page_id}")
    else:
        print(f"Erreur lors de l'ajout des boutons : {update_response['message']}")

# Fonction pour supprimer un bouton d'une page
def delete_button(page_id):
    button_id = int(input("Entrez l'ID du bouton à supprimer : "))
    
    # Suppression d'un bouton (logique à adapter selon la structure du client API)
    delete_response = pages_endpoint.delete_button_from_page(page_id, button_id)
    
    if delete_response['status'] == "success":
        print(f"Le bouton {button_id} a été supprimé de la page {page_id}")
    else:
        print(f"Erreur lors de la suppression du bouton : {delete_response['message']}")
        
# Lancer la création de la page avec des boutons
create_table()  # Crée la table si elle n'existe pas
