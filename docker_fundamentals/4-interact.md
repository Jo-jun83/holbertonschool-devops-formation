# Interaction avec Docker et les variables d'environnement

L'application créée dans la tâche 1 a été modifiée afin que le message affiché puisse être configuré avec une variable d'environnement.

L'application Python lit la variable `MESSAGE` avec :

```python
MESSAGE = os.getenv("MESSAGE", "Hello from my first Docker image!")
```

Si aucune variable d'environnement n'est fournie, l'application utilise le message par défaut.

## Lancer le conteneur avec une variable d'environnement

L'image a été lancée avec l'option `-e` :

```bash
docker run -d --name first_image_container -p 8082:5000 -e MESSAGE="Bonjour depuis Docker !" first-image
```

L'option `-e` permet de transmettre la variable d'environnement `MESSAGE` au conteneur.

Pour vérifier la réponse de l'application :

```bash
curl http://localhost:8082
```

Résultat observé :

```text
Bonjour depuis Docker !
```

Cela montre que le message affiché par l'application change en fonction de la variable d'environnement fournie au démarrage du conteneur.

## Lire la variable depuis l'intérieur du conteneur

La variable d'environnement a été vérifiée depuis l'intérieur du conteneur en cours d'exécution avec :

```bash
docker exec first_image_container printenv MESSAGE
```

Résultat observé :

```text
Bonjour depuis Docker !
```

Cela confirme que la variable `MESSAGE` est bien disponible à l'intérieur du conteneur.

## Inspecter le conteneur

La configuration du conteneur a été inspectée avec :

```bash
docker inspect -f "{{range .Config.Env}}{{println .}}{{end}}" first_image_container
```

La sortie contenait notamment :

```text
MESSAGE=Bonjour depuis Docker !
```

Cela confirme que la variable d'environnement a bien été transmise au conteneur et enregistrée dans sa configuration.

## Conclusion

L'application accepte désormais un message configurable grâce à la variable d'environnement `MESSAGE`.

Les fonctionnalités Docker suivantes ont été utilisées :

- `-e` pour transmettre une variable d'environnement au démarrage du conteneur ;
- `docker exec` pour vérifier la variable depuis l'intérieur du conteneur ;
- `docker inspect` pour vérifier la configuration du conteneur.