# 1. Pull de l'image officielle
docker pull nginx

# 2. Run du conteneur en arrière-plan (première tentative, port 8080)
docker run -d --name my_nginx -p 8081:80 nginx
docker ps
curl http://localhost:8081

# 4. Ouvrir un shell à l'intérieur du conteneur
docker exec -it my_nginx bash
# (à l'intérieur du conteneur)
ls /usr/share/nginx/html
cat /etc/nginx/nginx.conf
exit

# 5. Lire les logs du conteneur
docker logs my_nginx

# 6. Arrêter puis supprimer le conteneur
docker stop my_nginx
docker rm my_nginx