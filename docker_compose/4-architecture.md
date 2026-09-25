# Architecture de la stack Docker Compose

Cette architecture correspond à la stack construite dans la tâche 2.

Elle contient cinq services :

- `proxy`
- `frontend`
- `api`
- `redis`
- `db`

## Vue d'ensemble

```text
Utilisateur / Navigateur
          |
          v
   localhost:8082
          |
          v
+-------------------+
|  proxy - Nginx    |
|  reverse proxy    |
+-------------------+
      |         |
      |         |
      |         +----------------------+
      |                                |
      v                                v
+-------------+                  +-------------+
|  frontend   |                  |     api     |
|   Nginx     |                  |    Flask    |
+-------------+                  +-------------+
                                      |     |
                                      |     |
                                      v     v
                                +---------+ +-------------+
                                |  Redis  | | PostgreSQL  |
                                |  cache  | |     db      |
                                +---------+ +-------------+
                                                  |
                                                  v
                                        +------------------+
                                        | postgres_data    |
                                        | Docker volume    |
                                        +------------------+
```

## Services

### proxy

Le service `proxy` utilise Nginx comme reverse proxy.

Son rôle est d'être la seule porte d'entrée publique de la stack.

Il est exposé sur :

```text
localhost:8082
```

Le proxy redirige les requêtes selon leur chemin :

```text
/       -> frontend
/api/   -> api
```

Le fichier `nginx.conf` contient les règles de routage.

### frontend

Le service `frontend` utilise Nginx pour servir le fichier `index.html`.

Il n'est pas directement exposé sur la machine hôte.

Il reçoit uniquement le trafic envoyé par le reverse proxy.

### api

Le service `api` exécute l'application Flask.

Il écoute sur le port `5000` à l'intérieur du réseau Docker.

Il peut communiquer avec :

- Redis avec le nom de service `redis`
- PostgreSQL avec le nom de service `db`

L'API attend que Redis et PostgreSQL soient disponibles avant de démarrer grâce à `depends_on` et aux healthchecks.

### redis

Le service `redis` utilise Redis comme cache.

Il permet à l'API de stocker temporairement des données rapides d'accès, par exemple le compteur de visites.

L'API se connecte à Redis avec :

```text
redis:6379
```

Redis n'est pas exposé directement vers la machine hôte.

### db

Le service `db` utilise PostgreSQL.

Il représente la base de données persistante de la stack.

L'API peut le joindre avec :

```text
db:5432
```

PostgreSQL utilise un healthcheck avec `pg_isready` afin de vérifier qu'il est prêt à accepter des connexions.

## Réseau Docker

Docker Compose crée automatiquement un réseau pour les services du projet.

Tous les services de la stack sont connectés à ce réseau par défaut :

```text
proxy
frontend
api
redis
db
```

Grâce à ce réseau, les conteneurs peuvent communiquer entre eux en utilisant directement le nom du service comme nom d'hôte.

Par exemple :

```text
proxy -> frontend:80
proxy -> api:5000
api -> redis:6379
api -> db:5432
```

Il n'est donc pas nécessaire d'utiliser des adresses IP fixes.

## Ports

Un seul service est exposé vers l'extérieur :

```text
proxy
```

Le mapping utilisé est :

```text
8082:80
```

Cela signifie :

```text
port 8082 de la machine
        |
        v
port 80 du conteneur proxy
```

Les autres services restent accessibles uniquement à l'intérieur du réseau Docker.

## Volumes

PostgreSQL utilise un volume Docker nommé :

```text
postgres_data
```

Ce volume est monté dans :

```text
/var/lib/postgresql/data
```

Il permet de conserver les données de la base même si le conteneur PostgreSQL est supprimé puis recréé.

```text
db container
     |
     v
/var/lib/postgresql/data
     |
     v
postgres_data
```

Le frontend et le proxy utilisent également des montages de fichiers pour accéder à :

```text
index.html
nginx.conf
```

Ces fichiers viennent directement du dossier du projet.

## Chemin d'une requête

### Requête vers le frontend

Lorsqu'un utilisateur ouvre :

```text
http://localhost:8082/
```

le chemin est :

```text
Navigateur
   |
   v
proxy
   |
   v
frontend
   |
   v
index.html
   |
   v
Navigateur
```

Le reverse proxy reçoit la requête puis la transmet au service `frontend`.

### Requête vers l'API

Lorsqu'un utilisateur appelle :

```text
http://localhost:8082/api/
```

le chemin est :

```text
Navigateur
   |
   v
proxy
   |
   v
api
   |
   +----> Redis
   |
   +----> PostgreSQL
   |
   v
proxy
   |
   v
Navigateur
```

Le proxy reçoit la requête `/api/` et l'envoie à l'API Flask.

L'API peut ensuite :

1. vérifier si la donnée existe dans Redis ;
2. utiliser la donnée du cache si elle existe ;
3. sinon interroger PostgreSQL ;
4. éventuellement stocker le résultat dans Redis ;
5. construire la réponse HTTP ;
6. renvoyer la réponse au proxy ;
7. le proxy renvoie finalement la réponse au navigateur.

## Résumé du flux complet

```text
Client
  |
  v
Reverse proxy Nginx
  |
  v
API Flask
  |
  +--> Redis
  |
  +--> PostgreSQL
          |
          v
     postgres_data
  |
  v
API Flask
  |
  v
Reverse proxy
  |
  v
Client
```

Cette architecture permet de séparer clairement les responsabilités :

- Nginx gère l'entrée et le routage ;
- le frontend gère l'affichage ;
- l'API gère la logique applicative ;
- Redis fournit un cache rapide ;
- PostgreSQL assure le stockage persistant.