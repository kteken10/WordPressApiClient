from client import WordPressApiClient


class ThemesEndpoint:
    def __init__(self, client: WordPressApiClient):
        self.client = client

    def create_template(self, name, header_title):
        slug = name.lower().replace(" ", "-")
        payload = {
            "title": name,
            "slug": slug,
            "content": f"<h1>{header_title}</h1>",  # Contenu par défaut.
            "excerpt": "Résumé automatique",
            "status": "publish",
        }
        return self.client.create("elementor_library", payload)

    def update_template(self, template_id, content):
        """
        Met à jour le contenu du template existant via l'API WordPress.
        :param template_id: L'ID du template à mettre à jour.
        :param content: Le contenu HTML à insérer dans le template.
        :return: La réponse de l'API WordPress.
        """
        payload = {
            "content": content,  
        }
        return self.client.update(f"elementor_library/{template_id}", payload)

    def get_all_templates(self):
        return self.client.recup("elementor_library")
