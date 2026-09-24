// Vercel Serverless Function — relais d'inscription vers Brevo.
// Reçoit le formulaire (JSON), crée/met à jour le contact dans la liste du webinaire.
// L'email de confirmation est envoyé par l'automation Brevo (déclenchée à l'entrée dans la liste).
//
// Variables d'environnement (Vercel → Settings → Environment Variables) :
//   BREVO_API_KEY   clé API v3 Brevo (obligatoire)
//   BREVO_LIST_ID   ID de la liste (défaut : 22 — « Webinar 5 octobre »)

const BREVO_API = 'https://api.brevo.com/v3';
const LIST_ID = Number(process.env.BREVO_LIST_ID || 22);

// Attributs de contact alimentés par le formulaire (créés à la volée s'ils n'existent pas).
const ATTRIBUTES = {
  WEBINAR_ORGANISATION: 'text',
  WEBINAR_TYPE_ORGA: 'text',
  WEBINAR_TAILLE_ORGA: 'text',
  WEBINAR_SITE_WEB: 'text',
  WEBINAR_PROJETS_IA: 'text',
  WEBINAR_REFERENT_IA: 'text',
  WEBINAR_COMITE_IA: 'text',
  WEBINAR_CHARTE_IA: 'text',
  WEBINAR_LOGICIEL_IA: 'text',
  WEBINAR_SOURCE: 'text',
  WEBINAR_INSCRIT_LE: 'date'
};

const MAX = { prenom: 80, nom: 80, email: 200, organisation: 150, site_web: 200, autre: 100 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

let attributesEnsured = false;

async function brevo(path, init = {}) {
  const res = await fetch(BREVO_API + path, {
    ...init,
    headers: {
      'api-key': process.env.BREVO_API_KEY,
      accept: 'application/json',
      'content-type': 'application/json',
      ...(init.headers || {})
    }
  });
  let data = null;
  try { data = await res.json(); } catch (_) { /* 204 sans corps */ }
  return { status: res.status, ok: res.ok, data };
}

// Crée les attributs manquants (idempotent : Brevo répond 400 « already exists » sinon).
async function ensureAttributes() {
  if (attributesEnsured) return;
  await Promise.all(Object.entries(ATTRIBUTES).map(([name, type]) =>
    brevo(`/contacts/attributes/normal/${name}`, { method: 'POST', body: JSON.stringify({ type }) })
  ));
  attributesEnsured = true;
}

const clean = (v, max = MAX.autre) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  }
  if (!process.env.BREVO_API_KEY) {
    console.error('[inscription] BREVO_API_KEY manquante');
    return res.status(500).json({ ok: false, error: 'server_misconfigured' });
  }

  const body = typeof req.body === 'string' ? safeJson(req.body) : (req.body || {});

  // Honeypot : un bot a rempli le champ caché → on répond OK sans rien faire.
  if (body.website_url) return res.status(200).json({ ok: true });

  const email = clean(body.email, MAX.email).toLowerCase();
  const prenom = clean(body.prenom, MAX.prenom);
  const nom = clean(body.nom, MAX.nom);
  const organisation = clean(body.organisation, MAX.organisation);
  if (!EMAIL_RE.test(email) || !prenom || !nom || !organisation || body.consentement_rgpd !== true) {
    return res.status(400).json({ ok: false, error: 'invalid_payload' });
  }

  const attributes = {
    FIRSTNAME: prenom,
    LASTNAME: nom,
    WEBINAR_ORGANISATION: organisation,
    WEBINAR_TYPE_ORGA: clean(body.type_organisation),
    WEBINAR_TAILLE_ORGA: clean(body.taille_organisation),
    WEBINAR_SITE_WEB: clean(body.site_web, MAX.site_web),
    WEBINAR_PROJETS_IA: clean(body.projets_ia),
    WEBINAR_REFERENT_IA: clean(body.referent_ia),
    WEBINAR_COMITE_IA: clean(body.comite_ia),
    WEBINAR_CHARTE_IA: clean(body.charte_ia),
    WEBINAR_LOGICIEL_IA: clean(body.logiciel_ia_officiel),
    WEBINAR_SOURCE: clean(body.source) || 'lp-webinaire-ai-protect',
    WEBINAR_INSCRIT_LE: new Date().toISOString().slice(0, 10)
  };
  // Brevo refuse les attributs vides pour certains types : on ne transmet que les valeurs renseignées.
  for (const k of Object.keys(attributes)) if (attributes[k] === '') delete attributes[k];

  const contact = { email, attributes, listIds: [LIST_ID], updateEnabled: true };

  try {
    await ensureAttributes();
    let r = await brevo('/contacts', { method: 'POST', body: JSON.stringify(contact) });

    // Contact déjà existant hors de la liste → l'ajouter explicitement (updateEnabled couvre le cas général).
    if (!r.ok && r.data && /already exist|duplicate_parameter/i.test(JSON.stringify(r.data))) {
      r = await brevo(`/contacts/lists/${LIST_ID}/contacts/add`, { method: 'POST', body: JSON.stringify({ emails: [email] }) });
    }

    if (!r.ok) {
      console.error('[inscription] Brevo a refusé la requête', r.status, r.data);
      return res.status(502).json({ ok: false, error: 'brevo_error' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[inscription] Erreur réseau Brevo', err);
    return res.status(502).json({ ok: false, error: 'brevo_unreachable' });
  }
}

function safeJson(s) { try { return JSON.parse(s); } catch (_) { return {}; } }
