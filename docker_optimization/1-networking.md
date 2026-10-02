# 1. Créer un réseau Docker custom 
docker network create mon_reseau

# 2. Lancer un premier conteneur sur ce réseau
docker run -d --name container_a --network mon_reseau nginx

# 3. Lancer un deuxième conteneur sur le même réseau
docker run -d --name container_b --network mon_reseau nginx

# 4. Vérifier que les deux conteneurs tournent
docker ps

# 5. Ouvrir un shell dans container_a
docker exec -it container_a bash

# 6. (à l'intérieur de container_a) installer curl si besoin, puis joindre container_b PAR SON NOM
apt-get update && apt-get install -y curl
curl http://container_b

# 7. Sortir
exit