#!/usr/bin/env python3
"""Génère les 4 emails de relance (J-5, J-3, J-1, H-1) dans la charte graphique du site."""
import json, os

MEET = "https://meet.google.com/mhs-fuic-iiz"
FONT = "font-family:'Inter Tight',Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;"

def p(txt, **kw):
    color = kw.get("color", "#4C4F57"); mb = kw.get("mb", 16)
    return f'<p style="margin:0 0 {mb}px;color:{color};">{txt}</p>'

def strong(t): return f'<strong style="color:#121722;font-weight:600;">{t}</strong>'

def questions(items):
    rows = "<br>".join(items)
    return f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:4px 0 20px;">
          <tr><td style="padding:14px 18px;border-left:3px solid #0068F9;background:#FAF9F7;border-radius:0 10px 10px 0;font-size:16px;line-height:26px;color:#121722;font-weight:500;">{rows}</td></tr>
        </table>'''

def arrows(items):
    rows = "".join(f'<tr><td style="padding:5px 0;font-size:16px;line-height:24px;color:#121722;"><span style="color:#0068F9;font-weight:600;">&rarr;</span>&nbsp; {i}</td></tr>' for i in items)
    return f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 18px;">{rows}</table>'

def quote(t):
    return f'<p style="margin:8px 0 18px;font-size:22px;line-height:30px;letter-spacing:-0.02em;font-weight:600;color:#121722;">{t}</p>'

def shell(*, title_html, badge, subtitle, preheader, body_html, cta_label, date_label, date_sub, sign):
    return f'''<!DOCTYPE html>
