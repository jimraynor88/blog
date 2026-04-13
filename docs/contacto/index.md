---
title: Contacto cifrado
description: Envíame un mensaje seguro con PGP
---

# Contacto cifrado con PGP

Si quieres comunicarte conmigo de forma segura, utiliza este formulario. Tu mensaje se cifrará con mi clave pública y podrás dejar tu contacto para que pueda responderte. Si no tienes clave PGP, puedes [generar una aquí](generar-clave/) e incluirla en el mensaje para que yo pueda responderte cifrado.

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
  <label for="senderPubKey">Tu clave pública (opcional):</label>
  <textarea id="senderPubKey" rows="4" placeholder="Pega aquí tu clave pública si quieres que te responda cifrado..."></textarea>
  <small>Si la incluyes, podré responderte de forma cifrada. Si no tienes, puedes <a href="generar-clave/">generar una aquí</a>.</small>
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

<script src="https://jim88.pp.ua/js/openpgp.min.js"></script>
<script>
// Tu clave pública (oculta)
const myPublicKeyArmored = `-----BEGIN PGP PUBLIC KEY BLOCK-----

xjMEad1dZBYJKwYBBAHaRw8BAQdAm/+1BydAgefBb1MyVoz4APWag2UiJRfr
JKc8X0trBBjNGEppbVBHUCA8cGdwQGppbTg4LnBwLnVhPsKMBBAWCgA+BYJp
3V1kBAsJBwgJkPENWUIvZM5uAxUICgQWAAIBAhkBApsDAh4BFiEECCPRLlaj
1OtfSoCf8Q1ZQi9kzm4AAPU3AQDhpBZdKVjWPYgcQ0IZSgKGSba0bTHJ7dGT
hK73EX/vjAEAsD6lbUoWYnVcX5DQUeiJswwMEOX0Cr1CxxZPKlhbaQfOOARp
3V1kEgorBgEEAZdVAQUBAQdAIXUE+NXLVgH6MSVQXLuCXukHbeee0p9wBWoK
56uOIn8DAQgHwngEGBYKACoFgmndXWQJkPENWUIvZM5uApsMFiEECCPRLlaj
1OtfSoCf8Q1ZQi9kzm4AAI30AP9ZL6iLD+uiKRyyrzsuiVi9khYu7KvWufgo
gGw34cDmRgEAiXFIopBdM7VeGWh1NYWnCjNU4RXQh7L+8+Y/vLE+Jwg=
=k1K6
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

let currentEncrypted = ''; // almacena el último mensaje cifrado

// Función para mostrar mensajes de estado
function setStatus(text, isError = false) {
  statusEl.innerHTML = `<span style="color: ${isError ? 'red' : 'green'};">${text}</span>`;
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
  if (!plaintext) {
    setStatus('❌ Escribe un mensaje.', true);
    return;
  }
  if (!contact) {
    setStatus('❌ Indica un contacto (email, Telegram, etc.).', true);
    return;
  }

  setStatus('🔐 Cifrando mensaje... (puede tardar unos segundos)');
  encryptBtn.disabled = true;
  copyBtn.disabled = true;
  sendBtn.disabled = true;
  encryptedResultEl.value = '';

  try {
    let fullMessage = `Mensaje de: ${contact}\n\n${plaintext}`;
    if (senderKeyEl.value.trim()) {
      fullMessage += `\n\n--- Clave pública del remitente ---\n${senderKeyEl.value.trim()}`;
    }

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
      // esperar un momento antes de reintentar
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
    // Eliminar mensaje manual si existe
    const oldDiv = document.getElementById('manualInstructions');
    if (oldDiv) oldDiv.remove();
  } else {
    // Mostrar mensaje de error y ofrecer alternativa manual
    let errorMsg = `❌ Error al enviar: ${result.error || 'desconocido'}.`;
    if (result.status === 403 || result.status === 401) {
      errorMsg += ' Posible problema de CORS o autenticación.';
    } else if (result.status === 500) {
      errorMsg += ' Error interno del servidor.';
    }
    setStatus(errorMsg, true);
    
    // Mostrar instrucciones para envío manual
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
    sendBtn.disabled = false; // Permitir reintentar
    copyBtn.disabled = false; // Permitir copiar
  }
});

// Limpiar mensaje manual al volver a escribir o cambiar algo
function resetManualInstructions() {
  const oldDiv = document.getElementById('manualInstructions');
  if (oldDiv) oldDiv.remove();
}
messageEl.addEventListener('input', resetManualInstructions);
contactEl.addEventListener('input', resetManualInstructions);
senderKeyEl.addEventListener('input', resetManualInstructions);
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
</style>
