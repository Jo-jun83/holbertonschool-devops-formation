Résolution du conflit de fusion

Le conflit se trouvait sur la ligne version dans le fichier config.yml :

feature/scale-up contenait version: 1.1.0
feature/dark-mode contenait version: 2.0.0

Cette ligne était en conflit parce que les deux branches avaient modifié exactement la même ligne avec des valeurs différentes.

Les autres modifications n’étaient pas en conflit car elles concernaient des lignes différentes : feature/scale-up a modifié le nombre de réplicas à 4, tandis que feature/dark-mode a ajouté feature_dark_mode: true. Git peut généralement fusionner automatiquement des modifications lorsqu’elles concernent des lignes différentes.

La version retenue après résolution est :

version: 2.0.0

Le fichier final conserve donc les deux modifications fonctionnelles demandées :

replicas: 4
feature_dark_mode: true

et fixe la version de l’application à 2.0.0.

Des modifications plus petites et plus ciblées permettent de réduire les conflits de fusion, car chaque branche modifie moins de lignes sans rapport avec son objectif principal. Lorsqu’une branche est limitée à une seule fonctionnalité ou à un seul changement, elle a moins de risques de modifier les mêmes parties d’un fichier qu’une autre branche. Cela rend les fusions automatiques plus fiables et les éventuels conflits manuels plus simples à comprendre, résoudre et vérifier.