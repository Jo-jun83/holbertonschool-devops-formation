# DORA

## Q1

Les 4 métriques DORA sont :

- Deployment Frequency : fréquence à laquelle une équipe déploie en production.
- Lead Time for Changes : temps entre une modification du code et son déploiement en production.
- Change Failure Rate : pourcentage de déploiements qui provoquent un incident, une erreur ou nécessitent un correctif.
- Time to Restore / MTTR : temps nécessaire pour rétablir le service après un incident.

## Q2

Si une équipe ne déploie qu'une fois par trimestre, la métrique mauvaise est la Deployment Frequency.

Cela signifie que l'équipe déploie très rarement.

## Q3

Si on réduit le temps entre le merge d'une Pull Request et son déploiement en production, on améliore le Lead Time for Changes.

## Q4

Si 1 déploiement sur 4 provoque un incident, cela correspond au Change Failure Rate.

Ici, le taux est de 25 %.

Une valeur élevée est mauvaise, car cela signifie qu'une grande partie des déploiements provoque des problèmes.

## Q5

CALMS signifie :

- Culture
- Automation
- Lean
- Measurement
- Sharing

## Q6

Faux.

Les équipes dites "elite" déploient généralement plus souvent, avec de petits changements.

Faire des petits déploiements fréquents permet de réduire les risques, de détecter les problèmes plus rapidement et de corriger plus facilement.

## Q7

La meilleure réponse est :

(b) monitoring and alerting plus automated rollback

La surveillance, les alertes et le rollback automatique permettent de détecter rapidement un problème et de revenir rapidement à une version fonctionnelle.

Cela améliore donc le MTTR.

## Q8

Les métriques de throughput, c'est-à-dire la vitesse de livraison, sont :

- Deployment Frequency
- Lead Time for Changes

Les métriques de stabilité sont :

- Change Failure Rate
- MTTR

## Q9

Les blameless post-mortems servent à comprendre les causes d'un incident sans chercher à désigner un coupable.

Le but est d'identifier les problèmes techniques, les processus ou les décisions qui ont conduit à l'incident afin d'éviter qu'il se reproduise.

Cela encourage également les membres de l'équipe à parler ouvertement des erreurs et à améliorer le système.