# Emails Brevo — Webinaire AI Protect (5 octobre 2026)

Expéditeur : Puissance AI <contact@puissance.ai>. Personnalisation : `{{ contact.FIRSTNAME }}`. Liste cible : #22.

## Confirmation (automation à l'entrée dans la liste #22)

| Fichier | Template Brevo | Objet |
|---|---|---|
| `inscription-validee.html` | #48 — « Webinaire AI Protect — Inscription validée » | Votre inscription est confirmée : Webinaire IA en entreprise avec Puissance IA |

## Relances (campagnes programmées sur la liste #22)

| Fichier | Campagne Brevo | Envoi (Paris) | Objet |
|---|---|---|---|
| `relance-j5.html` | #51 — J-5 | mer. 30 sept. 08:30 | Votre entreprise a-t-elle déjà un cadre pour l'IA ? |
| `relance-j3.html` | #52 — J-3 | ven. 2 oct. 08:30 | Que devrait vraiment contenir votre charte IA ? |
| `relance-j1.html` | #53 — J-1 | dim. 4 oct. 09:00 | Demain, on parle de votre cadre IA |
| `relance-h1.html` | #54 — H-1 | lun. 5 oct. 07:30 | Dans une heure : IA en entreprise |

Les 4 relances sont générées par `generer-relances.py` (même gabarit que le site : Inter Tight, noir #121722, bleu #0068F9, papier #FAF9F7).
Pour modifier un email : éditer le script, le relancer, puis recoller le HTML dans la campagne Brevo correspondante.
