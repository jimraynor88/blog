---
title: Contacto cifrado
description: Envíame un mensaje seguro con PGP
---

# Contacto cifrado con PGP

Si quieres comunicarte conmigo de forma segura, utiliza este formulario. Tu mensaje se cifrará con mi clave pública y **debes incluir tu clave pública** para que pueda responderte de forma cifrada. Si no tienes una, puedes generar una abajo.

---

## 📝 Enviar mensaje cifrado

<div class="pgp-contact">

<div class="form-group">
  <label for="message">Tu mensaje (texto plano):</label>
  <textarea id="message" rows="6" placeholder="Escribe aquí tu mensaje..."></textarea>
</div>

<div class="form-group">
  <label for="contact">Tu contacto (email, Telegram, etc.):</label>
  <input type="text" id="contact" placeholder="ejemplo@dominio.com o @usuario" value="">
  <small>Obligatorio para que pueda responderte.</small>
</div>

<div class="form-group">
  <label for="senderPubKey">Tu clave pública (obligatoria):</label>
  <textarea id="senderPubKey" rows="6" placeholder="Pega aquí tu clave pública PGP..."></textarea>
  <small>Debe empezar por <code>-----BEGIN PGP PUBLIC KEY BLOCK-----</code> y terminar con <code>-----END PGP PUBLIC KEY BLOCK-----</code>.</small>
</div>

<div class="form-group">
  <label for="encryptedResult">Mensaje cifrado (resultado):</label>
  <textarea id="encryptedResult" rows="8" readonly style="font-family: monospace;"></textarea>
  <small>Este es el texto cifrado. Puedes copiarlo y guardarlo por si acaso.</small>
</div>

<div class="form-group">
  <label for="status">Estado:</label>
  <div id="status" style="margin-top: 0.5rem;"></div>
</div>

<button id="encryptBtn">1. Cifrar mensaje</button>
<button id="copyBtn" disabled>2. Copiar mensaje cifrado</button>
<button id="sendBtn" disabled>3. Enviar mensaje</button>

</div>

---

## 🔑 Generar nueva clave PGP (si no tienes)

Rellena tu nombre y contacto (opcional), genera un par de claves y luego copia la clave pública al formulario de arriba.

<div class="keygen-inline">

<div class="form-group">
  <label for="genName">Nombre / Alias:</label>
  <input type="text" id="genName" placeholder="Tu nombre o nick" value="Anónimo">
</div>

<div class="form-group">
  <label for="genContact">Contacto (email, Telegram, etc.):</label>
  <input type="text" id="genContact" placeholder="ejemplo@dominio.com o @usuario">
  <small>Opcional. Se incluirá en la clave.</small>
</div>

<button id="genKeyBtn">Generar par de claves</button>

<div id="genResult" style="display: none; margin-top: 1rem;">
  <div class="form-group">
    <label>Clave pública generada:</label>
    <textarea id="genPublicKey" rows="6" readonly style="font-family: monospace;"></textarea>
    <button id="copyPubToFormBtn">Copiar clave pública al formulario</button>
    <button id="downloadPubBtn">Descargar clave pública (.asc)</button>
  </div>
  <div class="form-group">
    <label>Clave privada (descárgala y guárdala):</label>
    <textarea id="genPrivateKey" rows="6" readonly style="font-family: monospace;"></textarea>
    <button id="downloadPrivBtn">Descargar clave privada (.asc)</button>
  </div>
  <p class="warning">⚠️ La clave privada es única. Guárdala en un lugar seguro. No la pierdas.</p>
</div>

</div>

<script src="https://jim88.pp.ua/js/openpgp.min.js"></script>
<script>
// ==================== TU CLAVE PÚBLICA (actualizada) ====================
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

// ==================== ELEMENTOS DEL FORMULARIO PRINCIPAL ====================
const messageEl = document.getElementById('message');
const contactEl = document.getElementById('contact');
const senderKeyEl = document.getElementById('senderPubKey');
const encryptedResultEl = document.getElementById('encryptedResult');
const statusEl = document.getElementById('status');
const encryptBtn = document.getElementById('encryptBtn');
const copyBtn = document.getElementById('copyBtn');
const sendBtn = document.getElementById('sendBtn');

let currentEncrypted = '';

// Función para mostrar mensajes de estado
function setStatus(text, isError = false) {
  statusEl.innerHTML = `<span style="color: ${isError ? 'red' : 'green'};">${text}</span>`;
}

