# Première stack Docker Compose

Ce projet contient une petite stack Docker Compose composée de trois services :

- un frontend servi avec Nginx ;
- une API Python avec Flask ;
- une base de données PostgreSQL.

Docker Compose permet de lancer tous les services avec une seule commande.

## Prérequis

Docker et Docker Compose doivent être installés et Docker Desktop doit être démarré.

## Lancer la stack

Depuis le dossier `0-first_stack`, exécuter :

```bash
docker compose up --build
```

L'option `--build` permet de construire l'image de l'API avant de démarrer les conteneurs.

Une fois les services démarrés :

- le frontend est accessible sur :

```text
http://localhost:8081
```

- l'API est accessible sur :

```text
http://localhost:5000
```

## Vérifier les services

Pour vérifier que les trois services sont bien démarrés :

```bash
docker compose ps
```

Les services suivants doivent apparaître :

- `frontend`
- `api`
- `db`

Le service PostgreSQL utilise également un healthcheck afin de vérifier que la base de données est prête à accepter des connexions.

## Arrêter la stack

Pour arrêter et supprimer les conteneurs :

```bash
docker compose down
```

Le volume PostgreSQL est conservé, ce qui permet de garder les données entre deux exécutions.

Pour supprimer également les volumes et donc les données de la base :

```bash
docker compose down -v
```

## Relancer la stack

Pour relancer les services :

```bash
docker compose up
```

Si le code ou le Dockerfile a été modifié, il est préférable d'utiliser :

```bash
docker compose up --build
```