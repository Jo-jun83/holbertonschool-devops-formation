# Fondamentaux de Docker

Ce module introduit les principales commandes Docker, la création d'images et
le diagnostic de Dockerfiles pour des applications Python et Node.js.

## Objectifs

- récupérer une image depuis un registre ;
- créer, démarrer, inspecter, arrêter et supprimer un conteneur ;
- publier un port entre un conteneur et la machine hôte ;
- construire une image à partir d'un Dockerfile ;
- corriger les erreurs fréquentes de conteneurisation ;
- transmettre et inspecter des variables d'environnement.

## Prérequis

- Docker installé ;
- le démon Docker ou Docker Desktop démarré ;
- `curl` pour tester les applications HTTP.

Vérifier l'installation :

```bash
docker --version
docker info
```

## Exercices

| Étape | Ressource | Contenu |
| ---: | --- | --- |
| 0 | [`0-first_container.md`](./0-first_container.md) | lancement d'un serveur Nginx, publication d'un port, shell, logs et nettoyage |
| 1 | [`1-first-image`](./1-first-image/) | première image d'une application HTTP Python sans dépendance externe |
| 2 | [`2-fix_flask`](./2-fix_flask/) | Dockerfile corrigé pour une application Flask |
| 3 | [`3-fix_express`](./3-fix_express/) | Dockerfile corrigé pour une application Express |
| 4 | [`4-interact.md`](./4-interact.md) | interaction avec un conteneur et étude des variables d'environnement |

## Commandes essentielles

### Manipuler un conteneur

```bash
docker pull nginx
docker run -d --name my_nginx -p 8081:80 nginx
docker ps
docker logs my_nginx
docker exec -it my_nginx sh
docker stop my_nginx
docker rm my_nginx
```

Le mapping `8081:80` relie le port `8081` de la machine au port `80` du
conteneur.

### Construire et tester la première image

```bash
cd 1-first-image
docker build -t first-image .
docker run -d --name first_image_container -p 8082:5000 first-image
curl http://localhost:8082
```

Réponse attendue :

```text
Hello from my first Docker image!
```

Nettoyer ensuite le conteneur :

```bash
docker stop first_image_container
docker rm first_image_container
```

## Applications de débogage

### Flask

```bash
cd 2-fix_flask
docker build -t flask-debug .
docker run --rm -p 5000:5000 flask-debug
```

Dans un autre terminal :

```bash
curl http://localhost:5000
```

### Express

```bash
cd 3-fix_express
docker build -t express-debug .
docker run --rm -p 3001:3001 express-debug
```

Dans un autre terminal :

```bash
curl http://localhost:3001
```

## Bonnes pratiques illustrées

- choisir une image de base adaptée et légère ;
- définir un `WORKDIR` explicite ;
- copier et installer les dépendances avant le code pour profiter du cache de
  construction ;
- utiliser la forme JSON de `CMD` ;
- écouter sur `0.0.0.0` pour rendre l'application joignable hors du conteneur ;
- distinguer `EXPOSE`, qui documente un port, de `-p`, qui le publie réellement ;
- utiliser `--rm` pour les conteneurs de test temporaires.
