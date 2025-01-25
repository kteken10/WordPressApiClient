import json
from . import WordPressApiClient
from config import BASE_URL
from endpoints.posts import PostsEndpoint
from ui.button import Button, ButtonContainer

# Initialiser le client WordPress et l'endpoint des posts
client = WordPressApiClient(base_url=BASE_URL)
posts_endpoint = PostsEndpoint(client)

# Cas d'utilisation pour générer et publier des articles
def generate_and_publish_articles():
    try:
        max_buttons = int(input("Combien de boutons souhaitez-vous créer sur votre Post ? "))
        if max_buttons <= 0:
            print("Le nombre de boutons doit être supérieur à zéro.")
            return
        
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    for i in range(1, max_buttons + 1):
        buttons = [
            Button(
                label=f"Bouton {j}",
                link=f"https://example{j}.com",
                styles="color: white; background-color: blue; padding: 10px 20px; text-decoration: none;"
            )
            for j in range(1, i + 1)
        ]
        button_container = ButtonContainer(
            buttons=buttons, styles="margin: 20px auto;"
        )
        content = button_container.render()
        title = f"Article avec {i} Bouton{'s' if i > 1 else ''} Dynamiques"

        create_post_response = posts_endpoint.create_post(
            title=title,
            content=content,
            status="publish"
        )

        if create_post_response["status"] == "success":
            print(f"Article '{title}' publié avec succès !")
            print(content)
            print('\n')
        else:
            print(f"Erreur lors de la publication de l'article '{title}':")
            print(json.dumps(create_post_response, indent=4))
