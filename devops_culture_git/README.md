# Culture DevOps et Git

Ce module présente les pratiques humaines et techniques qui facilitent la
livraison continue : environnement reproductible, collaboration par pull
request, résolution de conflits, mesure de la performance et apprentissage à
partir des incidents.

## Objectifs

- valider un environnement Git et Docker ;
- travailler avec des branches et des pull requests ;
- comprendre et résoudre un conflit de fusion ;
- connaître les quatre métriques DORA et le modèle CALMS ;
- rédiger un post-mortem sans blâme ;
- structurer un historique avec Conventional Commits.

## Prérequis

- Git configuré avec un nom et une adresse e-mail ;
- Docker en cours d'exécution ;
- Bash ou Git Bash ;
- un accès GitHub par SSH pour la partie collaborative ;
- Python 3 pour l'exercice HolbieBot.

## Exercices

| Étape | Ressource | Sujet |
| ---: | --- | --- |
| 0 | [`0-environment.md`](./0-environment.md) | validation de Git, Docker, SSH et du runtime local |
| 1 | [`1-pull_request.md`](./1-pull_request.md) | création, revue et fusion de pull requests |
| 2 | [`2-merge_conflict`](./2-merge_conflict/) | résolution documentée d'un conflit dans un fichier YAML |
| 3 | [`3-dora.md`](./3-dora.md) | métriques DORA, CALMS et performance de livraison |
| 4 | [`4-postmortem.md`](./4-postmortem.md) | analyse d'un incident et définition d'actions correctives |
| 5 | [`5-conventional-commit`](./5-conventional-commit/) | historique Git utilisant les types `feat`, `fix`, `refactor`, `test` et `docs` |

## Vérifier l'environnement

Depuis ce dossier, exécuter :

```bash
bash check-setup.sh
```

Le script contrôle la disponibilité de Docker et de Git, la configuration de
l'identité Git, l'authentification SSH vers GitHub et la présence de Python ou
Node.js.

Un test Docker simple peut compléter la vérification :

```bash
docker run --rm hello-world
```

## S'entraîner à résoudre un conflit

Le script fourni crée un petit dépôt autonome avec deux branches qui modifient
la même version :

```bash
bash setup-conflit.sh conflit-demo
cd conflit-demo
git merge feature/dark-mode
```

Après l'apparition du conflit :

1. repérer les marqueurs `<<<<<<<`, `=======` et `>>>>>>>` dans `config.yml` ;
2. conserver les valeurs fonctionnelles attendues ;
3. supprimer les marqueurs ;
4. valider la résolution avec `git add config.yml` puis `git commit`.

La solution retenue et son explication sont disponibles dans
[`2-merge_conflict/RESOLUTION.md`](./2-merge_conflict/RESOLUTION.md).

> `setup-conflit.sh` recrée entièrement le dossier passé en argument. Ne pas
> l'utiliser avec le nom d'un dossier contenant un travail à conserver.

## Conventional Commits

Le dernier exercice applique la forme suivante :

```text
type: description courte
```

Exemples :

```text
feat: add deploy capability
fix: clamp energy between 0 and 100
test: add energy validation tests
docs: add HolbieBot usage instructions
```

Pour exécuter le programme et ses tests :

```bash
cd 5-conventional-commit
python devops_bot.py
python -m unittest test_devops_bot.py
```

## Principes à retenir

Une culture DevOps efficace associe automatisation et collaboration. Les petits
changements, la revue de code, la mesure par les indicateurs DORA et les
post-mortems sans blâme permettent de livrer plus souvent tout en améliorant la
stabilité du service.
