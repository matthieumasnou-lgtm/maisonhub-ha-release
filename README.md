# Maison Hub — laboratoire Home Assistant

Application familiale auto-hébergée en cours de développement.

## État actuel

Version expérimentale : mur de messages local SQLite, réservé aux administrateurs Home Assistant via Ingress. **Ce n'est pas encore une messagerie familiale sécurisée.** Ne pas y enregistrer de données personnelles.

## Sécurité : conditions obligatoires avant ouverture familiale

- Aucun port direct publié vers le conteneur ; accès uniquement via Ingress.
- Pas de tunnel public direct vers le serveur, le NAS ou les caméras.
- Identités et permissions vérifiées côté serveur pour chaque lecture et écriture.
- Protection CSRF, limitation des requêtes, limites de taille et tests de contrôle d'accès.
- Stockage des médias privé : ne jamais publier les photos dans le partage SMB `Public` en clair.
- Sauvegardes chiffrées, restauration testée et mises à jour contrôlées.
- Audit des dépendances et des journaux avant chaque version ouverte aux proches.

## Modules existants envisagés

- **Nextcloud / Talk** : messagerie, appels, documents, calendrier.
- **Immich** : albums, photos et vidéos.
- **Home Assistant** : automatisations, annonces, équipements.

Ces modules ne sont **pas installés**. Leur intégration dépendra de la validation d'un hébergement isolé et de la RAM disponible sur le Pi 5.

## Installation

Dépôt de laboratoire, ne pas exposer au public. Le démarrage automatique reste désactivé tant que les contrôles de sécurité ne sont pas validés.
