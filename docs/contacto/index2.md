---
title: Contacto cifrado
description: Envíame un mensaje seguro con PGP
---

# Contacto cifrado con PGP

Si quieres comunicarte conmigo de forma segura, utiliza este formulario. Tu mensaje se cifrará con mi clave pública y necesito tu clave pública para responderte de forma cifrada. **Puedes pegar tu clave o generar una nueva abajo.**

---

## 📝 Enviar mensaje cifrado

<div class="pgp-contact">

<div class="form-group">
  <label for="userName">Tu nombre o alias:</label>
  <input type="text" id="userName" placeholder="Ej: Juan Pérez" value="">
  <small>Obligatorio para identificarte.</small>
</div>

<div class="form-group">
  <label for="userContact">Tu contacto (email, Telegram, etc.):</label>
  <input type="text" id="userContact" placeholder="ejemplo@dominio.com o @usuario" value="">
  <small>Obligatorio para que pueda responderte.</small>
</div>

<div class="form-group">
  <label for="senderPubKey">Tu clave pública (obligatoria):</label>
  <textarea id="senderPubKey" rows="6" placeholder="Pega aquí tu clave pública PGP..."></textarea>
  <small>Debe empezar por <code>-----BEGIN PGP PUBLIC KEY BLOCK-----</code>.</small>
  <button type="button" id="generateKeyBtn" style="margin-top: 0.5rem;">🔑 Generar nueva clave con mis datos</button>
</div>

<div id="keygenArea" style="display: none; margin-top: 1rem; padding: 1rem; border: 1px solid var(--md-default-fg-color--lighter); border-radius: 8px;">
  <div class="form-group">
    <label>Clave pública generada:</label>
    <textarea id="genPublicKey" rows="6" readonly style="font-family: monospace;"></textarea>
    <button id="copyPubToFormBtn">Usar esta clave pública</button>
    <button id="downloadPubBtn">Descargar clave pública (.asc)</button>
  </div>
  <div class="form-group">
    <label>Clave privada (descárgala y guárdala):</label>
    <textarea id="genPrivateKey" rows="6" readonly style="font-family: monospace;"></textarea>
    <button id="downloadPrivBtn">Descargar clave privada (.asc)</button>
  </div>
  <p class="warning">⚠️ Guarda tu clave privada. Sin ella no podrás descifrar mis respuestas.</p>
</div>

<div class="form-group">
  <label for="message">Tu mensaje (texto plano):</label>
  <textarea id="message" rows="6" placeholder="Escribe aquí tu mensaje..."></textarea>
</div>

<div class="form-group">
  <label for="encryptedResult">Mensaje cifrado (resultado):</label>
  <textarea id="encryptedResult" rows="8" readonly style="font-family: monospace;"></textarea>
  <small>Este es el texto cifrado. Puedes copiarlo por si acaso.</small>
</div>

<div class="form-group">
  <label for="status">Estado:</label>
  <div id="status" style="margin-top: 0.5rem;"></div>
</div>

<button id="encryptBtn">1. Cifrar mensaje</button>
<button id="copyBtn" disabled>2. Copiar mensaje cifrado</button>
<button id="sendBtn" disabled>3. Enviar mensaje</button>

</div>

