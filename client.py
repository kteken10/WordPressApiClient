import requests
from auth import get_auth

class WordPressApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.auth = get_auth()

    def create(self, endpoint, data):
        """
        Crée une ressource dans WordPress.
        """
        url = f"{self.base_url}/{endpoint}"
        print(f"Requête POST vers {url} avec les données : {data}")  # Debugging.
        response = requests.post(url, auth=self.auth, json=data)
        return self._handle_response(response)


    def recup(self, endpoint):
        """
        Récupère des ressources dans WordPress.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, auth=self.auth)
        return self._handle_response(response)

    def update(self, endpoint, data):
        """
        Met à jour une ressource dans WordPress (ex: une page).
        
        :param endpoint: L'endpoint de la ressource à mettre à jour (ex: "pages/1").
        :param data: Les données à mettre à jour (ex: titre ou contenu d'une page).
        :return: La réponse formatée de l'API.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, auth=self.auth, json=data)  # Utilisation de PUT pour mettre à jour
        return self._handle_response(response)

    def delete(self, endpoint, params=None):
        """
        Supprime une ressource dans WordPress.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, auth=self.auth, params=params)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Gère les réponses de l'API et retourne le JSON formaté ou un message d'erreur.
        """
        try:
            response_data = response.json()
            if response.ok:
                return {"status": "success", "data": response_data}
            else:
                return {"status": "error", "code": response.status_code, "message": response_data}
        except ValueError:
            return {"status": "error", "message": "Réponse JSON invalide", "raw_response": response.text}
