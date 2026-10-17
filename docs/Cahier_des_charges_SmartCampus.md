# Cahier des charges — SmartCampus

17 octobre 2026 · Oli

SmartCampus est une plateforme web où étudiants et personnel s'authentifient, trouvent une salle libre et la réservent sans conflit. Ce cahier des charges étend le tuto du TP 1 de 3 à 6 modules et 41 exigences fonctionnelles, qui forment la base du backlog Jira.

## 1. Contexte, objectifs et périmètre

SmartCampus remplace une gestion des salles dispersée (e-mails, registres papier, appels à l'administration) par un service unique en ligne, où chaque réservation est vérifiée et tracée.

### 1.1 Fiche projet

| Élément | Valeur |
| --- | --- |
| Projet | SmartCampus — plateforme de services du campus |
| Cadre | Projet fil rouge des TP DevOps, ENSA Khouribga |
| Document de référence | Énoncé « TP 1 — Piloter le projet SmartCampus avec Jira » |
| Clé du projet Jira | SC |
| Équipe | à compléter |
| Encadrant | à compléter |
| Version du document | 1.1 — backend FastAPI |

### 1.2 Problématique

La situation de départ est supposée, comme le prévoit l'étude de cas :

- Une même salle est réservée deux fois, faute de vue partagée des créneaux.
- Des salles réservées restent vides pendant que d'autres demandeurs n'en trouvent pas.
- Rien ne trace qui a réservé, annulé ou signalé une panne.
- Les pannes d'équipement (vidéoprojecteur, PC) sont découvertes au début du cours.
- Aucun chiffre d'occupation n'aide à planifier les besoins en salles.

### 1.3 Objectifs

| ID | Objectif | Indicateur de réussite |
| --- | --- | --- |
| O1 | Trouver et réserver une salle libre rapidement | Réservation faite en 3 écrans au plus et moins de 2 min |
| O2 | Supprimer les doubles réservations | 0 chevauchement accepté (contrôle applicatif et contrainte en base) |
| O3 | Tracer les actions sensibles | 100 % des connexions, échecs et changements de réservation journalisés |
| O4 | Fiabiliser l'état des salles | Tout incident visible par le technicien ; salle hors service non réservable |
| O5 | Piloter l'occupation | Taux d'occupation par salle et par semaine disponible au gestionnaire |
| O6 | Livrer par une chaîne DevOps complète | Chaque changement lié à une clé Jira, construit, testé et déployé par pipeline |

### 1.4 Périmètre

La version 1 couvre six modules ; chacun devient un Epic Jira.

| Module | Contenu | Origine |
| --- | --- | --- |
| AUTH — Authentification et comptes | Connexion, sécurité des accès, gestion des comptes et rôles | Socle du TP |
| ROOM — Gestion des salles | Référentiel des salles et équipements, recherche, disponibilité | Socle du TP |
| BOOK — Réservation | Création, modification, annulation, validation des réservations | Socle du TP |
| NOTIF — Notifications | Confirmations, rappels, alertes par e-mail et dans l'application | Extension |
| INCID — Incidents | Signalement et suivi des pannes dans les salles | Extension |
| ADMIN — Administration et pilotage | Paramètres, journal d'audit, tableau de bord d'occupation | Extension |

Hors périmètre de la version 1 :

- Emplois du temps et planification pédagogique : SmartCampus réserve des salles, il ne construit pas l'emploi du temps.
- Application mobile native : l'interface web responsive couvre le mobile.
- Connexion unique avec l'annuaire réel de l'université (EF-AUTH-09, prévue après la V1).
- Paiement, gestion des notes et des examens.

## 2. Acteurs et rôles

Cinq profils humains utilisent SmartCampus ; chaque compte porte un rôle, et ses droits sont vérifiés côté serveur à chaque requête (contrôle d'accès par rôle, RBAC).

| Acteur | Qui | Droits principaux |
| --- | --- | --- |
| Étudiant | Inscrit dans l'établissement | Rechercher une salle, réserver une salle de travail ou de TD dans son quota, gérer ses réservations, signaler un incident |
| Enseignant | Corps enseignant permanent ou vacataire | Droits de l'étudiant, plus : réservations plus longues et plus lointaines, réservations récurrentes, demande d'amphithéâtre |
| Gestionnaire des salles | Service logistique ou scolarité | Gérer les salles et équipements, valider ou refuser les demandes, bloquer des créneaux, consulter le tableau de bord |
| Technicien de maintenance | Service technique | Traiter les incidents, mettre une salle hors service et la remettre en service |
| Administrateur système | Service informatique | Gérer les comptes et les rôles, paramétrer les règles, consulter le journal d'audit |

Deux acteurs non humains interviennent aussi : le planificateur de tâches (rappels, libération des salles non occupées) et le serveur de messagerie SMTP qui achemine les e-mails.

## 3. Besoins fonctionnels

Les 41 exigences fonctionnelles sont réparties en six modules ; 13 sont indispensables (M) et toutes appartiennent au socle AUTH, ROOM, BOOK du TP.

Priorités selon la méthode MoSCoW, au niveau de la version 1 :

- **M** (Must) : indispensable, la V1 n'est pas livrable sans.
- **S** (Should) : important, prévu dans un sprint de la V1.
- **C** (Could) : souhaitable, réalisé si la capacité le permet.
- **W** (Won't) : hors V1, conservé dans le backlog.

Chaque identifiant EF-MODULE-NN est repris dans le ticket Jira correspondant (champ description ou label) pour garder la traçabilité.

### 3.1 AUTH — Authentification et comptes

| ID | Exigence | Acteur | Priorité |
| --- | --- | --- | --- |
| EF-AUTH-01 | Se connecter avec son e-mail institutionnel et son mot de passe | Tous | M |
| EF-AUTH-02 | Se déconnecter ; la session est invalidée côté serveur | Tous | M |
| EF-AUTH-03 | Afficher un message d'erreur clair et générique si les identifiants sont faux, sans dire lequel l'est | Tous | M |
| EF-AUTH-04 | Journaliser chaque échec de connexion et bloquer temporairement le compte après 3 échecs consécutifs (RG-02) | Système | M |
| EF-AUTH-05 | Réinitialiser son mot de passe par un lien reçu par e-mail, valable 30 min et à usage unique | Tous | S |
| EF-AUTH-06 | Consulter et modifier son profil (nom, téléphone, préférences de notification) | Tous | S |
| EF-AUTH-07 | Créer, modifier, désactiver un compte et lui attribuer un rôle | Administrateur | M |
| EF-AUTH-08 | Importer des comptes en masse depuis un fichier CSV | Administrateur | C |
| EF-AUTH-09 | Se connecter par l'annuaire de l'établissement (SSO / LDAP) | Tous | W |

### 3.2 ROOM — Gestion des salles et équipements

| ID | Exigence | Acteur | Priorité |
| --- | --- | --- | --- |
| EF-ROOM-01 | Consulter la liste des salles : bâtiment, type, capacité, équipements, statut | Tous | M |
| EF-ROOM-02 | Rechercher une salle libre par date, créneau, capacité minimale, type et équipement | Tous | M |
| EF-ROOM-03 | Afficher le planning d'occupation d'une salle en vue jour et semaine | Tous | M |
| EF-ROOM-04 | Créer, modifier et archiver une salle | Gestionnaire | M |
| EF-ROOM-05 | Gérer le catalogue d'équipements (vidéoprojecteur, PC, tableau interactif) et leur affectation aux salles | Gestionnaire | S |
| EF-ROOM-06 | Bloquer une salle sur une période (examen, maintenance, événement) avec un motif | Gestionnaire | S |
| EF-ROOM-07 | Mettre une salle hors service et la remettre en service (RG-10) | Technicien, Gestionnaire | S |
| EF-ROOM-08 | Afficher sur chaque salle un QR code qui ouvre sa fiche et son planning | Gestionnaire | C |

### 3.3 BOOK — Réservation

| ID | Exigence | Acteur | Priorité |
| --- | --- | --- | --- |
| EF-BOOK-01 | Réserver un créneau libre : salle, date, heure de début et de fin, motif, nombre de participants (RG-03, RG-04, RG-07, RG-08) | Étudiant, Enseignant | M |
| EF-BOOK-02 | Refuser toute réservation qui chevauche une réservation ou un blocage existant (RG-01) | Système | M |
| EF-BOOK-03 | Consulter « Mes réservations » : à venir, passées, annulées | Étudiant, Enseignant | M |
| EF-BOOK-04 | Annuler sa réservation dans le délai autorisé (RG-05) | Étudiant, Enseignant | M |
| EF-BOOK-05 | Modifier le créneau ou la salle d'une réservation non commencée, avec nouvelle vérification des conflits | Étudiant, Enseignant | S |
| EF-BOOK-06 | Soumettre à validation les demandes d'amphithéâtre ou hors quota ; le gestionnaire valide ou refuse avec un motif (RG-09) | Enseignant, Gestionnaire | S |
| EF-BOOK-07 | Créer une réservation récurrente hebdomadaire jusqu'à une date de fin (RG-04) | Enseignant | S |
| EF-BOOK-08 | Confirmer sa présence (check-in) par QR code ou bouton ; sinon, libération automatique de la salle (RG-06) | Étudiant, Enseignant | C |
| EF-BOOK-09 | S'inscrire en liste d'attente sur un créneau occupé et être prévenu s'il se libère | Étudiant, Enseignant | C |

### 3.4 NOTIF — Notifications

| ID | Exigence | Acteur | Priorité |
| --- | --- | --- | --- |
| EF-NOTIF-01 | Envoyer un e-mail de confirmation à la création, la modification et l'annulation d'une réservation | Système | S |
| EF-NOTIF-02 | Envoyer un rappel 1 h avant le début d'une réservation | Système | S |
| EF-NOTIF-03 | Informer le demandeur de la décision du gestionnaire (validée ou refusée, avec motif) | Système | S |
| EF-NOTIF-04 | Prévenir les titulaires de réservations futures quand leur salle est bloquée ou mise hors service (RG-10) | Système | S |
| EF-NOTIF-05 | Proposer un centre de notifications dans l'application (lues, non lues) | Tous | C |
| EF-NOTIF-06 | Choisir ses canaux de notification : e-mail, application, ou les deux | Tous | C |

### 3.5 INCID — Signalement d'incidents

| ID | Exigence | Acteur | Priorité |
| --- | --- | --- | --- |
| EF-INCID-01 | Signaler un incident sur une salle : catégorie, description, photo facultative | Étudiant, Enseignant | S |
| EF-INCID-02 | Suivre l'état de son signalement : Ouvert, En cours, Résolu | Étudiant, Enseignant | S |
| EF-INCID-03 | Prendre en charge, commenter et clôturer un incident | Technicien | S |
| EF-INCID-04 | Mettre la salle hors service directement depuis un incident bloquant (lien EF-ROOM-07, EF-NOTIF-04) | Technicien | C |
| EF-INCID-05 | Consulter l'historique des incidents d'une salle | Technicien, Gestionnaire | C |

### 3.6 ADMIN — Administration et pilotage

| ID | Exigence | Acteur | Priorité |
| --- | --- | --- | --- |
| EF-ADMIN-01 | Paramétrer les règles de gestion : durées maximales, horizon, quotas, délai d'annulation, délai de check-in | Administrateur | S |
| EF-ADMIN-02 | Consulter le journal d'audit (connexions, échecs, actions sur les réservations), filtré par utilisateur et par date | Administrateur | S |
| EF-ADMIN-03 | Afficher un tableau de bord : taux d'occupation par salle, bâtiment et semaine, salles les plus demandées, taux de non-présentation | Gestionnaire | S |
| EF-ADMIN-04 | Exporter réservations et statistiques au format CSV | Gestionnaire | C |

## 4. Règles de gestion

Douze règles encadrent les réservations et l'accès ; leurs valeurs chiffrées sont des propositions, paramétrables par l'administrateur (EF-ADMIN-01) et à valider avec l'encadrant (Annexe B).

| ID | Règle | Exigences concernées |
| --- | --- | --- |
| RG-01 | Une salle ne peut pas porter deux réservations dont les créneaux se chevauchent. Les réservations confirmées, celles en attente de validation et les blocages comptent tous. | EF-BOOK-02, EF-BOOK-05, EF-ROOM-06 |
| RG-02 | Après 3 échecs de connexion consécutifs, le compte est bloqué 15 min et un événement de sécurité est journalisé. Une connexion réussie remet le compteur à zéro. | EF-AUTH-03, EF-AUTH-04 |
| RG-03 | Les créneaux vont par pas de 30 min, de 08:00 à 20:00, du lundi au samedi. Durée maximale : 2 h pour un étudiant, 4 h pour un enseignant. | EF-BOOK-01 |
| RG-04 | Horizon de réservation : 7 jours pour un étudiant, 30 jours pour un enseignant. Une récurrence ne dépasse pas la fin du semestre. | EF-BOOK-01, EF-BOOK-07 |
| RG-05 | Le titulaire peut annuler jusqu'au début du créneau. Une annulation faite moins de 1 h avant le début compte comme une non-présentation. | EF-BOOK-04 |
| RG-06 | Sans check-in 15 min après le début, la réservation passe à « Non honorée » et la salle redevient libre. Trois non-présentations en 30 jours suspendent le droit de réserver d'un étudiant pendant 7 jours. | EF-BOOK-08, EF-ADMIN-03 |
| RG-07 | Un étudiant a au plus 2 réservations à venir et 6 h réservées par semaine. Une demande au-delà passe par validation (RG-09). | EF-BOOK-01, EF-BOOK-06 |
| RG-08 | Le nombre de participants déclaré ne dépasse pas la capacité de la salle. | EF-BOOK-01, EF-ROOM-02 |
| RG-09 | Seul un enseignant peut demander un amphithéâtre. Ces demandes et celles hors quota (RG-07) sont validées par le gestionnaire. Sans décision 24 h avant le début, la demande est refusée automatiquement et le demandeur prévenu. | EF-BOOK-06, EF-NOTIF-03 |
| RG-10 | Une salle bloquée ou hors service ne peut pas être réservée. Les réservations futures sur la période sont annulées et leurs titulaires prévenus. | EF-ROOM-06, EF-ROOM-07, EF-NOTIF-04 |
| RG-11 | Seules les adresses du domaine e-mail de l'établissement servent d'identifiant. | EF-AUTH-01, EF-AUTH-07 |
| RG-12 | Une réservation n'est jamais supprimée : elle change de statut (En attente, Confirmée, Refusée, Annulée, Non honorée, Terminée), ce qui conserve l'historique pour l'audit. | EF-BOOK-03, EF-ADMIN-02 |

### 4.1 Cycle de vie d'une réservation

*(Diagramme du cycle de vie : voir la version Word)*

Une réservation n'occupe la salle que tant qu'elle est en attente ou confirmée ; les quatre statuts finaux libèrent le créneau mais restent dans l'historique.

## 5. Exigences non fonctionnelles

Quinze exigences de qualité s'appliquent à tous les modules ; chacune a un critère vérifiable, et la plupart sont contrôlées automatiquement par le pipeline.

| ID | Catégorie | Exigence | Vérification |
| --- | --- | --- | --- |
| ENF-01 | Sécurité | Mots de passe hachés (bcrypt ou Argon2), jamais stockés ni journalisés en clair | Revue de code, test sur la base |
| ENF-02 | Sécurité | Tous les échanges en HTTPS ; API protégée par jeton JWT expirant après 30 min | Test d'appel sans jeton ou expiré : réponse 401 |
| ENF-03 | Sécurité | Droits du rôle vérifiés côté serveur sur chaque point d'accès de l'API | Tests d'autorisation : réponse 403 hors rôle |
| ENF-04 | Sécurité | Aucune vulnérabilité critique ou haute (OWASP Top 10, dépendances, images) | Scans SAST, dépendances et images dans le pipeline DevSecOps |
| ENF-05 | Données personnelles | Conformité à la loi marocaine 09-08 : données minimales, journaux conservés 12 mois au plus | Revue du modèle de données et des durées de conservation |
| ENF-06 | Performance | 95 % des recherches de salles répondent en moins de 1 s avec 200 utilisateurs simultanés | Test de charge (JMeter ou k6) |
| ENF-07 | Disponibilité | 99 % de disponibilité de 08:00 à 20:00 ; redémarrage automatique d'un composant en panne | Sondes Kubernetes, suivi de disponibilité |
| ENF-08 | Scalabilité | Backend sans état, au moins 2 réplicas, montée en charge horizontale | Déploiement Kubernetes à 2 réplicas, test d'arrêt d'un pod |
| ENF-09 | Ergonomie | Interface en français, responsive de 360 px (mobile) à l'écran de bureau | Recette sur mobile et sur poste |
| ENF-10 | Accessibilité | Parcours connexion, recherche et réservation conformes WCAG 2.1 niveau AA | Audit Lighthouse, score accessibilité de 90 au moins |
| ENF-11 | Maintenabilité | Couverture des tests unitaires backend de 70 % au moins ; aucun bug bloquant en analyse statique | pytest --cov-fail-under=70 et quality gate SonarQube dans Jenkins |
| ENF-12 | Traçabilité | Chaque branche, commit et Pull Request cite une clé Jira (SC-nn) | Contrôle automatique du message de commit et du titre de PR |
| ENF-13 | Portabilité | Chaque composant livré en image Docker ; environnements recréés par code (Terraform, Ansible) | Recréation complète d'un environnement de test |
| ENF-14 | Observabilité | Journaux structurés en JSON, point de santé /health, métriques exposées | Contrôle des journaux et de /health en recette |
| ENF-15 | Sauvegarde | Base sauvegardée chaque jour ; restauration testée une fois par sprint | Procès-verbal de test de restauration |

## 6. Architecture et choix techniques

SmartCampus suit une architecture trois tiers : une application web monopage, une API REST et une base relationnelle. L'équipe retient FastAPI (Python) pour l'API ; l'interface web et la base de données ne changent pas.

### 6.1 Stack retenue

| Couche | Choix retenu | Justification |
| --- | --- | --- |
| Interface web | React + TypeScript (Vite) | Application monopage responsive (ENF-09), tests avec Vitest |
| API | FastAPI (Python 3.14), servie par Uvicorn | Peu de code, validation des entrées par Pydantic, documentation OpenAPI générée automatiquement |
| Sécurité | PyJWT pour les jetons, bcrypt pour les mots de passe, dépendance FastAPI commune pour vérifier le rôle | JWT et contrôle par rôle (ENF-01 à ENF-03) |
| Accès aux données | SQLAlchemy 2 (ORM) + Alembic (migrations) | Schéma versionné avec le code ; `alembic upgrade head` appliqué à chaque déploiement |
| Base de données | PostgreSQL 16 | Une contrainte d'exclusion interdit en base tout chevauchement (RG-01), en plus du contrôle applicatif |
| E-mails | SMTP ; MailHog en développement | Tester les notifications sans envoyer de vrais e-mails |
| Tâches planifiées | Script Python lancé par un CronJob Kubernetes | Rappels (EF-NOTIF-02), libération des salles (RG-06), refus automatique (RG-09), exécutés une seule fois même avec 2 réplicas de l'API |
| Contrat d'API | OpenAPI généré par FastAPI (Swagger UI sur /docs) | Contrat partagé entre interface et API, sans configuration supplémentaire |
| Tests | pytest, TestClient (httpx), pytest-cov ; Playwright de bout en bout | Couverture (ENF-11) et recette automatisée des critères d'acceptation |
| Qualité du code | ruff (lint), mypy (typage) | Compense l'absence de compilation : les erreurs sont détectées dans le pipeline |

FastAPI réduit le code du backend et laisse plus de temps à la chaîne DevOps, qui est l'objet du cours. Trois points demandent de la rigueur :

- **Sécurité** : pas d'équivalent de Spring Security ; l'authentification JWT et la vérification des rôles vivent dans une dépendance FastAPI commune, testée à part (ENF-03).
- **Pas de compilation** : ruff, mypy et pytest tournent dans Jenkins à chaque Pull Request (section 7).
- **Tâches planifiées** : un planificateur placé dans l'API (APScheduler) tournerait dans chacun des 2 réplicas et enverrait chaque rappel deux fois ; d'où le CronJob Kubernetes (ENF-08).

Garantie de RG-01 au niveau de la base, pour les réservations en attente ou confirmées (les blocages restent contrôlés par l'API) :

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE booking ADD CONSTRAINT booking_no_overlap
  EXCLUDE USING gist (room_id WITH =, tstzrange(start_at, end_at) WITH &&)
  WHERE (status IN ('PENDING', 'CONFIRMED'));
```

### 6.2 Modèle de données principal

| Entité | Attributs clés | Relations |
| --- | --- | --- |
| User | e-mail, nom, rôle, statut du compte, compteur d'échecs, bloqué jusqu'à | passe des Booking, signale des Incident |
| Room | code, bâtiment, type, capacité, statut (active, hors service, archivée) | possède des Equipment, reçoit des Booking et des Blocking |
| Equipment | libellé, catégorie | rattaché à plusieurs Room |
| Booking | salle, titulaire, début, fin, motif, participants, statut, série de récurrence | appartient à un User et une Room |
| Blocking | salle, période, motif, auteur | appartient à une Room |
| Incident | salle, auteur, catégorie, description, photo, statut | concerne une Room |
| Notification | destinataire, type, canal, lu ou non | adressée à un User |
| AuditLog | acteur, action, cible, date, adresse IP | trace les actions des User |
| Setting | clé, valeur | règles paramétrables (EF-ADMIN-01) |

### 6.3 Architecture cible

*(Diagramme d'architecture : voir la version Word)*

Le navigateur ne parle qu'à l'Ingress, qui sert l'interface et l'API ; seule l'API accède à la base. Une image n'atteint le cluster qu'après le passage du pipeline Jenkins.

## 7. Chaîne DevOps et traçabilité

Chaque TP ajoute un maillon à la même chaîne de livraison ; le tableau fixe ce que SmartCampus doit produire à chaque étape et l'exigence de qualité qu'elle sert.

| Étape | Outil | Production attendue sur SmartCampus | Exigences servies |
| --- | --- | --- | --- |
| 1 | Jira | Backlog à 6 Epics, Stories avec critères d'acceptation, Sprint 1, workflow To Do → In Progress → Done, clé retenue pour le TP suivant | ENF-12 |
| 2 | Git / GitHub | Dépôt, branche main protégée, une branche par ticket, Pull Requests revues et liées aux tickets | ENF-12 |
| 3 | Jenkins | Jenkinsfile : installation des dépendances, lint (ruff), typage (mypy), tests pytest avec couverture, analyse SonarQube à chaque PR ; un échec bloque la fusion | ENF-11 |
| 4 | Docker | Dockerfile de l'interface et de l'API, docker-compose (API, interface, PostgreSQL, MailHog), images taguées par commit | ENF-13 |
| 5 | Kubernetes | Deployments, Services, Ingress, ConfigMap et Secret, sondes de vie et de disponibilité, 2 réplicas de l'API, CronJob des tâches planifiées | ENF-07, ENF-08 |
| 6 | Terraform | Infrastructure décrite en code : cluster, réseau, base de données, variables par environnement | ENF-13 |
| 7 | Ansible | Configuration des machines et des dépendances, déploiement reproductible | ENF-13 |
| 8 | DevSecOps | Analyse du code Python (Bandit ou Semgrep), des dépendances (pip-audit), des images (Trivy) et des secrets (Gitleaks), bloquantes dans le pipeline | ENF-04 |

### 7.1 Conventions de nommage

| Élément | Convention | Exemple |
| --- | --- | --- |
| Branche | type/CLÉ-description courte | feature/SC-11-login, bugfix/SC-13-message-echecs |
| Commit | CLÉ + action au présent | SC-11 Ajoute la validation des identifiants |
| Pull Request | CLÉ — résumé | SC-11 — Implémenter la connexion utilisateur |
| Image Docker | composant:hash court du commit | smartcampus-api:3f2a9c1 |

### 7.2 Chaîne de traçabilité de bout en bout

Une exigence se suit sans rupture du cahier des charges jusqu'au déploiement :

**EF-AUTH-01** → Epic **AUTH** → Story **SC-11** → Task **SC-12** → branche **feature/SC-11-login** → PR **SC-11 — Implémenter la connexion utilisateur** → build Jenkins → image **smartcampus-api:\<hash>** → déploiement Kubernetes.

Cette ligne est la « vue de traçabilité » demandée au point 9 du TP 1.

## 8. Planification

Le développement tient en 5 sprints de 2 semaines : les 13 exigences M sont livrées à la fin du Sprint 3. L'ordre suit les dépendances : toute action suppose un utilisateur authentifié, et réserver suppose des salles.

| Sprint | Objectif du sprint | Exigences couvertes | Étape DevOps menée en parallèle |
| --- | --- | --- | --- |
| 1 | Un utilisateur se connecte et se déconnecte en sécurité | EF-AUTH-01 à EF-AUTH-04 | 1 Jira, 2 Git / GitHub |
| 2 | Un utilisateur trouve une salle libre | EF-AUTH-05 à EF-AUTH-07, EF-ROOM-01 à EF-ROOM-04 | 3 Jenkins |
| 3 | Un utilisateur réserve et annule sans conflit | EF-BOOK-01 à EF-BOOK-05, EF-ROOM-05, EF-ROOM-06 | 4 Docker |
| 4 | Les utilisateurs sont prévenus et les pannes suivies | EF-NOTIF-01 à EF-NOTIF-04, EF-INCID-01 à EF-INCID-03, EF-BOOK-06, EF-BOOK-07, EF-ROOM-07 | 5 Kubernetes, 6 Terraform |
| 5 | L'établissement pilote et sécurise la plateforme | EF-ADMIN-01 à EF-ADMIN-03, puis les exigences C selon la capacité restante | 7 Ansible, 8 DevSecOps |

Les 9 exigences C (EF-AUTH-08, EF-ROOM-08, EF-BOOK-08, EF-BOOK-09, EF-NOTIF-05, EF-NOTIF-06, EF-INCID-04, EF-INCID-05, EF-ADMIN-04) restent dans le backlog et entrent au Sprint 5 si la capacité le permet. EF-AUTH-09 (W) est hors V1.

### 8.1 Definition of Done

Un ticket passe à « Done » seulement si :

- ses critères d'acceptation sont tous vérifiés ;
- le code est fusionné par une Pull Request relue et approuvée, dont le titre porte la clé Jira ;
- le pipeline Jenkins est vert : lint ruff, typage mypy, tests pytest, quality gate SonarQube (ENF-11) ;
- les tests unitaires couvrent au moins 70 % du code ajouté ;
- le contrat OpenAPI généré par FastAPI est relu si l'API change ;
- aucune vulnérabilité critique ou haute n'est introduite (à partir de l'étape 8, ENF-04).

## 9. Livrables et recette

La V1 est acceptée si les 13 exigences M et au moins 15 des 18 exigences S passent leurs critères d'acceptation.

### 9.1 Livrables

| Livrable | Contenu | Échéance |
| --- | --- | --- |
| Cahier des charges | Ce document, validé par l'encadrant | Avant de compléter le TP 1 |
| Livrables du TP 1 | Captures du backlog et du Sprint 1 avec son workflow, deux Stories avec critères, clé Jira retenue, justification de la priorisation | Fin du TP 1 |
| Dépôt GitHub | Code source, historique lié aux clés Jira, Pull Requests | Chaque sprint |
| Pipeline d'intégration | Jenkinsfile, rapports de tests et SonarQube | Étape 3 |
| Conteneurs | Dockerfile de chaque composant, docker-compose | Étape 4 |
| Déploiement | Manifests Kubernetes | Étape 5 |
| Infrastructure | Code Terraform, playbooks Ansible | Étapes 6 et 7 |
| Sécurité | Rapport des analyses et des corrections apportées | Étape 8 |
| Recette | Cahier de recette et procès-verbal | Fin du Sprint 5 |
| Soutenance | Démonstration et rapport final | Fin du module |

### 9.2 Démarche de recette

- Chaque exigence M ou S a au moins un scénario au format « Étant donné… lorsque… alors… », repris de ses critères d'acceptation.
- Les scénarios sont automatisés quand c'est possible (tests d'API, Playwright), sinon exécutés à la main et consignés.
- Toute anomalie est saisie en Bug Jira, liée à l'exigence et à la Story concernées.
- Les exigences non fonctionnelles sont vérifiées selon la colonne « Vérification » de la section 5.

## Annexe A — Backlog initial Jira

Les six modules deviennent six Epics ; le Sprint 1 compte 6 tickets pour 16 points et livre la connexion (SC-11), ticket retenu pour le TP Git/GitHub.

Jira attribue les clés dans l'ordre de création : les numéros ci-dessous reprennent ceux de l'énoncé (SC-11 à SC-14) et sont à remplacer par ceux que Jira affiche.

### A.1 Epics

| Epic | Nom dans Jira | Exigences couvertes |
| --- | --- | --- |
| AUTH | Authentification et comptes | EF-AUTH-01 à EF-AUTH-09 |
| ROOM | Gestion des salles | EF-ROOM-01 à EF-ROOM-08 |
| BOOK | Réservation | EF-BOOK-01 à EF-BOOK-09 |
| NOTIF | Notifications | EF-NOTIF-01 à EF-NOTIF-06 |
| INCID | Incidents | EF-INCID-01 à EF-INCID-05 |
| ADMIN | Administration et pilotage | EF-ADMIN-01 à EF-ADMIN-04 |

### A.2 Sprint 1

Objectif : « Un utilisateur se connecte et se déconnecte en sécurité. » Tickets dans l'ordre du backlog :

| Clé | Type | Résumé | Priorité Jira | Estimation (points) | Labels | Exigences |
| --- | --- | --- | --- | --- | --- | --- |
| SC-12 | Task | Créer le modèle User et le service d'authentification | Highest | 3 | backend | EF-AUTH-01 |
| SC-11 | Story | Se connecter avec e-mail et mot de passe | Highest | 5 | auth, backend, frontend | EF-AUTH-01, EF-AUTH-03 |
| SC-14 | Task | Écrire les tests pytest du service d'authentification | High | 2 | tests | ENF-11 |
| SC-16 | Story | Bloquer le compte après 3 échecs consécutifs | High | 3 | auth, securite | EF-AUTH-04, RG-02 |
| SC-15 | Story | Se déconnecter | High | 2 | auth, frontend | EF-AUTH-02 |
| SC-13 | Bug | Message incorrect après trois échecs | Medium | 1 | auth, bug | EF-AUTH-03, RG-02 |

SC-12 se découpe en Sub-tasks : modèle SQLAlchemy User et migration Alembic, service d'authentification (bcrypt, PyJWT), route FastAPI POST /api/auth/login. Chaque ticket reçoit un responsable de l'équipe au moment de la planification.

Justification de la priorisation :

- La connexion conditionne tout le reste : sans utilisateur authentifié, ni recherche ni réservation n'a de sens.
- Ces tickets portent des exigences M et la sécurité d'accès (ENF-01 à ENF-03), qu'il vaut mieux poser dès le départ.
- SC-12 passe avant SC-11, car la Story dépend du modèle et du service.
- 16 points restent atteignables en 2 semaines et donnent un incrément démontrable ; le volume est à ajuster à la taille de l'équipe.
- Ni salles ni réservations dans ce sprint : le Sprint 1 vise un objectif atteignable, pas tout le backlog.

### A.3 Stories du Sprint 1 et critères d'acceptation

**SC-11 — Se connecter avec e-mail et mot de passe** (EF-AUTH-01, EF-AUTH-03, RG-11)

« En tant qu'étudiant, je veux me connecter avec mon e-mail institutionnel et mon mot de passe afin d'accéder aux services SmartCampus. »

- Étant donné un compte actif, lorsque je saisis un e-mail et un mot de passe corrects, alors j'arrive sur l'accueil et un jeton valable 30 min est émis.
- Étant donné un mot de passe incorrect, lorsque je valide, alors le message « E-mail ou mot de passe incorrect » s'affiche, sans dire lequel est faux.
- Étant donné une adresse hors du domaine de l'établissement, lorsque je valide, alors la connexion est refusée.
- Étant donné un compte désactivé, lorsque je valide, alors la connexion est refusée avec un message invitant à contacter l'administration.

**SC-15 — Se déconnecter** (EF-AUTH-02)

« En tant qu'utilisateur connecté, je veux me déconnecter afin que personne ne puisse utiliser ma session sur un poste partagé. »

- Lorsque je clique sur « Se déconnecter », alors je reviens à la page de connexion et le jeton est invalidé côté serveur.
- Étant donné un jeton invalidé, lorsqu'une requête l'utilise, alors l'API répond 401.
- Étant donné 30 min d'inactivité, lorsque je fais une action, alors la connexion m'est redemandée.

**SC-16 — Bloquer le compte après 3 échecs consécutifs** (EF-AUTH-04, RG-02)

« En tant qu'administrateur système, je veux que les échecs de connexion répétés bloquent le compte et soient journalisés afin de freiner et repérer les tentatives d'intrusion. »

- Étant donné 3 échecs consécutifs sur un compte, alors le compte est bloqué 15 min et un événement de sécurité est enregistré avec date, e-mail et adresse IP.
- Étant donné un compte bloqué, lorsque je saisis le bon mot de passe, alors la connexion est refusée avec un message indiquant d'attendre.
- Étant donné 2 échecs suivis d'une connexion réussie, alors le compteur d'échecs revient à zéro.

### A.4 Stories principales des autres Epics

| Epic | Story | Exigence |
| --- | --- | --- |
| ROOM | En tant qu'étudiant, je veux rechercher une salle libre par date, créneau et capacité afin de trouver vite où travailler en groupe. | EF-ROOM-02 |
| ROOM | En tant que gestionnaire, je veux créer et modifier les fiches des salles afin que capacités et équipements affichés soient exacts. | EF-ROOM-04 |
| BOOK | En tant qu'étudiant, je veux réserver une salle libre sur un créneau afin d'être sûr d'avoir un lieu de travail. | EF-BOOK-01 |
| BOOK | En tant qu'enseignant, je veux annuler ma réservation afin de libérer la salle pour d'autres. | EF-BOOK-04 |
| BOOK | En tant qu'enseignant, je veux réserver une salle chaque semaine jusqu'à la fin du semestre afin de ne pas refaire la demande à chaque séance. | EF-BOOK-07 |
| NOTIF | En tant qu'étudiant, je veux recevoir un rappel 1 h avant ma réservation afin de ne pas l'oublier. | EF-NOTIF-02 |
| INCID | En tant qu'enseignant, je veux signaler un vidéoprojecteur en panne afin qu'il soit réparé avant le prochain cours. | EF-INCID-01 |
| ADMIN | En tant que gestionnaire, je veux voir le taux d'occupation par salle et par semaine afin d'ajuster l'offre de salles. | EF-ADMIN-03 |

## Annexe B — Points à valider et glossaire

### B.1 Points à valider avec l'encadrant

- [ ] Faire valider la stack retenue par l'encadrant : FastAPI, React et PostgreSQL (section 6).
- [ ] Nombre et durée des sprints : 5 sprints de 2 semaines sont supposés, à caler sur le calendrier des TP.
- [ ] Valeurs des règles de gestion RG-02 à RG-09 : durées, quotas et délais proposés.
- [ ] Taille de l'équipe et rôles Scrum (Product Owner, Scrum Master, développeurs).
- [ ] Environnement des TP Kubernetes et Terraform : cluster local (Minikube, kind) ou cloud.
- [ ] Domaine e-mail de l'établissement à utiliser pour RG-11.
- [ ] Compléter l'équipe et l'encadrant dans la fiche projet (section 1.1).

### B.2 Glossaire

| Terme | Définition |
| --- | --- |
| Epic | Grand ensemble de besoins, trop large pour un seul sprint ; ici, un module |
| Story | Besoin exprimé du point de vue de l'utilisateur : « En tant que…, je veux… afin de… » |
| Task | Travail technique nécessaire à une Story |
| Sub-task | Découpage d'une Task ou d'une Story en unités plus petites |
| Bug | Anomalie à corriger dans un comportement attendu |
| Critère d'acceptation | Condition vérifiable qui dit si une Story est terminée |
| MoSCoW | Priorisation en Must, Should, Could, Won't |
| Definition of Done | Conditions communes à remplir par tout ticket avant « Done » |
| RBAC | Contrôle d'accès fondé sur le rôle de l'utilisateur |
| JWT | Jeton signé qui prouve l'identité de l'utilisateur à chaque appel de l'API |
| Check-in | Confirmation de présence au début d'une réservation |
| Non-présentation | Réservation non honorée faute de check-in (no-show) |
| CI/CD | Intégration et livraison continues par pipeline automatisé |
| SAST | Analyse statique de la sécurité du code source |
