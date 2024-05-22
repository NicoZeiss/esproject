# Bienvenue sur le guide d'installation de l'app DoctoBill !



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

# Se rendre sur l'adresse locale
http://localhost:8000/
```
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