// Validación de clave pública (formato básico)
function isPublicKeyValid(pubKey) {
  const trimmed = pubKey.trim();
  return trimmed.startsWith('-----BEGIN PGP PUBLIC KEY BLOCK-----') && 
         trimmed.endsWith('-----END PGP PUBLIC KEY BLOCK-----');
}

// Cifrado con timeout
async function encryptMessageWithTimeout(publicKeyArmored, plaintext, signKeyArmored = null, timeoutMs = 30000) {
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Tiempo de espera agotado al cifrar. Recarga la página y vuelve a intentarlo.')), timeoutMs)
  );
  const encryptPromise = (async () => {
    const publicKey = await openpgp.readKey({ armoredKey: publicKeyArmored });
    const options = {
      message: await openpgp.createMessage({ text: plaintext }),
      encryptionKeys: publicKey,
    };
    if (signKeyArmored && signKeyArmored.trim()) {
      const privateKey = await openpgp.readPrivateKey({ armoredKey: signKeyArmored });
      options.signingKeys = privateKey;
    }
    return await openpgp.encrypt(options);
  })();
  return await Promise.race([encryptPromise, timeoutPromise]);
}

// Cifrar mensaje
encryptBtn.addEventListener('click', async () => {
  const plaintext = messageEl.value.trim();
  const contact = contactEl.value.trim();
  const senderPubKey = senderKeyEl.value.trim();
  
  if (!plaintext) {
    setStatus('❌ Escribe un mensaje.', true);
    return;
  }
  if (!contact) {
    setStatus('❌ Indica un contacto (email, Telegram, etc.).', true);
    return;
  }
  if (!senderPubKey) {
    setStatus('❌ Debes proporcionar tu clave pública (puedes generar una abajo).', true);
    return;
  }
  if (!isPublicKeyValid(senderPubKey)) {
    setStatus('❌ La clave pública no tiene el formato correcto. Debe empezar y terminar con las cabeceras PGP.', true);
    return;
  }

  setStatus('🔐 Cifrando mensaje... (puede tardar unos segundos)');
  encryptBtn.disabled = true;
  copyBtn.disabled = true;
  sendBtn.disabled = true;
  encryptedResultEl.value = '';

  try {
    let fullMessage = `Mensaje de: ${contact}\n\n${plaintext}\n\n--- Clave pública del remitente ---\n${senderPubKey}`;
    const encrypted = await encryptMessageWithTimeout(myPublicKeyArmored, fullMessage);
    currentEncrypted = encrypted;
    encryptedResultEl.value = encrypted;
    setStatus('✅ Mensaje cifrado correctamente. Ya puedes copiarlo o enviarlo.');
    copyBtn.disabled = false;
    sendBtn.disabled = false;
  } catch (err) {
    console.error(err);
    setStatus(`❌ Error al cifrar: ${err.message}.`, true);
    encryptBtn.disabled = false;
  } finally {
    encryptBtn.disabled = false;
  }
});

// Copiar mensaje cifrado
copyBtn.addEventListener('click', async () => {
  if (!currentEncrypted) {
    setStatus('❌ No hay mensaje cifrado para copiar.', true);
    return;
  }
  try {
    await navigator.clipboard.writeText(currentEncrypted);
    setStatus('📋 Mensaje cifrado copiado al portapapeles.');
  } catch (err) {
    setStatus('❌ No se pudo copiar automáticamente. Selecciona y copia manualmente.', true);
  }
});

