# VTEK - Collecte et affichage de données automobile

> Projet Security by Design - Application de collecte et comparaison de performances automobiles

## Description

![[architecture_devops.png]]
Application web permettant de collecter automatiquement des données sur des véhicules automobiles et de comparer leurs performances dans une interface unique, tout en garantissant l'intégrité, la disponibilité et la confidentialité des données.

## Architecture

- **Tier 1 - Présentation** : Interface web client
- **Tier 2 - Application** : API Backend, Collecteur Python, Message Queue
- **Tier 3 - Données** : Base de données sécurisée

## Équipe

- Guillaume A. : Sécurité
- Simon R. : Tech Lead
- Eric J. : Testeur
- Nicolas P. : Chef de projet

## Documentation

- `VTEK - WBS.md` : Documentation complète du projet (architecture, principes Security by Design, analyse des risques)
- `VTEK - Kanban.md` : Tableau Kanban avec les tâches par rôle
- `architecture.excalidraw.md` : Schéma d'architecture détaillé

## Contribuer au projet

### Prérequis

- Git installé sur votre machine
- Obsidian 1.10.1
	- Plugin Kanban. --> faire une migration vers tasknotes.
	- Plugin Excalidraw

### Cloner le projet

```bash
# Cloner le dépôt
git clone <URL_DU_DEPOT>

# Accéder au dossier du projet
cd exercice_VTEK
```

### Workflow de contribution

1. **Créer une branche pour votre tâche**
   ```bash
   git checkout -b feature/nom-de-votre-tache
   ```

2. **Effectuer vos modifications**
   - Consultez le Kanban pour voir les tâches disponibles
   - Mettez à jour les documents selon votre rôle

3. **Commiter vos changements**
   ```bash
   git add .
   git commit -m "Description claire de vos modifications"
   ```

4. **Pousser votre branche**
   ```bash
   git push origin feature/nom-de-votre-tache
   ```

5. **Créer une Pull Request**
   - Rendez-vous sur GitHub
   - Cliquez sur "Compare & pull request"
   - Décrivez vos modifications
   - Assignez un reviewer de l'équipe

### Bonnes pratiques

- Toujours travailler sur une branche dédiée
- Faire des commits réguliers avec des messages clairs
- Synchroniser régulièrement avec la branche principale :
  ```bash
  git pull origin main
  ```
- Demander une revue de code avant de merger

## Principes Security by Design

- Minimisation du périmètre (Zero Trust)
- Gestion sécurisée des secrets
- Sécurité des dépendances
- Chiffrement des données (transit & repos)
- Journalisation et détection
- Segmentation réseau

