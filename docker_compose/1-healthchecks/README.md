# Healthchecks avec Docker Compose

Ce projet montre comment utiliser un `healthcheck` avec Docker Compose afin de s'assurer que l'API ne démarre qu'une fois la base de données PostgreSQL réellement prête.

La stack contient trois services :

- un frontend servi avec Nginx ;
- une API Python avec Flask ;
- une base de données PostgreSQL.

## Problème

Lorsqu'une API et une base de données sont démarrées en même temps, l'API peut essayer de se connecter alors que PostgreSQL n'est pas encore prêt à accepter des connexions.

Le simple fait que le conteneur PostgreSQL soit démarré ne signifie pas forcément que la base est déjà disponible.

## Healthcheck PostgreSQL

Le service `db` utilise un healthcheck basé sur `pg_isready` :

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U jo -d test"]
  interval: 5s
  timeout: 5s
  retries: 5
```

La commande `pg_isready` vérifie que PostgreSQL est prêt à accepter des connexions.

Tant que ce test échoue, le service n'est pas considéré comme `healthy`.

## Dépendance de l'API

Le service `api` dépend du service `db` :

```yaml
depends_on:
  db:
    condition: service_healthy
```

Grâce à `condition: service_healthy`, Docker Compose attend que la base de données soit déclarée saine avant de démarrer l'API.

## Lancer les services

Depuis le dossier `1-healthchecks`, exécuter :

```bash
docker compose up --build
```

Docker Compose démarre PostgreSQL, exécute régulièrement son healthcheck, puis démarre l'API une fois la base déclarée `healthy`.

## Vérifier l'état des services

Pour vérifier l'état des conteneurs :

```bash
docker compose ps
```

Le service PostgreSQL doit apparaître avec un état similaire à :

```text
healthy
```

## Vérifier l'ordre de démarrage dans les logs

Les logs peuvent être affichés avec :

```bash
docker compose logs db api
```

On peut alors observer que PostgreSQL démarre d'abord et devient prêt à accepter des connexions avant le démarrage de l'API.

La base de données affiche notamment un message indiquant qu'elle est prête à accepter des connexions.

L'API démarre ensuite, car sa dépendance avec `condition: service_healthy` est satisfaite.

Cela évite que l'API tente de se connecter trop tôt à une base qui n'est pas encore prête.

## Arrêter les services

Pour arrêter et supprimer les conteneurs :

```bash
docker compose down
```

Les données PostgreSQL restent conservées si elles sont stockées dans un volume Docker.

Pour supprimer également les volumes :

```bash
docker compose down -v
```

## Conclusion

L'utilisation combinée de :

```yaml
healthcheck:
```

et :

```yaml
depends_on:
  db:
    condition: service_healthy
```

permet de contrôler proprement l'ordre de démarrage des services.

L'API attend que PostgreSQL soit réellement opérationnel avant de démarrer.