// Enviar al Worker con timeout y reintento
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
      if (response.ok) {
        return { ok: true, status: response.status };
      } else {
        const errorText = await response.text();
        return { ok: false, status: response.status, error: errorText };
      }
    } catch (err) {
      if (i === retries) {
        return { ok: false, error: err.message };
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  return { ok: false, error: 'Máximo de reintentos alcanzado' };
}

sendBtn.addEventListener('click', async () => {
  if (!currentEncrypted) {
    setStatus('❌ Primero debes cifrar el mensaje (botón "Cifrar mensaje").', true);
    return;
  }

  setStatus('📡 Enviando mensaje cifrado...');
  sendBtn.disabled = true;
  copyBtn.disabled = true;

  const workerUrl = 'https://mimail.jimraynor.workers.dev';
  const result = await sendWithRetry(workerUrl, { text: currentEncrypted }, 1);

  if (result.ok) {
    setStatus('✅ Mensaje enviado correctamente. Recibiré tu mensaje cifrado.');
    // Limpiar campos
    messageEl.value = '';
    contactEl.value = '';
    senderKeyEl.value = '';
    encryptedResultEl.value = '';
    currentEncrypted = '';
    copyBtn.disabled = true;
    sendBtn.disabled = true;
    const oldDiv = document.getElementById('manualInstructions');
    if (oldDiv) oldDiv.remove();
  } else {
    let errorMsg = `❌ Error al enviar: ${result.error || 'desconocido'}.`;
    setStatus(errorMsg, true);
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

// Reset manual instructions
function resetManualInstructions() {
  const oldDiv = document.getElementById('manualInstructions');
  if (oldDiv) oldDiv.remove();
}
messageEl.addEventListener('input', resetManualInstructions);
contactEl.addEventListener('input', resetManualInstructions);
senderKeyEl.addEventListener('input', resetManualInstructions);

// ==================== GENERADOR DE CLAVES INTEGRADO ====================
const genName = document.getElementById('genName');
const genContact = document.getElementById('genContact');
const genKeyBtn = document.getElementById('genKeyBtn');
const genResultDiv = document.getElementById('genResult');
const genPublicKey = document.getElementById('genPublicKey');
const genPrivateKey = document.getElementById('genPrivateKey');
const copyPubToFormBtn = document.getElementById('copyPubToFormBtn');
const downloadPubBtn = document.getElementById('downloadPubBtn');
const downloadPrivBtn = document.getElementById('downloadPrivBtn');

let lastGeneratedPublicKey = '';
let lastGeneratedPrivateKey = '';

genKeyBtn.addEventListener('click', async () => {
  const name = genName.value.trim() || 'Anónimo';
  const contact = genContact.value.trim();
  // Crear userID: puede ser solo nombre o nombre + email
  let userID = name;
  if (contact) userID += ` <${contact}>`;
  
  genKeyBtn.disabled = true;
  genKeyBtn.textContent = 'Generando... (puede tardar unos segundos)';
  genResultDiv.style.display = 'none';
  try {
    const { privateKey, publicKey } = await openpgp.generateKey({
      type: 'ecc',
      curve: 'ed25519',
      userIDs: [{ name: userID }],
      format: 'armored'
    });
    lastGeneratedPublicKey = publicKey;
    lastGeneratedPrivateKey = privateKey;
    genPublicKey.value = publicKey;
    genPrivateKey.value = privateKey;
    genResultDiv.style.display = 'block';
  } catch (err) {
    alert('Error al generar las claves: ' + err.message);
  } finally {
    genKeyBtn.disabled = false;
    genKeyBtn.textContent = 'Generar par de claves';
  }
});

copyPubToFormBtn.addEventListener('click', () => {
  if (!lastGeneratedPublicKey) {
    alert('Primero genera las claves.');
    return;
  }
  senderKeyEl.value = lastGeneratedPublicKey;
  setStatus('✅ Clave pública añadida al formulario. Ahora puedes cifrar el mensaje.');
  // Opcional: desplazar hacia arriba
  senderKeyEl.scrollIntoView({ behavior: 'smooth' });
});

function downloadKey(key, filename) {
  if (!key) return;
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

downloadPubBtn.addEventListener('click', () => {
  if (!lastGeneratedPublicKey) {
    alert('Primero genera las claves.');
    return;
  }
  const name = genName.value.trim().replace(/\s+/g, '_') || 'anonymous';
  downloadKey(lastGeneratedPublicKey, `${name}_public.asc`);
});

downloadPrivBtn.addEventListener('click', () => {
  if (!lastGeneratedPrivateKey) {
    alert('Primero genera las claves.');
    return;
  }
  const name = genName.value.trim().replace(/\s+/g, '_') || 'anonymous';
  downloadKey(lastGeneratedPrivateKey, `${name}_private.asc`);
});
</script>

<style>
/* Estilos del formulario principal */
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

/* Estilos del generador inline */
.keygen-inline {
  margin-top: 2rem;
  padding: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 8px;
  background-color: var(--md-default-bg-color);
}
.keygen-inline .form-group {
  margin-bottom: 1rem;
}
.warning {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #fff3cd;
  color: #856404;
  border-radius: 4px;
}
</style>
