# Formation DevOps — Holberton School

Ce dépôt rassemble les exercices réalisés autour de la culture DevOps, de Git,
de Docker et de Docker Compose. Le parcours commence par les pratiques de
collaboration et d'amélioration continue, puis progresse vers la création
d'images et l'orchestration d'applications composées de plusieurs services.

## Contenu du dépôt

| Module | Notions abordées |
| --- | --- |
| [`devops_culture_git`](./devops_culture_git/) | environnement de travail, pull requests, conflits Git, métriques DORA, post-mortem et Conventional Commits |
| [`docker_fundamentals`](./docker_fundamentals/) | cycle de vie d'un conteneur, création d'images, débogage de Dockerfiles et variables d'environnement |
| [`docker_compose`](./docker_compose/) | stacks multi-conteneurs, healthchecks, dépendances, réseaux, volumes, Redis, PostgreSQL et reverse proxy Nginx |

Chaque module possède son propre README avec le détail des exercices et les
commandes utiles.

## Prérequis

Pour réaliser l'ensemble du parcours, il faut disposer de :

- Git ;
- Docker avec la commande `docker compose` ;
- Bash ou Git Bash pour exécuter les scripts shell ;
- Python 3 et Node.js pour lancer certains exemples hors conteneur.

Vérifier les versions installées :

```bash
git --version
docker --version
docker compose version
python3 --version
node --version
```

Sous Windows, Docker Desktop doit être démarré avant l'utilisation des
conteneurs.

## Parcours conseillé

1. Commencer par [`devops_culture_git`](./devops_culture_git/) pour revoir les
   pratiques de collaboration et les indicateurs DevOps.
2. Continuer avec [`docker_fundamentals`](./docker_fundamentals/) pour manipuler
   des conteneurs et construire ses premières images.
3. Terminer avec [`docker_compose`](./docker_compose/) pour assembler et faire
   communiquer plusieurs services.

## Démarrage rapide

Cloner le dépôt puis entrer dans le module souhaité :

```bash
git clone <URL_DU_DEPOT>
cd holbertonschool-devops-formation
cd docker_fundamentals
```

Les applications Docker Compose se lancent depuis le dossier de l'exercice
concerné. Par exemple :

```bash
cd docker_compose/2-full_stack
docker compose up --build
```

Pour arrêter la stack :

```bash
docker compose down
```

> La commande `docker compose down -v` supprime également les volumes et les
> données persistantes associées.

## Objectifs pédagogiques

À l'issue de ces exercices, l'apprenant doit être capable de :

- collaborer avec Git à l'aide de branches et de pull requests ;
- résoudre un conflit de fusion et documenter un incident sans rechercher de
  responsable individuel ;
- expliquer les métriques DORA et les principes CALMS ;
- construire, exécuter, inspecter et dépanner une image Docker ;
- orchestrer une application multi-services avec Docker Compose ;
- configurer des healthchecks, des dépendances, des volumes et un reverse
  proxy.
