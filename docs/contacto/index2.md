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
  <button type="button" id="generateKeyBtn" style="margin-top: 0.5rem;">🔑 No tengo clave, generar una</button>
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

<!-- Modal para generar clave -->
<dialog id="keygenModal" style="border: none; border-radius: 8px; padding: 1rem; max-width: 90%; width: 500px;">
  <div class="modal-content">
    <h3>Generar tu clave PGP</h3>
    <div class="form-group">
      <label for="modalName">Nombre / Alias:</label>
      <input type="text" id="modalName" placeholder="Tu nombre o nick" value="Anónimo">
    </div>
    <div class="form-group">
      <label for="modalEmail">Correo electrónico (opcional):</label>
      <input type="email" id="modalEmail" placeholder="ejemplo@dominio.com">
    </div>
    <button id="modalGenerateBtn">Generar par de claves</button>
    <div id="modalResult" style="display: none; margin-top: 1rem;">
      <div class="form-group">
        <label>Clave pública generada:</label>
        <textarea id="modalPublicKey" rows="6" readonly style="font-family: monospace;"></textarea>
        <button id="modalCopyPubBtn">Copiar clave pública</button>
      </div>
      <div class="form-group">
        <label>Clave privada (descárgala):</label>
        <textarea id="modalPrivateKey" rows="6" readonly style="font-family: monospace;"></textarea>
        <button id="modalDownloadPrivBtn">Descargar clave privada (.asc)</button>
      </div>
      <p class="warning">⚠️ Guarda tu clave privada en un lugar seguro. No la pierdas.</p>
    </div>
    <button id="closeModalBtn" style="margin-top: 1rem;">Cerrar</button>
  </div>
</dialog>

<script src="https://jim88.pp.ua/js/openpgp.min.js"></script>
<script>
// Tu clave pública (oculta)
const myPublicKeyArmored = `-----BEGIN PGP PUBLIC KEY BLOCK-----

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

// Elementos DOM
const messageEl = document.getElementById('message');
const contactEl = document.getElementById('contact');
const senderKeyEl = document.getElementById('senderPubKey');
const encryptedResultEl = document.getElementById('encryptedResult');
const statusEl = document.getElementById('status');
const encryptBtn = document.getElementById('encryptBtn');
const copyBtn = document.getElementById('copyBtn');
const sendBtn = document.getElementById('sendBtn');
const generateKeyBtn = document.getElementById('generateKeyBtn');
const keygenModal = document.getElementById('keygenModal');
const modalGenerateBtn = document.getElementById('modalGenerateBtn');
const modalResult = document.getElementById('modalResult');
const modalPublicKey = document.getElementById('modalPublicKey');
const modalPrivateKey = document.getElementById('modalPrivateKey');
const modalCopyPubBtn = document.getElementById('modalCopyPubBtn');
const modalDownloadPrivBtn = document.getElementById('modalDownloadPrivBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const modalName = document.getElementById('modalName');
const modalEmail = document.getElementById('modalEmail');

let currentEncrypted = ''; // almacena el último mensaje cifrado

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

// Función para cifrar el mensaje con timeout
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

// Cifrar al hacer clic
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
    setStatus('❌ Debes proporcionar tu clave pública (o generarla con el botón).', true);
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
    setStatus(`❌ Error al cifrar: ${err.message}. Recarga la página y vuelve a intentarlo.`, true);
    encryptBtn.disabled = false;
  } finally {
    encryptBtn.disabled = false;
  }
});

// Copiar al portapapeles
copyBtn.addEventListener('click', async () => {
  if (!currentEncrypted) {
    setStatus('❌ No hay mensaje cifrado para copiar.', true);
    return;
  }
  try {
    await navigator.clipboard.writeText(currentEncrypted);
    setStatus('📋 Mensaje cifrado copiado al portapapeles.');
  } catch (err) {
    setStatus('❌ No se pudo copiar automáticamente. Selecciona el texto y copia manualmente.', true);
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
    if (result.status === 403 || result.status === 401) {
      errorMsg += ' Posible problema de CORS o autenticación.';
    } else if (result.status === 500) {
      errorMsg += ' Error interno del servidor.';
    }
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
      Copia el texto cifrado de arriba (ya está en el campo "Mensaje cifrado") y envíalo por correo a <strong>pgp@jim88.pp.ua</strong>.<br>
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

// --- Modal de generación de claves ---
generateKeyBtn.addEventListener('click', () => {
  keygenModal.showModal();
});

closeModalBtn.addEventListener('click', () => {
  keygenModal.close();
});

modalGenerateBtn.addEventListener('click', async () => {
  const name = modalName.value.trim() || 'Anónimo';
  const email = modalEmail.value.trim();
  modalGenerateBtn.disabled = true;
  modalGenerateBtn.textContent = 'Generando... (puede tardar unos segundos)';
  modalResult.style.display = 'none';
  try {
    const { privateKey, publicKey } = await openpgp.generateKey({
      type: 'ecc',
      curve: 'ed25519',
      userIDs: [{ name: name, email: email }],
      format: 'armored'
    });
    modalPublicKey.value = publicKey;
    modalPrivateKey.value = privateKey;
    modalResult.style.display = 'block';
    // Guardar temporalmente la clave privada para descarga
    window._tempPrivateKey = privateKey;
  } catch (err) {
    alert('Error al generar las claves: ' + err.message);
  } finally {
    modalGenerateBtn.disabled = false;
    modalGenerateBtn.textContent = 'Generar par de claves';
  }
});

modalCopyPubBtn.addEventListener('click', () => {
  const pub = modalPublicKey.value;
  if (!pub) return;
  navigator.clipboard.writeText(pub).then(() => {
    alert('Clave pública copiada al portapapeles.');
    // Rellenar el campo del formulario principal y cerrar el modal
    senderKeyEl.value = pub;
    keygenModal.close();
    setStatus('✅ Clave pública añadida. Ahora puedes cifrar el mensaje.');
  }).catch(() => {
    alert('No se pudo copiar automáticamente. Selecciona y copia manualmente.');
  });
});

modalDownloadPrivBtn.addEventListener('click', () => {
  const priv = modalPrivateKey.value;
  if (!priv) return;
  const blob = new Blob([priv], { type: 'application/pgp-keys' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'private.asc';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});
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
dialog {
  border: none;
  border-radius: 8px;
  padding: 1rem;
  max-width: 90%;
  width: 500px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
}
.modal-content textarea, .modal-content input {
  width: 100%;
  box-sizing: border-box;
  margin: 0.5rem 0;
  padding: 0.5rem;
  font-family: monospace;
}
.warning {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #fff3cd;
  color: #856404;
  border-radius: 4px;
}
</style>
