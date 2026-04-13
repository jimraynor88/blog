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
