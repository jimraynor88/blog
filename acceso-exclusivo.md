---
title: Acceso Exclusivo
description: Contenido especial para mecenas
---

# Acceso Exclusivo

Si has recibido una contraseña por correo, introdúcela aquí para acceder al contenido especial.

<div id="acceso-form">
  <input type="password" id="password" placeholder="Contraseña" style="width: 100%; padding: 0.5rem; margin-bottom: 1rem;">
  <button id="btn-verificar">Verificar y acceder</button>
</div>

<div id="contenido" style="display: none;"></div>
<div id="error-msg" style="color: red; margin-top: 1rem;"></div>

<script>
const workerUrl = 'https://kofi-manager.jimraynor.workers.dev/webhook'; // CAMBIA ESTO

document.getElementById('btn-verificar').addEventListener('click', async () => {
  const password = document.getElementById('password').value.trim();
  const errorDiv = document.getElementById('error-msg');
  const contentDiv = document.getElementById('contenido');
  if (!password) {
    errorDiv.innerText = 'Introduce una contraseña.';
    return;
  }
  errorDiv.innerText = '';
  contentDiv.style.display = 'none';
  document.getElementById('btn-verificar').disabled = true;
  document.getElementById('btn-verificar').innerText = 'Verificando...';

  try {
    const response = await fetch(workerUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password })
    });
    const data = await response.json();
    if (data.valid) {
      contentDiv.innerHTML = data.content;
      contentDiv.style.display = 'block';
      document.getElementById('acceso-form').style.display = 'none';
    } else {
      errorDiv.innerText = 'Contraseña incorrecta o caducada.';
    }
  } catch (err) {
    errorDiv.innerText = 'Error de conexión. Inténtalo más tarde.';
  } finally {
    document.getElementById('btn-verificar').disabled = false;
    document.getElementById('btn-verificar').innerText = 'Verificar y acceder';
  }
});
</script>

<style>
#contenido {
  margin-top: 2rem;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: var(--md-default-bg-color);
}
</style>
