

from interactions.pages import create_page_with_buttons


def main():
    print("Bienvenue dans l'application WordPress Page Manager!")
    while True:
        choix = input("\nQue souhaitez-vous faire ?\n1. Créer une nouvelle page avec des boutons\n2. Quitter\nVotre choix : ").strip()
        
        if choix == "1":
            create_page_with_buttons()  
        elif choix == "2":
            print("Merci d'avoir utilisé WordPress Page Manager. Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
