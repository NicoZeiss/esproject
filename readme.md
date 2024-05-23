# Bienvenue sur le guide d'installation de l'app DoctoBill !

## Prérequis
Sur Windows, avoir téléchargé et activé le WSL2.
Avoir installé Git.
Avoir installé Docker, Docker Compose et Docker Desktop.
[Aide à l'installation](https://docs.docker.com/compose/install/)

## Récupération du projet
[Repository du projet](https://github.com/NicoZeiss/esproject)
```bash
# Cloner le projet
git clone https://github.com/NicoZeiss/esproject.git

# Créer un fhichier environments/required.env à la racine du projet
mkdir environments
touch environments/required.env

# Ajouter les variables d'environnements dans required.env
POSTGRES_DB=[NOM_DE_LA_DATABASE_POSTGRESQL] 
POSTGRES_USER=[NOM_DU_USER_POSTGRESQL]
POSTGRES_PASSWORD=[PASSWORD_DU_USER_POSTGRESQL]
POSTGRES_HOST=db 
  
DJANGO_SECRET_KEY=[SECRET_KEY_DE_DJANGO]
# La clé secrête de Django n'a pas besoin d'être sécurisée 
# pour un lancement de serveur en local
```

## Initialisation du projet
```bash
# Création des containers
docker-compose up -d

# Migration de la BDD
docker-compose exec web python manage.py migrate

# Il n'est pas nécessaire de créer un superuser 
# Je n'ai pas intégré de fonctionnalités dans le panel admin

# Création de 5000 patients en BDD
docker-compose exec web python manage.py create_patients
```
**Se rendre sur l'adresse locale pour vérifier que tout fonctionne :**
<http://localhost:8000/>
## Créer un médecin
1. Cliquer sur *"Pas encore de compte ?"*
2. Cliquer sur *"Un médecin"*
3. Remplir le formulaire
4. Cliquer sur *"S'inscrire"*

## Créer un patient
1. Cliquer sur *"Pas encore de compte ?"*
2. Cliquer sur *"Un patient"*
3. Remplir le formulaire
4. Cliquer sur *"S'inscrire"*

*A noter que les médecins peuvent aussi créer des patients depuis leur espace personnel.*

## Fonctionnalités
### Médecin
- Consulter la liste des consultations qui lui sont rattachées
- Créer des consultations
- Modifier des consultations
- Supprimer des consultations
- Consulter la liste des patients
- Recherche un patient
- Créer des patients
- Modifier des patients
- Supprimer des patients

### Patient
- Consulter la liste de ses consultations
- Consulter ses données personnelles