<html lang="fr" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>Webinaire AI Protect</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
<style>
  body {{ margin:0; padding:0; background:#FAF9F7; -webkit-font-smoothing:antialiased; }}
  table {{ border-collapse:collapse; }}
  img {{ border:0; display:block; }}
  a {{ color:#0068F9; }}
  .btn:hover {{ background:#0057D6 !important; }}
  @media (max-width:600px) {{
    .wrap {{ width:100% !important; }}
    .px {{ padding-left:24px !important; padding-right:24px !important; }}
    .h1 {{ font-size:26px !important; line-height:32px !important; }}
    .cd {{ display:block !important; width:100% !important; border-right:0 !important; }}
  }}
</style>
</head>
<body style="margin:0;padding:0;background:#FAF9F7;">
<div style="display:none;max-height:0;overflow:hidden;font-size:1px;line-height:1px;color:#FAF9F7;">{preheader}&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#FAF9F7;">
<tr><td align="center" style="padding:32px 16px;">

<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;">

  <tr><td class="px" style="padding:0 8px 20px;{FONT}">
    <span style="font-size:22px;font-weight:600;letter-spacing:-0.03em;color:#121722;">&#10042;&nbsp; Puissance<sup style="font-size:10px;font-weight:600;margin-left:2px;">AI</sup></span>
  </td></tr>

  <tr><td style="background:#FFFFFF;border:1px solid #E4E2DD;border-radius:18px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0">

      <tr><td class="px" style="background:#121722;border-radius:18px 18px 0 0;padding:36px 40px 32px;{FONT}">
        <table role="presentation" cellpadding="0" cellspacing="0"><tr>
          <td style="background:#0068F9;border-radius:999px;padding:5px 12px;font-size:12px;font-weight:600;color:#FFFFFF;letter-spacing:0.02em;">{badge}</td>
        </tr></table>
        <h1 class="h1" style="margin:18px 0 0;font-size:30px;line-height:36px;font-weight:600;letter-spacing:-0.03em;color:#FFFFFF;">{title_html}</h1>
        <p style="margin:12px 0 0;font-size:15px;line-height:22px;color:rgba(255,255,255,0.7);">{subtitle}</p>
      </td></tr>

      <tr><td class="px" style="padding:28px 40px 8px;{FONT}font-size:16px;line-height:25px;color:#4C4F57;">
        {p("Bonjour{% if contact.FIRSTNAME %} {{ contact.FIRSTNAME }}{% endif %},", color="#121722")}
        {body_html}
      </td></tr>

      <tr><td class="px" style="padding:12px 40px 0;{FONT}">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#FAF9F7;border:1px solid #E4E2DD;border-radius:14px;">
          <tr>
            <td class="cd" width="50%" style="padding:18px 20px;vertical-align:top;border-right:1px solid #E4E2DD;">
              <div style="font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#777C86;font-weight:500;">&#128197;&nbsp; {date_label}</div>
              <div style="margin-top:6px;font-size:17px;font-weight:600;letter-spacing:-0.01em;color:#121722;">{date_sub}</div>
            </td>
            <td class="cd" width="50%" style="padding:18px 20px;vertical-align:top;">
              <div style="font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#777C86;font-weight:500;">&#128187;&nbsp; En direct sur Google Meet</div>
              <div style="margin-top:6px;font-size:14px;line-height:20px;"><a href="{MEET}" style="color:#0057D6;font-weight:600;text-decoration:underline;word-break:break-all;">meet.google.com/mhs-fuic-iiz</a></div>
            </td>
          </tr>
        </table>
      </td></tr>

      <tr><td class="px" style="padding:20px 40px 12px;{FONT}">
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr>
          <td align="center" style="border-radius:8px;background:#0068F9;">
            <a class="btn" href="{MEET}" style="display:block;padding:16px 24px;font-size:16px;font-weight:600;color:#FFFFFF;text-decoration:none;border-radius:8px;">{cta_label} &nbsp;&rarr;</a>
          </td>
        </tr></table>
        <p style="margin:12px 0 0;font-size:13px;line-height:20px;color:#777C86;text-align:center;">Lien direct&nbsp;: <a href="{MEET}" style="color:#0057D6;">{MEET}</a></p>
      </td></tr>

      <tr><td class="px" style="padding:16px 40px 36px;{FONT}">
        <p style="margin:0;font-size:16px;line-height:25px;color:#4C4F57;">{sign}<br><strong style="color:#121722;font-weight:600;">L'équipe Puissance AI</strong></p>
      </td></tr>

    </table>
  </td></tr>

  <tr><td class="px" style="padding:24px 8px 0;{FONT}font-size:12px;line-height:18px;color:#777C86;">
    Puissance AI · 5 rue Jean Montavont, 68200 Mulhouse, France · <a href="mailto:contact@puissance.ai" style="color:#777C86;">contact@puissance.ai</a><br>
    Vous recevez cet email parce que vous vous êtes inscrit(e) au webinaire AI Protect. <a href="{{{{ unsubscribe }}}}" style="color:#777C86;">Se désinscrire</a>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>
'''

EM = lambda t: f'<em style="font-family:\'Instrument Serif\',Georgia,\'Times New Roman\',serif;font-style:italic;font-weight:400;color:#7DB2FF;">{t}</em>'

EMAILS = {
 "j-5": dict(
  name="Webinaire AI Protect — J-5",
  subject="Votre entreprise a-t-elle déjà un cadre pour l'IA ?",
  preheader="Savez-vous comment vos équipes utilisent aujourd'hui l'IA ? Rendez-vous dans 5 jours.",
  scheduled="2026-09-30T08:30:00+02:00",
  html=shell(
   badge="J-5 · Webinaire AI Protect",
   title_html=f"Votre entreprise a-t-elle déjà un {EM('cadre')} pour l'IA&nbsp;?",
   subtitle="Webinaire Puissance AI × Sparlann · Lundi 5 octobre, 8h30",
   preheader="Savez-vous comment vos équipes utilisent aujourd'hui l'IA ? Rendez-vous dans 5 jours.",
   body_html=(
    p("Dans 5 jours, nous nous retrouverons pour parler de charte IA.")
    + p("Mais commençons par une question simple&nbsp;:", mb=8)
    + quote("Savez-vous comment vos équipes utilisent aujourd'hui l'IA&nbsp;?")
    + questions(["ChatGPT avec un compte personnel&nbsp;?", "Un outil gratuit&nbsp;?", "Une IA intégrée à un logiciel métier&nbsp;?", "Des données clients dans les prompts&nbsp;?", "Des documents internes&nbsp;?", "Des usages dont la direction n'a jamais été informée&nbsp;?"])
    + p("L'IA peut s'installer très rapidement dans les pratiques quotidiennes.")
    + p(f"Le sujet n'est donc plus seulement de décider {strong('si')} votre entreprise va utiliser l'IA. Il faut aussi savoir {strong('dans quel cadre')} elle peut être utilisée.")
    + p("Et depuis le 2 février 2025, l'article 4 de l'AI Act impose aux fournisseurs et déployeurs de prendre des mesures adaptées pour soutenir la culture IA des personnes qui utilisent ces systèmes pour leur compte.")
    + p(f"Dans 5 jours, nous verrons comment aborder concrètement ces questions avec notre partenaire juridique {strong('Sparlann')}.", mb=8)
   ),
   cta_label="Votre lien de connexion", date_label="Date", date_sub="Lundi 5 octobre à 8h30",
   sign="À la semaine prochaine,")),

 "j-3": dict(
  name="Webinaire AI Protect — J-3",
  subject="Que devrait vraiment contenir votre charte IA ?",
  preheader="Si vous deviez rédiger votre charte demain, que mettriez-vous dedans ?",
  scheduled="2026-10-02T08:30:00+02:00",
  html=shell(
   badge="J-3 · Webinaire AI Protect",
   title_html=f"Que devrait {EM('vraiment')} contenir votre charte IA&nbsp;?",
   subtitle="Webinaire Puissance AI × Sparlann · Lundi 5 octobre, 8h30",
   preheader="Si vous deviez rédiger votre charte demain, que mettriez-vous dedans ?",
   body_html=(
    p("Dans 3 jours, nous parlerons de charte IA.")
    + p("Mais avant le webinaire, posez-vous cette question&nbsp;:", mb=8)
    + quote("Si vous deviez rédiger votre charte demain, que mettriez-vous dedans&nbsp;?")
    + questions(["Les outils autorisés&nbsp;?", "Les usages interdits&nbsp;?", "Les comptes personnels&nbsp;?", "Les données confidentielles&nbsp;?", "Les responsabilités des collaborateurs&nbsp;?", "Les règles en cas de doute ou d'incident&nbsp;?", "La gestion des nouveaux outils&nbsp;?", "La formation&nbsp;?"])
    + p("Ce sont précisément les questions auxquelles une charte doit pouvoir apporter des réponses.")
    + p(f"Et surtout, ces réponses doivent pouvoir être {strong('comprises et utilisées par les équipes')}.")
    + p("La CNIL recommande d'ailleurs aux organisations d'encadrer l'utilisation de l'IA générative par des politiques ou chartes internes définissant clairement les usages autorisés et interdits, et souligne l'importance de l'intelligibilité des documents et de la formation des utilisateurs.")
    + p(f"Nous verrons comment passer de ces principes à un cadre réellement adapté à votre entreprise avec notre partenaire juridique {strong('Sparlann')}.", mb=8)
   ),
   cta_label="Je rejoins le webinaire", date_label="Date", date_sub="Lundi 5 octobre à 8h30",
   sign="À lundi,")),

 "j-1": dict(
  name="Webinaire AI Protect — J-1",
  subject="Demain, on parle de votre cadre IA",
  preheader="Tout autoriser ? Tout interdire ? Ou construire un cadre qui protège votre entreprise ?",
  scheduled="2026-10-04T09:00:00+02:00",
  html=shell(
   badge="Demain · Webinaire AI Protect",
   title_html=f"Demain, on parle de {EM('votre')} cadre IA",
   subtitle="IA en entreprise : reprendre le contrôle sans freiner les usages",
   preheader="Tout autoriser ? Tout interdire ? Ou construire un cadre qui protège votre entreprise ?",
   body_html=(
    quote("C'est demain.")
    + p("L'IA est déjà utilisée dans les entreprises.")
    + p("Mais entre un collaborateur qui utilise un compte gratuit, un autre qui travaille avec des données confidentielles et un nouvel outil qui apparaît chaque semaine… " + strong("où placez-vous le curseur&nbsp;?"))
    + questions(["Tout autoriser&nbsp;?", "Tout interdire&nbsp;?", "Ou construire un cadre qui permette à vos équipes d'utiliser l'IA tout en protégeant votre entreprise&nbsp;?"])
    + p(f"C'est précisément ce que nous allons explorer demain avec notre partenaire juridique {strong('Sparlann')}.")
    + p("Nous parlerons notamment&nbsp;:", mb=8)
    + arrows(["des usages réels de l'IA en entreprise", "des comptes personnels et outils gratuits", "des données à protéger", "des responsabilités", "de la charte IA", "du rôle du dirigeant", "et de la manière de poser un cadre réellement applicable."])
    + p(strong("Prévoyez votre café. Et surtout, vos questions."), mb=8)
   ),
   cta_label="Votre lien pour participer", date_label="Demain", date_sub="Lundi 5 octobre à 8h30",
   sign="À demain,")),

 "h-1": dict(
  name="Webinaire AI Protect — H-1",
  subject="Dans une heure : IA en entreprise",
  preheader="Rendez-vous à 8h30 sur Google Meet. Le lien est dans cet email.",
  scheduled="2026-10-05T07:30:00+02:00",
  html=shell(
   badge="Dans une heure",
   title_html=f"IA en entreprise&nbsp;: reprendre le {EM('contrôle')} sans freiner les usages",
   subtitle="Rendez-vous à 8h30 · En direct sur Google Meet",
   preheader="Rendez-vous à 8h30 sur Google Meet. Le lien est dans cet email.",
   body_html=(
    p("Dans une heure, nous nous retrouvons pour notre webinaire.")
    + p("Une heure pour parler très concrètement de ce qui se passe déjà dans les entreprises&nbsp;:", mb=8)
    + questions(["Vos équipes utilisent-elles des comptes personnels&nbsp;?", "Quels outils sont autorisés&nbsp;?", "Quelles données peuvent être transmises à une IA&nbsp;?", "Que doit contenir une charte IA&nbsp;?", "Qui décide et que faire lorsqu'un collaborateur a un doute&nbsp;?"])
    + p(f"Nous poserons ces questions avec notre partenaire juridique {strong('Sparlann')}.")
    + p(strong("Pas de théorie déconnectée du terrain.") + " L'objectif est de vous aider à prendre du recul sur vos propres usages et sur le cadre que vous avez, ou pas encore, posé dans votre entreprise.", mb=8)
   ),
   cta_label="Rejoindre le webinaire maintenant", date_label="Rendez-vous", date_sub="Aujourd'hui à 8h30",
   sign="À tout de suite,")),
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "emails_out"); os.makedirs(out, exist_ok=True)
    for k, e in EMAILS.items():
        open(os.path.join(out, f"relance-{k}.html"), "w").write(e["html"])
    json.dump({k: {kk: vv for kk, vv in e.items()} for k, e in EMAILS.items()}, open(os.path.join(out, "emails.json"), "w"), ensure_ascii=False)
    print("ok", list(EMAILS))
