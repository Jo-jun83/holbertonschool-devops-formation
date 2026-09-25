# Docker Compose

Ce module montre comment décrire et exploiter une application composée de
plusieurs conteneurs dans un fichier `compose.yaml`. Les exercices font évoluer
une première stack vers une architecture avec contrôle de santé, cache,
stockage persistant et reverse proxy.

## Objectifs

- lancer plusieurs services avec une seule commande ;
- faire communiquer les conteneurs par leur nom de service ;
- contrôler l'ordre de démarrage avec des healthchecks ;
- monter des fichiers et conserver les données dans un volume ;
- centraliser l'accès à l'application avec un reverse proxy Nginx ;
- diagnostiquer une stack Compose incomplète ou incorrecte.

## Prérequis

- Docker installé et démarré ;
- Docker Compose v2, accessible avec `docker compose` ;
- `curl` ou un navigateur pour tester les services.

Vérifier l'installation :

```bash
docker --version
docker compose version
```

## Exercices

| Étape | Ressource | Contenu |
| ---: | --- | --- |
| 0 | [`0-first_stack`](./0-first_stack/) | frontend Nginx, API Flask et base PostgreSQL |
| 1 | [`1-healthchecks`](./1-healthchecks/) | attente de PostgreSQL avec `healthcheck` et `condition: service_healthy` |
| 2 | [`2-full_stack`](./2-full_stack/) | reverse proxy, frontend, API, Redis, PostgreSQL et volume persistant |
| 3 | [`3-fix_stack`](./3-fix_stack/) | exercice de diagnostic et de correction d'une stack |
| 4 | [`4-architecture.md`](./4-architecture.md) | documentation des services et du chemin suivi par les requêtes |

## Commandes courantes

Les commandes doivent être lancées dans le dossier contenant le fichier
`compose.yaml` :

```bash
docker compose up --build
docker compose ps
docker compose logs -f
docker compose config
docker compose down
```

- `up --build` construit les images locales et démarre les services ;
- `ps` affiche leur état ;
- `logs -f` suit leurs journaux ;
- `config` valide et affiche la configuration résolue ;
- `down` arrête et supprime les conteneurs et le réseau du projet.

Pour supprimer aussi les volumes et leurs données :

```bash
docker compose down -v
```

## Première stack

```bash
cd 0-first_stack
docker compose up --build
```

Une fois les services prêts :

- frontend : <http://localhost:8081> ;
- API : <http://localhost:5000> ;
- santé de l'API : <http://localhost:5000/health>.

La base PostgreSQL n'est pas publiée sur l'hôte : elle reste accessible aux
autres services sur le réseau Compose.

## Stack complète

Depuis `2-full_stack` :

```bash
docker compose up --build
```

La stack comprend cinq services :

```text
Navigateur
    |
    v
proxy Nginx :8082
    |-- /      --> frontend Nginx
    `-- /api/  --> API Flask
                       |--> Redis
                       `--> PostgreSQL --> volume postgres_data
```

Tester les deux routes exposées par le proxy :

```bash
curl http://localhost:8082/
curl http://localhost:8082/api/
```

Le proxy est la seule porte d'entrée publique de cette stack. Docker Compose
crée le réseau interne et fournit une résolution DNS basée sur les noms
`frontend`, `api`, `redis` et `db`.

## Healthchecks et dépendances

`depends_on` contrôle les dépendances de démarrage. Associé à
`condition: service_healthy`, il attend que le healthcheck du service dépendant
réussisse. Dans ces exercices :

- PostgreSQL est contrôlé avec `pg_isready` ;
- Redis est contrôlé avec `redis-cli ping` ;
- l'API démarre lorsque ses dépendances sont prêtes.

Pour observer les états et l'ordre de démarrage :

```bash
docker compose ps
docker compose logs db redis api
```

## Points de vigilance

- un conteneur démarré n'est pas nécessairement prêt à recevoir du trafic ;
- seuls les services devant être accessibles depuis l'hôte ont besoin de
  `ports` ;
- les services communiquent avec les ports internes, pas avec les ports publiés
  sur l'hôte ;
- les volumes nommés survivent à `docker compose down`, mais pas à
  `docker compose down -v` ;
- les identifiants présents dans ces fichiers sont destinés à un environnement
  pédagogique et ne doivent pas être réutilisés en production.
