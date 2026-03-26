---
title: Contacto cifrado
description: Envíame un mensaje seguro con PGP
---

# Contacto cifrado con PGP

Si quieres comunicarte conmigo de forma segura, utiliza este formulario. Tu mensaje se cifrará con mi clave pública y podrás incluir tu propia clave para que yo pueda responderte de forma cifrada. Si no tienes clave, puedes [generar una aquí](generar-clave/).

---

## 📝 Enviar mensaje cifrado

<div class="pgp-contact">

<div class="form-group">
  <label for="message">Tu mensaje (texto plano):</label>
  <textarea id="message" rows="6" placeholder="Escribe aquí tu mensaje..."></textarea>
</div>

<div class="form-group">
  <label for="recipientPubKey">Mi clave pública (no la modifiques):</label>
  <textarea id="recipientPubKey" rows="8" readonly style="background-color:#f5f5f5; font-family: monospace;">-----BEGIN PGP PUBLIC KEY BLOCK-----

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
-----END PGP PUBLIC KEY BLOCK-----</textarea>
  <small>No modifiques este campo.</small>
</div>

<div class="form-group">
  <label for="senderPubKey">Tu clave pública (opcional):</label>
  <textarea id="senderPubKey" rows="4" placeholder="Pega aquí tu clave pública si quieres que te la incluya..."></textarea>
  <small>Si la incluyes, podré responderte de forma cifrada. Si no tienes, puedes <a href="generar-clave/">generar una aquí</a>.</small>
</div>

<div class="form-group">
  <label for="encryptedResult">Mensaje cifrado (resultado):</label>
  <textarea id="encryptedResult" rows="8" readonly></textarea>
</div>

<button id="encryptBtn">Cifrar mensaje</button>

<div class="form-group" style="margin-top: 1rem;">
  <button id="sendViaCloudflareBtn">Enviar mensaje cifrado</button>
  <small>El mensaje se enviará a mi correo de forma segura.</small>
</div>

</div>

<script src="https://cdn.jsdelivr.net/npm/openpgp@5.11.0/dist/openpgp.min.js"></script>
<script>
// Tu clave pública (la misma que está en el textarea)
const myPublicKeyArmored = document.getElementById('recipientPubKey').value.trim();

// Función para cifrar el mensaje (con opción de incluir clave del remitente)
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

// Cifrar al hacer clic
document.getElementById('encryptBtn').addEventListener('click', async () => {
  const plaintext = document.getElementById('message').value;
  if (!plaintext.trim()) {
    alert('Escribe un mensaje primero.');
    return;
  }
  const senderKey = document.getElementById('senderPubKey').value;
  try {
    const encrypted = await encryptMessage(myPublicKeyArmored, plaintext, senderKey);
    document.getElementById('encryptedResult').value = encrypted;
  } catch (err) {
    console.error(err);
    alert('Error al cifrar: ' + err.message);
  }
});

// Enviar al Worker de Cloudflare (Mailchannels)
document.getElementById('sendViaCloudflareBtn').addEventListener('click', async () => {
  const encryptedMsg = document.getElementById('encryptedResult').value;
  if (!encryptedMsg.trim()) {
    alert('Primero cifra el mensaje.');
    return;
  }

  const workerUrl = 'https://mimail.jimraynor.workers.dev';
  try {
    const response = await fetch(workerUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: encryptedMsg })
    });
    if (response.ok) {
      alert('Mensaje enviado correctamente. Recibiré tu mensaje cifrado por correo.');
      // Opcional: limpiar el formulario
      document.getElementById('message').value = '';
      document.getElementById('senderPubKey').value = '';
      document.getElementById('encryptedResult').value = '';
    } else {
      alert('Error al enviar. Inténtalo de nuevo más tarde.');
    }
  } catch (err) {
    console.error(err);
    alert('Error de red: ' + err.message);
  }
});
</script>

<style>
.pgp-contact textarea {
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
