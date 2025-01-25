from interactions.pages import create_page_with_buttons, delete_page, list_all_pages, modify_existing_page

def main():
    print("Bienvenue dans l'application WordPress Page Manager!")
    while True:
        choix = input("\nQue souhaitez-vous faire ?\n1. Créer une nouvelle page avec des boutons\n2. Modifier une page existante\n3. Supprimer une page\n4. Lister toutes les pages disponibles\n5. Quitter\nVotre choix : ").strip()

        if choix == "1":
            create_page_with_buttons()  
        elif choix == "2":
            modify_existing_page()
        elif choix == "3":
            delete_page()  
        elif choix == "4":
            list_all_pages()  
        elif choix == "5":
            print("Merci d'avoir utilisé WordPress Page Manager. Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":  
    main()
