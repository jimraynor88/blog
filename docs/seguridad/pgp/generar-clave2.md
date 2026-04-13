---
title: Generar tu clave PGP
description: Crea un par de claves PGP de curva elíptica directamente en tu navegador
---

# Generar tu clave PGP

Puedes generar un par de claves de curva elíptica (Ed25519 / Curve25519) de forma segura en tu propio navegador. **La clave privada nunca sale de tu ordenador**; solo se descarga como archivo. Guárdala en un lugar seguro.

---

## 🔑 Generar mi par de claves

<div class="pgp-keygen">

<div class="form-group">
  <label for="keyName">Nombre / Alias:</label>
  <input type="text" id="keyName" placeholder="Tu nombre o nick" value="-">
</div>

<div class="form-group">
  <label for="keyEmail">Email o URL de tu Perfil de RRSS:</label>
  <input type="email" id="keyEmail" placeholder="X.com/MiUser">
</div>

<button id="generateBtn">Generar mi par de claves</button>

<div id="resultArea" style="display: none; margin-top: 1.5rem;">
  <div class="form-group">
    <label>Clave pública (cópiala o guárdala):</label>
    <textarea id="publicKey" rows="8" readonly style="font-family: monospace;"></textarea>
    <button id="copyPubBtn" style="margin-top: 0.5rem;">Copiar clave pública</button>
  </div>
  <div class="form-group">
    <label>Clave privada (descárgala, guárdala e impórtala a tu gestor de claves):</label>
    <textarea id="privateKey" rows="8" readonly style="font-family: monospace;"></textarea>
    <button id="downloadPrivBtn" style="margin-top: 0.5rem;">Descargar clave privada (.asc)</button>
  </div>
  <p class="warning">⚠️ La clave privada es única. Si la pierdes, no podrás recuperar los mensajes cifrados para ti.</p>
</div>

</div>

<script src="https://cdn.jsdelivr.net/npm/openpgp@5.11.0/dist/openpgp.min.js"></script>
<script>
document.getElementById('generateBtn').addEventListener('click', async () => {
  const name = document.getElementById('keyName').value || 'Usuario';
  const email = document.getElementById('keyEmail').value || '';
  const btn = document.getElementById('generateBtn');
  const resultDiv = document.getElementById('resultArea');
  
  btn.disabled = true;
  btn.textContent = 'Generando... (puede tardar unos segundos)';
  resultDiv.style.display = 'none';
  
  try {
    const { privateKey, publicKey } = await openpgp.generateKey({
      type: 'ecc',
      curve: 'ed25519',
      userIDs: [{ name: name, email: email }],
      format: 'armored'
    });
    
    document.getElementById('publicKey').value = publicKey;
    document.getElementById('privateKey').value = privateKey;
    resultDiv.style.display = 'block';
  } catch (err) {
    alert('Error al generar las claves: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generar mi par de claves';
  }
});

document.getElementById('copyPubBtn').addEventListener('click', () => {
  const pub = document.getElementById('publicKey').value;
  navigator.clipboard.writeText(pub).then(() => {
    alert('Clave pública copiada al portapapeles.');
  }).catch(() => {
    alert('No se pudo copiar automáticamente. Selecciona y copia manualmente.');
  });
});

document.getElementById('downloadPrivBtn').addEventListener('click', () => {
  const priv = document.getElementById('privateKey').value;
  const name = document.getElementById('keyName').value || 'anonymous';
  // Reemplazar espacios y caracteres no deseados por guiones bajos
  const safeName = name.trim().replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_\-]/g, '');
  const filename = `${safeName}_private.asc`;
  
  const blob = new Blob([priv], { type: 'application/pgp-keys' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});
</script>

<style>
.pgp-keygen .form-group {
  margin-bottom: 1rem;
}
.pgp-keygen textarea {
  width: 100%;
  box-sizing: border-box;
  font-family: monospace;
  padding: 0.5rem;
}
button {
  background-color: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-right: 0.5rem;
}
button:hover {
  background-color: var(--md-accent-fg-color);
}
.warning {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #fff3cd;
  color: #856404;
  border-radius: 4px;
}
</style>