<script src="https://jim88.pp.ua/js/openpgp.min.js"></script>
<script>
// ==================== TU CLAVE PÚBLICA ====================
const myPublicKeyArmored = `-----BEGIN PGP PUBLIC KEY BLOCK-----
Comment: User-ID:	JimPGP <pgp@jim88.pp.ua>
Comment: Created:	13/4/26 23:17
Comment: Type:	256-bit EdDSA (secret key available)
Comment: Usage:	Signing, Encryption, Certifying User-IDs
Comment: Fingerprint:	0823D12E56A3D4EB5F4A809FF10D59422F64CE6E

mDMEad1dZBYJKwYBBAHaRw8BAQdAm/+1BydAgefBb1MyVoz4APWag2UiJRfrJKc8
X0trBBi0GEppbVBHUCA8cGdwQGppbTg4LnBwLnVhPoiMBBAWCgA+BYJp3V1kBAsJ
BwgJkPENWUIvZM5uAxUICgQWAAIBAhkBApsDAh4BFiEECCPRLlaj1OtfSoCf8Q1Z
Qi9kzm4AAPU3AQDhpBZdKVjWPYgcQ0IZSgKGSba0bTHJ7dGThK73EX/vjAEAsD6l
bUoWYnVcX5DQUeiJswwMEOX0Cr1CxxZPKlhbaQe4OARp3V1kEgorBgEEAZdVAQUB
AQdAIXUE+NXLVgH6MSVQXLuCXukHbeee0p9wBWoK56uOIn8DAQgHiHgEGBYKACoF
gmndXWQJkPENWUIvZM5uApsMFiEECCPRLlaj1OtfSoCf8Q1ZQi9kzm4AAI30AP9Z
L6iLD+uiKRyyrzsuiVi9khYu7KvWufgogGw34cDmRgEAiXFIopBdM7VeGWh1NYWn
CjNU4RXQh7L+8+Y/vLE+Jwg=
=XRPp
-----END PGP PUBLIC KEY BLOCK-----`;

// ==================== DOM Elements ====================
const userNameEl = document.getElementById('userName');
const userContactEl = document.getElementById('userContact');
const senderKeyEl = document.getElementById('senderPubKey');
const messageEl = document.getElementById('message');
const encryptedResultEl = document.getElementById('encryptedResult');
const statusEl = document.getElementById('status');
const encryptBtn = document.getElementById('encryptBtn');
const copyBtn = document.getElementById('copyBtn');
const sendBtn = document.getElementById('sendBtn');
const generateKeyBtn = document.getElementById('generateKeyBtn');
const keygenArea = document.getElementById('keygenArea');
const genPublicKey = document.getElementById('genPublicKey');
const genPrivateKey = document.getElementById('genPrivateKey');
const copyPubToFormBtn = document.getElementById('copyPubToFormBtn');
const downloadPubBtn = document.getElementById('downloadPubBtn');
const downloadPrivBtn = document.getElementById('downloadPrivBtn');

let currentEncrypted = '';
let lastGeneratedPublic = '';
let lastGeneratedPrivate = '';

function setStatus(text, isError = false) {
  statusEl.innerHTML = `<span style="color: ${isError ? 'red' : 'green'};">${text}</span>`;
}

function isPublicKeyValid(pubKey) {
  const trimmed = pubKey.trim();
  return trimmed.startsWith('-----BEGIN PGP PUBLIC KEY BLOCK-----') &&
         trimmed.endsWith('-----END PGP PUBLIC KEY BLOCK-----');
}

// Cifrado con timeout
async function encryptMessageWithTimeout(publicKeyArmored, plaintext, timeoutMs = 30000) {
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Tiempo de espera agotado. Recarga la página.')), timeoutMs)
  );
  const encryptPromise = (async () => {
    const publicKey = await openpgp.readKey({ armoredKey: publicKeyArmored });
    const message = await openpgp.createMessage({ text: plaintext });
    return await openpgp.encrypt({ message, encryptionKeys: publicKey });
  })();
  return await Promise.race([encryptPromise, timeoutPromise]);
}

// Generar clave usando nombre y contacto
async function generateKeyWithNameAndContact(name, contact) {
  let userID = name;
  if (contact) userID += ` <${contact}>`;
  return await openpgp.generateKey({
    type: 'ecc',
    curve: 'ed25519',
    userIDs: [{ name: userID }],
    format: 'armored'
  });
}

