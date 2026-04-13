---
title: Contacto cifrado
description: Envíame un mensaje seguro con PGP
---

# Contacto cifrado con PGP

Si quieres comunicarte conmigo de forma segura, utiliza este formulario. Tu mensaje se cifrará con mi clave pública y podrás dejar tu contacto para que pueda responderte. Si no tienes clave PGP, puedes [[generar-clave|generar una aquí]] e incluirla en el mensaje para que yo pueda responderte cifrado.

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
  <small>Si la incluyes, podré responderte de forma cifrada. Si no tienes, puedes <a href="../seguridad/pgp/generar-clave/">generar una aquí</a>.</small>
</div>

<div class="form-group">
  <label for="status">Estado:</label>
  <div id="status" style="margin-top: 0.5rem;"></div>
</div>

<button id="sendBtn">Cifrar y enviar mensaje</button>

</div>

<script src="https://cdn.jsdelivr.net/npm/openpgp@5.11.0/dist/openpgp.min.js"></script>
<script>
// Tu clave pública (oculta)
const myPublicKeyArmored = `-----BEGIN PGP PUBLIC KEY BLOCK-----

xjMEaTiwuBYJKwYBBAHaRw8BAQdAULW0hAnmT7uuWp0MLjPApWrPwB2byApD
cP61TkcrjQPNCkppbSBSYXlub3LCjAQQFgoAPgWCaTiwuAQLCQcICZAlsWQ4
ylh93gMVCAoEFgACAQIZAQKbAwIeARYhBEVAQ/IYfZwLbxKeyiWxZDjKWH3e
AAAhHAEA2TNPqXn072RNX5qJ2E1BdkKmGZ2zVHIy8GIitHqH0kMBAP57IEpK
NQlcvw5F7hxHuRmnfkly2MuadVJK6F7iUO8DzjgEaTiwuBIKKwYBBAGXVQEF
AQEHQH92bSqmHqW2yJ1PiZRdXSPOc7ImN0dKB7kPIZyVNH4aAwEIB8J4BBgW
CgAqBYJpOLC4CZAlsWQ4ylh93gKbDBYhBEVAQ/IYfZwLbxKeyiWxZDjKWH3e
AADTIgEAtl3w5Dv5yUviNqFRe6S4siobVbGw4NbiMaEZ+Xzu1vEBANKaL8ED
DiaBt6uhKqPZCWkBHanc5yMXA3BSjuGb8vgD
=4/cH
-----END PGP PUBLIC KEY BLOCK-----`;

// Función para cifrar el mensaje (opcionalmente con clave del remitente)
async function encryptMessage(publicKeyArmored, plaintext, signKeyArmored = null) {
  const publicKey = await openpgp.readKey({ armoredKey: publicKeyArmored });
  const options = {
    message: await openpgp.createMessage({ text: plaintext }),
    encryptionKeys: publicKey,
  };
  if (signKeyArmored && signKeyArmored.trim()) {
    const privateKey = await openpgp.readPrivateKey({ armoredKey: signKeyArmored });
    options.signingKeys = privateKey;
  }
  const encrypted = await openpgp.encrypt(options);
  return encrypted;
}

// Elementos DOM
const messageEl = document.getElementById('message');
const contactEl = document.getElementById('contact');
const senderKeyEl = document.getElementById('senderPubKey');
const statusEl = document.getElementById('status');
const sendBtn = document.getElementById('sendBtn');

sendBtn.addEventListener('click', async () => {
  const plaintext = messageEl.value.trim();
  const contact = contactEl.value.trim();
  if (!plaintext) {
    statusEl.innerHTML = '<span style="color: red;">❌ Escribe un mensaje.</span>';
    return;
  }
  if (!contact) {
    statusEl.innerHTML = '<span style="color: red;">❌ Indica un contacto (email, Telegram, etc.).</span>';
    return;
  }

  statusEl.innerHTML = '<span>🔐 Cifrando mensaje...</span>';
  sendBtn.disabled = true;

  try {
    // Construir el texto que se cifrará: incluir el contacto y la clave pública del remitente si se proporciona
    let fullMessage = `Mensaje de: ${contact}\n\n${plaintext}`;
    if (senderKeyEl.value.trim()) {
      fullMessage += `\n\n--- Clave pública del remitente ---\n${senderKeyEl.value.trim()}`;
    }

    // Cifrar el mensaje con mi clave pública
    const encrypted = await encryptMessage(myPublicKeyArmored, fullMessage);

    // Enviar al Worker
    statusEl.innerHTML = '<span>📡 Enviando mensaje cifrado...</span>';
    const workerUrl = 'https://mimail.jimraynor.workers.dev';
    const response = await fetch(workerUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: encrypted })
    });

    if (response.ok) {
      statusEl.innerHTML = '<span style="color: green;">✅ Mensaje enviado correctamente. Recibiré tu mensaje cifrado.</span>';
      // Limpiar campos
      messageEl.value = '';
      contactEl.value = '';
      senderKeyEl.value = '';
    } else {
      const errorText = await response.text();
      console.error('Worker error:', errorText);
      statusEl.innerHTML = `<span style="color: red;">❌ Error al enviar: ${errorText}</span>`;
    }
  } catch (err) {
    console.error(err);
    statusEl.innerHTML = `<span style="color: red;">❌ Error de red o cifrado: ${err.message}</span>`;
  } finally {
    sendBtn.disabled = false;
  }
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
.form-group {
  margin-bottom: 1rem;
}
small {
  display: block;
  margin-top: -0.25rem;
  color: #666;
}
</style>
