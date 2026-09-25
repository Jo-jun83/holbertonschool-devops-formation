# Stack complète avec reverse proxy et cache Redis

Ce projet utilise Docker Compose pour lancer une stack complète composée de plusieurs services :

- un reverse proxy Nginx ;
- un frontend Nginx ;
- une API Flask ;
- un cache Redis ;
- une base de données PostgreSQL.

L'ensemble de la stack peut être démarré avec une seule commande.

## Architecture

Le trafic externe passe uniquement par le reverse proxy Nginx.

```text
Navigateur
   ↓
Reverse proxy Nginx
   ├── /       → frontend
   └── /api/   → API Flask
                      ├── Redis
                      └── PostgreSQL
```

Le reverse proxy permet d'utiliser une seule porte d'entrée pour accéder aux différents services.

Redis est utilisé comme cache et est accessible par l'API grâce au nom du service Docker Compose : `redis`.

## Services

### Proxy

Le service `proxy` utilise Nginx.

Il écoute sur le port `80` dans le conteneur et est accessible depuis la machine hôte sur :

```text
http://localhost:8082
```

Le fichier `nginx.conf` définit les routes :

- `/` vers le frontend ;
- `/api/` vers l'API.

### Frontend

Le service `frontend` utilise également Nginx pour servir le fichier `index.html`.

Il n'expose pas directement de port vers la machine hôte, car le trafic passe par le reverse proxy.

### API

L'API est une application Flask exécutée sur le port `5000`.

Elle utilise Redis via les variables d'environnement suivantes :

```yaml
REDIS_HOST: redis
REDIS_PORT: 6379
```

Le nom `redis` correspond au nom du service Docker Compose.

L'API attend également que PostgreSQL et Redis soient prêts avant de démarrer.

### Redis

Redis est utilisé comme service de cache.

Un healthcheck vérifie que Redis répond correctement :

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
```

Redis répond avec `PONG` lorsqu'il est prêt.

### PostgreSQL

PostgreSQL est utilisé comme base de données.

Un healthcheck basé sur `pg_isready` permet de vérifier que la base est prête à accepter des connexions.

Les données PostgreSQL sont conservées dans un volume nommé `postgres_data`.

## Lancer la stack

Depuis le dossier `2-full_stack`, exécuter :

```bash
docker compose up --build
```

Cette commande :

- construit l'image de l'API ;
- démarre PostgreSQL ;
- démarre Redis ;
- attend que les services nécessaires soient prêts ;
- démarre l'API ;
- démarre le frontend ;
- démarre le reverse proxy.

## Vérifier les services

Pour vérifier que tous les services sont lancés :

```bash
docker compose ps
```

Les services suivants doivent apparaître :

```text
proxy
frontend
api
redis
db
```

Redis et PostgreSQL doivent apparaître avec un état `healthy`.

## Tester le frontend

Ouvrir dans un navigateur :

```text
http://localhost:8082
```

La requête passe par le reverse proxy puis est envoyée vers le frontend.

## Tester l'API

L'API est accessible à travers le reverse proxy avec :

```bash
curl http://localhost:8082/api/
```

Une réponse similaire doit être retournée :

```json
{
  "message": "Hello from the API!",
  "visits": 1
}
```

À chaque nouvel appel, la valeur `visits` augmente car elle est stockée dans Redis.

Par exemple :

```json
{
  "message": "Hello from the API!",
  "visits": 2
}
```

Cela montre que l'API communique correctement avec Redis.

## Reverse proxy

Le fichier `nginx.conf` contient les règles de routage principales :

```nginx
location / {
    proxy_pass http://frontend:80;
}

location /api/ {
    proxy_pass http://api:5000/;
}
```

Cela permet d'utiliser une seule adresse publique pour accéder au frontend et à l'API.

## Arrêter la stack

Pour arrêter et supprimer les conteneurs :

```bash
docker compose down
```

Le volume PostgreSQL est conservé.

Pour supprimer également les volumes et les données :

```bash
docker compose down -v
```

## Conclusion

Cette stack montre comment Docker Compose permet de gérer plusieurs services ensemble.

Le reverse proxy Nginx fournit une porte d'entrée unique, Redis fournit un cache accessible par nom de service, et PostgreSQL assure le stockage persistant des données.

Toute la stack peut être lancée avec une seule commande :

```bash
docker compose up --build
```