# Post-mortem — Incident du vendredi soir

## 1. Résumé de l'incident

Le vendredi soir, une modification de configuration a provoqué une interruption du tunnel de paiement du site PixelCart.

Une erreur dans l'URL de connexion à la base de données a rendu le checkout indisponible pendant environ 15 heures.

L'incident n'a pas été détecté immédiatement car aucun système de monitoring ou d'alerte automatique n'était en place.

Le service a finalement été rétabli le samedi matin après identification et correction manuelle de la configuration.

---

## 2. Timeline

### Vendredi — 17h40
Début du déploiement d'une modification du checkout.

Le déploiement est réalisé manuellement :
- connexion au serveur de production en SSH ;
- copie manuelle des fichiers ;
- modification directe de la configuration sur le serveur.

### Vendredi — 17h52
Une valeur de configuration concernant l'URL de la base de données est modifiée.

Une faute de frappe est introduite dans cette configuration.

La modification n'est pas testée dans un environnement identique à la production.

### Vendredi — 18h05
Le déploiement est terminé.

Aucune surveillance active du site ni alerte automatique n'est en place.

### Vendredi — 20h30
Un client signale sur les réseaux sociaux que le checkout ne fonctionne plus.

L'équipe ne voit pas immédiatement ce signalement.

### Samedi — 9h15
L'incident est découvert par l'équipe.

La personne qui intervient ne dispose pas immédiatement des accès nécessaires au serveur et il n'existe pas de journal clair des changements effectués.

Il n'existe pas non plus de mécanisme simple de rollback.

### Samedi — 11h40
La faute de frappe est identifiée et corrigée manuellement.

Le service est rétabli.

### Durée totale
Environ 15 heures d'indisponibilité du checkout.

---

## 3. Causes systémiques

L'objectif de ce post-mortem n'est pas de désigner une personne responsable, mais d'identifier les faiblesses du système qui ont permis à l'incident de se produire et de durer.

### Déploiement manuel en production

Le déploiement repose sur des actions manuelles effectuées directement sur le serveur.

Cela augmente le risque d'erreur humaine et rend les déploiements difficiles à reproduire.

**Métriques DORA dégradées :**
- Change Failure Rate : le risque qu'un déploiement provoque un incident augmente.
- Lead Time for Changes : le processus manuel ralentit la mise en production.

### Absence d'environnement de test proche de la production

Les modifications ne sont pas validées dans un environnement représentatif de la production.

Une erreur de configuration peut donc ne pas être détectée avant le déploiement.

**Métrique DORA dégradée :**
- Change Failure Rate.

### Absence de monitoring et d'alerting

Le système ne détecte pas automatiquement que le checkout est indisponible.

L'équipe dépend donc des retours des clients pour découvrir l'incident.

**Métrique DORA dégradée :**
- MTTR / Time to Restore, car le début de la résolution est fortement retardé.

### Absence de traçabilité des déploiements

Il n'existe pas de journal clair indiquant ce qui a été déployé et quelles modifications ont été réalisées.

Cela rallonge le diagnostic lorsqu'un incident survient.

**Métrique DORA dégradée :**
- MTTR.

### Absence de rollback simple

Il n'est pas possible de revenir rapidement à une version précédente connue comme fonctionnelle.

La correction doit être réalisée manuellement.

**Métriques DORA dégradées :**
- MTTR.
- Change Failure Rate, car l'impact d'un déploiement défectueux est plus important.

### Gestion des accès insuffisante

La personne qui intervient sur l'incident ne dispose pas immédiatement des accès nécessaires.

Cela augmente le temps nécessaire pour restaurer le service.

**Métrique DORA dégradée :**
- MTTR.

---

## 4. Actions prioritaires

### Priorité 1 — Mettre en place une pipeline CI/CD

Le déploiement doit être automatisé plutôt que réalisé manuellement en SSH.

La pipeline pourrait :
- exécuter les tests ;
- vérifier la configuration ;
- construire l'application ;
- déployer automatiquement ;
- conserver l'historique des versions.

**Pourquoi c'est prioritaire :**

Cela réduit fortement les erreurs manuelles et rend les déploiements reproductibles et traçables.

Cela améliore notamment :
- le Change Failure Rate ;
- le Lead Time for Changes ;
- la Deployment Frequency.

---

### Priorité 2 — Mettre en place du monitoring et des alertes

Il faut surveiller automatiquement les éléments critiques du service, notamment le checkout.

Une alerte doit être envoyée immédiatement lorsqu'un service important devient indisponible.

**Pourquoi c'est prioritaire :**

Dans cet incident, plusieurs heures ont été perdues simplement parce que l'équipe ne savait pas qu'un problème existait.

Une détection rapide permet de commencer la résolution beaucoup plus tôt.

Cela améliore principalement :

- le MTTR.

---

### Priorité 3 — Mettre en place un rollback automatisé

Chaque déploiement doit permettre de revenir rapidement à la dernière version fonctionnelle.

Par exemple, si le checkout échoue après un déploiement, la version précédente pourrait être restaurée automatiquement ou en une seule commande.

**Pourquoi c'est prioritaire :**

Même avec de bons tests, certains incidents peuvent toujours atteindre la production.

Le but n'est donc pas seulement d'empêcher tous les incidents, mais aussi de limiter leur durée et leur impact.

Cela améliore principalement :

- le MTTR ;
- le Change Failure Rate.

---

## 5. Impact sur les métriques DORA

Cet incident dégrade plusieurs métriques DORA.

### Change Failure Rate

Le déploiement a directement provoqué une panne en production.

L'absence de tests automatisés et le déploiement manuel augmentent le risque que cela se reproduise.

### MTTR / Time to Restore

Le temps de restauration a été très élevé à cause :
- de l'absence d'alerting ;
- du manque de traçabilité ;
- de l'absence de rollback ;
- des problèmes d'accès au serveur.

### Lead Time for Changes

Le processus de déploiement manuel rend les mises en production plus lentes et plus complexes.

Une pipeline automatisée permettrait de réduire le temps entre une modification du code et sa disponibilité en production.

### Deployment Frequency

Un processus de déploiement manuel et risqué peut pousser l'équipe à déployer moins souvent.

L'automatisation permet au contraire de réaliser des déploiements plus petits et plus fréquents.

---

## 6. Conclusion

L'incident ne vient pas d'une erreur individuelle isolée, mais d'un processus de déploiement fragile.

Le système permettait qu'une erreur de configuration atteigne directement la production, sans validation suffisante, sans détection rapide et sans mécanisme simple de retour arrière.

Les premières améliorations à mettre en place sont donc :

1. automatiser les déploiements avec une pipeline CI/CD ;
2. mettre en place du monitoring et de l'alerting ;
3. permettre un rollback rapide et automatisé.

Ces mesures réduiraient à la fois le risque d'incident et le temps nécessaire pour restaurer le service lorsqu'un problème survient.