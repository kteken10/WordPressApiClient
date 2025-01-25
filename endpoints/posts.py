from client import WordPressApiClient


class PostsEndpoint:
    def __init__(self, client: WordPressApiClient):
        self.client = client

    def create_post(self, title, content, status):
        """
        Crée un nouvel article dans WordPress.

        :param title: Le titre de l'article.
        :param content: Le contenu HTML de l'article.
        :param status: Le statut de publication (e.g., "publish", "draft").
        :return: La réponse de l'API WordPress.
        """
        post_data = {
            "title": title,
            "content": content,
            "status": status,
        }
        return self.client.create("posts", post_data)

    def get_posts(self):
        """
        Récupère tous les articles depuis WordPress.

        :return: La liste des articles ou la réponse brute de l'API.
        """
        return self.client.recup("posts")

    def update_post(self, post_id, title=None, content=None, status=None):
        """
        Met à jour un article existant.

        :param post_id: L'ID de l'article à mettre à jour.
        :param title: (Optionnel) Le nouveau titre de l'article.
        :param content: (Optionnel) Le nouveau contenu de l'article.
        :param status: (Optionnel) Le nouveau statut de l'article.
        :return: La réponse de l'API WordPress.
        """
        post_data = {}
        if title:
            post_data["title"] = title
        if content:
            post_data["content"] = content
        if status:
            post_data["status"] = status

        return self.client.update(f"posts/{post_id}", post_data)

    def delete_post(self, post_id, force=True):
        """
        Supprime un article existant.

        :param post_id: L'ID de l'article à supprimer.
        :param force: Si True, l'article est supprimé définitivement.
        :return: La réponse de l'API WordPress.
        """
        params = {"force": force}
        return self.client.delete(f"posts/{post_id}", params=params)
