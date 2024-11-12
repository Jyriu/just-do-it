# Just do IT : Un Forum Collaboratif pour les passionnés d'IT

Bienvenue sur **Just do IT**, un projet de forum collaboratif orienté autour de la communauté IT. Ce projet est actuellement en développement et vise à créer une plateforme où les utilisateurs peuvent partager des posts, demander de l'aide, échanger des conseils et participer à des discussions sur des thèmes liés à l'informatique.

## Fonctionnalités Actuelles
Voici une liste des fonctionnalités déjà implémentées ou en cours de développement :

- **Enregistrement et connexion des utilisateurs** : Chaque utilisateur peut créer un compte, se connecter et obtenir un jeton JWT pour l'authentification.
- **Création de posts** : Les utilisateurs peuvent créer des posts pour demander de l'aide, donner des conseils, ou démarrer des discussions sur des sujets précis.
- **Réponses aux posts** : Possibilité de répondre aux posts et d'avoir des discussions.
- **Pagination des posts** : Affichage des posts avec un système de pagination pour une meilleure navigation.
- **System de likes (en cours de développement)** : Les utilisateurs pourront aimer des posts et des réponses pour indiquer leur pertinence et popularité.
- **Statistiques et gamification** : Un système de points et de leaderboard est prévu pour encourager l’engagement et la qualité des contributions.

## Technologies Utilisées
- **Backend** : Flask (Python) avec SQLAlchemy pour la gestion de la base de données.
- **Base de données** : PostgreSQL, avec **Flask-Migrate** pour gérer les migrations de schéma.
- **Authentification** : JWT (JSON Web Tokens) pour gérer l’authentification et la sécurité des utilisateurs.
- **Frontend** : En préparation, le projet utilisera probablement **React** pour une interface utilisateur dynamique.

## Installation et Configuration
Si vous souhaitez contribuer ou tester ce projet en local, voici comment vous pouvez l'installer sur votre machine.

### Prérequis
- **Python 3.8+**
- **PostgreSQL** (configuré avec une base de données nommée `just_do_it_db`)
- **Node.js** (si le frontend est en cours de développement)

### Installation
1. Clonez le projet :
   ```sh
   git clone https://github.com/votre-utilisateur/just-do-it.git
   cd just-do-it/backend
   ```

2. Créez un environnement virtuel et activez-le :
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Sur Windows
   source venv/bin/activate # Sur MacOS/Linux
   ```

3. Installez les dépendances :
   ```sh
   pip install -r requirements.txt
   ```

4. Créez un fichier `.env` à la racine du projet backend avec les informations sensibles (par exemple, la chaîne de connexion à la base de données) :
   ```env
   DATABASE_URL=postgresql://username:password@localhost/just_do_it_db
   JWT_SECRET_KEY=votre-cle-secrete
   ```

5. Initialisez la base de données :
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. Lancez l’application :
   ```sh
   python app.py
   ```
   L’application devrait être accessible sur `http://127.0.0.1:5000`.

## Contribution
Pour l'instant il ne s'agit que d'un projet personnel ayant pour but l'apprentissage et la mise en pratique, cependant si le MVP est deployé et que des users sont intéressés alors les contributions seront les bienvenues ! Voici comment vous pourrez le faire :

- **Signaler des bugs** : Ouvrez une issue sur GitHub.
- **Proposer de nouvelles fonctionnalités** : Discutez d'une idée ou faites une suggestion en ouvrant une issue.
- **Envoyer une pull request** : Pour les nouvelles fonctionnalités ou corrections de bugs.

Merci de lire le fichier `CONTRIBUTING.md` (en construction) avant de soumettre vos contributions.

## Plan d'Évolution
Voici certaines des fonctionnalités planifiées pour un développement prochain :
- **Système de notification** : Pour avertir les utilisateurs des réponses ou des likes.
- **Gamification complète** : Leaderboard, niveaux, et badges pour gamification du forum.
- **Front-end dynamique** : Utilisation de **React** (à voir) pour l’interface utilisateur.

## Auteur
Ce projet est développé par @Jyriu (Sami YEZZA). Pour toute question, n'hésitez pas à me contacter sur GitHub.

## Licence
Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