// Descargar archivo
function downloadKey(key, filename) {
  const blob = new Blob([key], { type: 'application/pgp-keys' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// === Botón Generar clave ===
generateKeyBtn.addEventListener('click', async () => {
  const name = userNameEl.value.trim();
  const contact = userContactEl.value.trim();
  if (!name) {
    setStatus('❌ Introduce tu nombre o alias antes de generar la clave.', true);
    return;
  }
  generateKeyBtn.disabled = true;
  generateKeyBtn.textContent = 'Generando...';
  keygenArea.style.display = 'none';
  try {
    const { privateKey, publicKey } = await generateKeyWithNameAndContact(name, contact);
    lastGeneratedPublic = publicKey;
    lastGeneratedPrivate = privateKey;
    genPublicKey.value = publicKey;
    genPrivateKey.value = privateKey;
    keygenArea.style.display = 'block';
    setStatus('✅ Claves generadas. Puedes usarlas o copiarlas al formulario.');
  } catch (err) {
    console.error(err);
    setStatus('❌ Error al generar claves: ' + err.message, true);
  } finally {
    generateKeyBtn.disabled = false;
    generateKeyBtn.textContent = '🔑 Generar nueva clave con mis datos';
  }
});

// Usar la clave pública generada en el formulario
copyPubToFormBtn.addEventListener('click', () => {
  if (!lastGeneratedPublic) {
    setStatus('❌ Primero genera las claves.', true);
    return;
  }
  senderKeyEl.value = lastGeneratedPublic;
  setStatus('✅ Clave pública añadida al formulario. Ahora puedes continuar.');
  // Opcional: cerrar el área de generación (pero no es necesario)
  // keygenArea.style.display = 'none';
});

downloadPubBtn.addEventListener('click', () => {
  if (!lastGeneratedPublic) {
    setStatus('❌ Primero genera las claves.', true);
    return;
  }
  const name = userNameEl.value.trim().replace(/\s+/g, '_') || 'anonymous';
  downloadKey(lastGeneratedPublic, `${name}_public.asc`);
});

downloadPrivBtn.addEventListener('click', () => {
  if (!lastGeneratedPrivate) {
    setStatus('❌ Primero genera las claves.', true);
    return;
  }
  const name = userNameEl.value.trim().replace(/\s+/g, '_') || 'anonymous';
  downloadKey(lastGeneratedPrivate, `${name}_private.asc`);
});

// === Cifrar mensaje ===
encryptBtn.addEventListener('click', async () => {
  const name = userNameEl.value.trim();
  const contact = userContactEl.value.trim();
  const plaintext = messageEl.value.trim();
  const senderPubKey = senderKeyEl.value.trim();

  if (!name) {
    setStatus('❌ Introduce tu nombre o alias.', true);
    return;
  }
  if (!contact) {
    setStatus('❌ Introduce tu contacto (email, Telegram, etc.).', true);
    return;
  }
  if (!plaintext) {
    setStatus('❌ Escribe un mensaje.', true);
    return;
  }
  if (!senderPubKey) {
    setStatus('❌ Debes proporcionar tu clave pública (puedes generar una arriba).', true);
    return;
  }
  if (!isPublicKeyValid(senderPubKey)) {
    setStatus('❌ La clave pública no tiene el formato correcto.', true);
    return;
  }

  setStatus('🔐 Cifrando mensaje...');
  encryptBtn.disabled = true;
  copyBtn.disabled = true;
  sendBtn.disabled = true;
  encryptedResultEl.value = '';

  try {
    let fullMessage = `De: ${name} (${contact})\n\n${plaintext}\n\n--- Clave pública del remitente ---\n${senderPubKey}`;
    const encrypted = await encryptMessageWithTimeout(myPublicKeyArmored, fullMessage);
    currentEncrypted = encrypted;
    encryptedResultEl.value = encrypted;
    setStatus('✅ Mensaje cifrado correctamente. Ahora puedes copiarlo o enviarlo.');
    copyBtn.disabled = false;
    sendBtn.disabled = false;
  } catch (err) {
    console.error(err);
    setStatus(`❌ Error al cifrar: ${err.message}`, true);
    encryptBtn.disabled = false;
  }
});

// Copiar mensaje cifrado
copyBtn.addEventListener('click', async () => {
  if (!currentEncrypted) {
    setStatus('❌ No hay mensaje cifrado.', true);
    return;
  }
  try {
    await navigator.clipboard.writeText(currentEncrypted);
    setStatus('📋 Mensaje cifrado copiado al portapapeles.');
  } catch (err) {
    setStatus('❌ No se pudo copiar automáticamente. Selecciona y copia manualmente.', true);
  }
});

// Enviar al Worker
async function sendWithRetry(url, data, retries = 1) {
  for (let i = 0; i <= retries; i++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        signal: controller.signal
      });
      clearTimeout(timeoutId);
      if (response.ok) return { ok: true };
      else return { ok: false, error: await response.text() };
    } catch (err) {
      if (i === retries) return { ok: false, error: err.message };
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  return { ok: false, error: 'Máximo de reintentos' };
}

sendBtn.addEventListener('click', async () => {
  if (!currentEncrypted) {
    setStatus('❌ Primero cifra el mensaje.', true);
    return;
  }
  setStatus('📡 Enviando mensaje cifrado...');
  sendBtn.disabled = true;
  copyBtn.disabled = true;
  const result = await sendWithRetry('https://contacto.jim88.pp.ua', { text: currentEncrypted }, 1);
  if (result.ok) {
    setStatus('✅ Mensaje enviado correctamente. Recibiré tu mensaje cifrado.');
    // Limpiar todo
    userNameEl.value = '';
    userContactEl.value = '';
    senderKeyEl.value = '';
    messageEl.value = '';
    encryptedResultEl.value = '';
    currentEncrypted = '';
    copyBtn.disabled = true;
    sendBtn.disabled = true;
    const oldDiv = document.getElementById('manualInstructions');
    if (oldDiv) oldDiv.remove();
  } else {
    setStatus(`❌ Error al enviar: ${result.error}.`, true);
    let manualDiv = document.getElementById('manualInstructions');
    if (!manualDiv) {
      manualDiv = document.createElement('div');
      manualDiv.id = 'manualInstructions';
      manualDiv.style.marginTop = '1rem';
      manualDiv.style.padding = '0.5rem';
      manualDiv.style.backgroundColor = '#f8f9fa';
      manualDiv.style.border = '1px solid #ccc';
      manualDiv.style.borderRadius = '4px';
      document.querySelector('.pgp-contact').appendChild(manualDiv);
    }
    manualDiv.innerHTML = `
      <strong>⚠️ Envío automático falló. Puedes enviar el mensaje manualmente:</strong><br>
      Copia el texto cifrado de arriba y envíalo por correo a <strong>pgp@jim88.pp.ua</strong>.<br>
      Si el problema persiste, recarga la página e intenta de nuevo.
    `;
    sendBtn.disabled = false;
    copyBtn.disabled = false;
  }
});

// Limpiar mensaje manual si hay cambios
function resetManual() {
  const div = document.getElementById('manualInstructions');
  if (div) div.remove();
}
userNameEl.addEventListener('input', resetManual);
userContactEl.addEventListener('input', resetManual);
messageEl.addEventListener('input', resetManual);
senderKeyEl.addEventListener('input', resetManual);
</script>

<style>
.pgp-contact textarea, .pgp-contact input {
  width: 100%;
  box-sizing: border-box;
  margin: 0.5rem 0;
  padding: 0.5rem;
  font-family: monospace;
}
button {
  margin: 0.25rem;
  padding: 0.5rem 1rem;
  background-color: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: var(--md-accent-fg-color);
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.form-group {
  margin-bottom: 1rem;
}
small {
  display: block;
  margin-top: -0.25rem;
  color: #666;
}
.warning {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #fff3cd;
  color: #856404;
  border-radius: 4px;
}
</style>
