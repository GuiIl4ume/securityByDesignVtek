---
kanban-plugin: board
---

## Chef de projet

### Phase de cadrage
- [ ] Cadrer le sujet et définir le périmètre
- [ ] Définition des rôles et responsabilités
- [ ] Rédiger le cahier des charges
- [ ] Identifier les parties prenantes
- [ ] Définir les objectifs SMART du projet

### Planification
- [ ] Créer le Work Breakdown Structure (WBS)
- [ ] Élaborer le diagramme de Gantt
- [ ] Définir les ressources nécessaires (humaines, matérielles, budget)
- [ ] Identifier les risques projet
- [ ] Définir les KPI de suivi

### Suivi et communication
- [ ] Organiser les réunions d'équipe hebdomadaires
- [ ] Communication avec les parties prenantes
- [ ] Suivre l'avancement du projet
- [ ] Gérer les changements de périmètre
- [ ] Préparer les livrables et rapports


## Tech Lead

### Architecture
- [ ] Définir l'architecture 3-tiers complète
- [ ] Créer les schémas d'architecture (diagrammes)
- [ ] Valider l'architecture avec Security
- [ ] Documenter les choix techniques

### Choix technologiques
- [ ] Sélectionner les technologies pour le backend (API)
- [ ] Choisir la technologie frontend
- [ ] Sélectionner la base de données
- [ ] Choisir la solution de Message Queue (RabbitMQ/Kafka)
- [ ] Définir la stack du collecteur Python
- [ ] Veille technologique continue

### Gestion technique
- [ ] Définir les standards de code
- [ ] Créer la structure des repositories Git
- [ ] Définir les tâches de développement
- [ ] Communication avec le chef de projet (remontée)
- [ ] Communication avec l'équipe de dev (descendante)
- [ ] Code review des développements


## Security

### Analyse et conception
- [ ] Réaliser l'analyse de risques (threat modeling)
- [ ] Identifier les assets critiques
- [ ] Définir les exigences de sécurité
- [ ] Documenter les principes Security by Design appliqués

### Principes Security by Design
- [ ] Minimiser la surface d'attaque
- [ ] Implémenter "Secure by default"
- [ ] Appliquer le principe du moindre privilège
- [ ] Mettre en place la défense en profondeur
- [ ] Assurer "Fail secure"
- [ ] Implémenter le modèle Zero Trust
- [ ] Assurer la séparation des responsabilités
- [ ] Éviter la sécurité par obscurantisme

### Sécurité infrastructure
- [ ] Définir la segmentation réseau (VLAN, DMZ)
- [ ] Configurer le reverse proxy / WAF
- [ ] Mettre en place le système de gestion des secrets (Vault)
- [ ] Définir les règles de firewall
- [ ] Planifier les sauvegardes chiffrées

### Sécurité applicative
- [ ] Définir la politique d'authentification / autorisation (OAuth2, JWT)
- [ ] Implémenter le chiffrement TLS 1.3
- [ ] Configurer le chiffrement au repos
- [ ] Mettre en place la validation des entrées
- [ ] Définir la politique de gestion des logs
- [ ] Mettre en place une API Gateway

### Conformité et audit
- [ ] Vérifier la conformité RGPD
- [ ] Documenter les mesures de sécurité
- [ ] Préparer le plan de réponse aux incidents
- [ ] Définir les procédures de rotation des secrets


## Testeur

### Préparation des tests
- [ ] Créer le plan de test
- [ ] Définir les critères d'acceptation
- [ ] Préparer les jeux de données de test
- [ ] Mettre en place l'environnement de test

### Tests fonctionnels
- [ ] Tester les fonctions du collecteur Python
- [ ] Tester l'API backend (endpoints)
- [ ] Tester l'interface utilisateur
- [ ] Tester la Message Queue
- [ ] Tester les interactions avec la base de données

### Tests de sécurité
- [ ] S'informer sur les CVE des dépendances
- [ ] Tester l'authentification et autorisation
- [ ] Tester les injections (SQL, XSS, etc.)
- [ ] Tester le chiffrement des données
- [ ] Effectuer des tests de pénétration (pentest basique)

### Tests d'infrastructure
- [ ] Tester le déploiement
- [ ] Tester la segmentation réseau
- [ ] Vérifier la configuration du firewall
- [ ] Tester les sauvegardes et restaurations
- [ ] Tester la disponibilité et la résilience

### Reporting
- [ ] Documenter les bugs trouvés
- [ ] Informer l'équipe des problèmes
- [ ] Vérifier les corrections
- [ ] Générer les rapports de test




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false]}
```
%%