from client import WordPressApiClient

class PagesEndpoint:
    def __init__(self, client: WordPressApiClient):
        self.client = client

    def create_page(self, title, content, status):
        """
        Crée une page dans WordPress.

        :param title: Le titre de la page.
        :param content: Le contenu HTML de la page.
        :param status: Le statut de publication (e.g., "publish", "draft").
        :return: La réponse de l'API WordPress.
        """
        page_data = {
            "title": title,
            "content": content,
            "status": status,
        }
        return self.client.create("pages", page_data)
    def get_page(self, page_id):
        print("id à récupérer ",page_id)
        """
        Récupère une page spécifique par son ID.
        
        :param page_id: L'ID de la page à récupérer.
        :return: Un dictionnaire avec le statut et les données de la page.
        """
        try:
            response = self.client.recup(f"pages/{page_id}")
            
            # Si la réponse est un dictionnaire de succès avec des données
            if response['status'] == 'success':
                return {
                    'status': 'success',
                    'data': response['data']
                }
            else:
                return {
                    'status': 'error',
                    'message': response.get('message', "Impossible de récupérer les détails de la page")
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def get_pages(self):
        """
        Récupère toutes les pages depuis WordPress.

        :return: La liste des pages ou la réponse brute de l'API.
        """
        return self.client.recup("pages")

    def update_page(self, page_id, title=None, content=None, status=None):
        """
        Met à jour une page existante.

        :param page_id: L'ID de la page à mettre à jour.
        :param title: (Optionnel) Le nouveau titre de la page.
        :param content: (Optionnel) Le nouveau contenu de la page.
        :param status: (Optionnel) Le nouveau statut de la page.
        :return: La réponse de l'API WordPress.
        """
        page_data = {}
        if title:
            page_data["title"] = title
        if content:
            page_data["content"] = content
        if status:
            page_data["status"] = status

        return self.client.update(f"pages/{page_id}", page_data)

    def delete_page(self, page_id, force=True):
        """
        Supprime une page existante.

        :param page_id: L'ID de la page à supprimer.
        :param force: Si True, la page est supprimée définitivement.
        :return: La réponse de l'API WordPress.
        """
        params = {"force": force}
        return self.client.delete(f"pages/{page_id}", params=params)
