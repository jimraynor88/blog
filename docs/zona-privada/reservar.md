---
title: Reservar una sesión
---

# Reserva una hora conmigo

<div id="app">
  <form id="reserva-form">
    <label>Tu nombre:</label>
    <input type="text" id="nombre" required>

    <label>Tu email:</label>
    <input type="email" id="email" required>

    <label>Fecha:</label>
    <input type="date" id="fecha" required>

    <label>Hora:</label>
    <select id="hora" required>
      <option value="11:00">11:00</option>
      <option value="12:00">12:00</option>
      <option value="13:00">13:00</option>
      <option value="19:00">19:00</option>
      <option value="20:00">20:00</option>
      <option value="21:00">21:00</option>
    </select>

    <button type="submit">Reservar (pago en Ko‑fi)</button>
  </form>
  <div id="mensaje"></div>
</div>

<script>
  const workerUrl = 'https://ko-fi-unified-worker.jimraynor.workers.dev';

  document.getElementById('reserva-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;

    // Primero consultar disponibilidad
    const dispRes = await fetch(`${workerUrl}/disponible-franja?fecha=${fecha}&hora=${hora}`);
    const disp = await dispRes.json();
    if (!disp.disponible) {
      document.getElementById('mensaje').innerHTML = '<p style="color:red">❌ Esta franja ya no está libre.</p>';
      return;
    }

    // Crear reserva temporal
    const tempRes = await fetch(`${workerUrl}/reservar-temporal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, email, fecha, hora })
    });
    if (!tempRes.ok) {
      const err = await tempRes.json();
      document.getElementById('mensaje').innerHTML = `<p style="color:red">❌ ${err.error || 'Error al reservar'}</p>`;
      return;
    }

    // Redirigir a Ko‑fi para pagar (producto de cita)
    window.location.href = 'https://ko-fi.com/s/2f998ea3b5';
  });
</script>
