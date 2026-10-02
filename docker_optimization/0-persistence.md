# 1. Lancer un conteneur Postgres avec un volume nommé
docker run -d --name pg_container -e POSTGRES_PASSWORD=mysecret -v pg_data:/var/lib/postgresql/data postgres

# 2. Vérifier qu'il tourne
docker ps

# 3. Se connecter à Postgres et écrire une donnée
docker exec -it pg_container psql -U postgres -c "CREATE TABLE test (msg TEXT);"
docker exec -it pg_container psql -U postgres -c "INSERT INTO test (msg) VALUES ('hello persistence');"

# 4. Vérifier que la donnée est bien là (avant destruction)
docker exec -it pg_container psql -U postgres -c "SELECT * FROM test;"

# 5. Détruire complètement le conteneur
docker stop pg_container
docker rm pg_container

# 6. Confirmer que le conteneur a disparu, mais que le volume existe toujours
docker ps -a
docker volume ls

# 7. Recréer un NOUVEAU conteneur, branché sur le MÊME volume nommé
docker run -d --name pg_container_new -e POSTGRES_PASSWORD=mysecret -v pg_data:/var/lib/postgresql/data postgres

# 8. Vérifier que la donnée écrite avant est toujours présente
docker exec -it pg_container_new psql -U postgres -c "SELECT * FROM test;"