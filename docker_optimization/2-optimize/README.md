# Docker Optimization — 2-optimize

Optimisation d'une image Node/Express : réduction de taille, cache de build
fiable sur les changements de code, et exécution en non-root.

## Changements apportés au Dockerfile

- **Image de base** : `node:20` (full, Debian) → `node:20-alpine` (minimale)
- **Ordre des couches** : `COPY package.json .` + `RUN npm install` **avant**
  `COPY . .`, pour que l'installation des dépendances reste en cache tant que
  `package.json` ne change pas, même si le code source change.
- **`.dockerignore`** ajouté, pour éviter de copier un éventuel `node_modules`
  local dans l'image (régénéré de toute façon par `RUN npm install`).
- **Utilisateur non-root** : ajout de `RUN adduser --disabled-password appuser`
  et `USER appuser`, placés après `COPY . .` (pour que les fichiers soient
  copiés avec les droits root avant de changer d'utilisateur) et avant `CMD`.

## Avant / Après

| Mesure | Avant (`node:20`) | Après (`node:20-alpine`) |
|---|---|---|
| Taille de l'image | 1.1 GB | 143 MB |
| `RUN npm install` recaché après un changement de **code uniquement** (`index.js`) | Non — relancé à chaque fois (~2.6s) | Oui — reste `CACHED` |
| Utilisateur d'exécution | root (implicite, par défaut) | `appuser` (non-root) |
| `.dockerignore` | Absent | Présent (`node_modules`, `npm-debug.log`) |

**Réduction de taille : environ 87 %** (1.1 GB → 143 MB).

## Commandes utilisées pour mesurer

```powershell
# Baseline
docker build -t optimize-baseline .
docker images optimize-baseline

# Modifier une ligne dans index.js, puis rebuild pour observer le cache
docker build -t optimize-baseline .
# => COPY . . et RUN npm install non cachés : tout l'install est refait

# Version optimisée
docker build -t optimize-fixed .
docker images optimize-fixed
# => RUN npm install reste CACHED après un changement de code uniquement

# Vérification non-root
docker run -d --name optimize_test -p 3000:3000 optimize-fixed
docker exec optimize_test whoami
# => appuser
```