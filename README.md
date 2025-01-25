wordpress_api_client/
│
├── wordpress_api_client/
│   ├── __init__.py                # Init du package
│   ├── client.py                  # Classe principale WordPressApiClient
│   ├── endpoints/
│   │   ├── __init__.py            # Init du module endpoints
│   │   ├── posts.py               # Gestion des posts
│   │   ├── users.py               # Gestion des utilisateurs
│   │   ├── categories.py          # Gestion des catégories
│   ├── auth.py                    # Gestion de l'authentification
│   ├── exceptions.py              # Définition des exceptions personnalisées
│   └── utils.py                   # Fonctions utilitaires (formatage, etc.)
│
├── tests/
│   ├── __init__.py
│   ├── test_client.py             # Tests pour WordPressApiClient
│   ├── test_endpoints.py          # Tests pour les endpoints
│
├── setup.py                       # Configuration du package Python
├── README.md                      # Documentation du projet
└── requirements.txt  