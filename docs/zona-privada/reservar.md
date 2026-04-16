---
title: Reservar una sesión
---

# Reserva una hora conmigo

<form id="reserva-form">
  <label>Nombre: <input type="text" id="nombre" required></label><br>
  <label>Email: <input type="email" id="email" required></label><br>
  <label>Fecha: <input type="date" id="fecha" required></label><br>
  <label>Hora:
    <select id="hora" required>
      <option value="11:00">11:00</option>
      <option value="12:00">12:00</option>
      <option value="13:00">13:00</option>
      <option value="19:00">19:00</option>
      <option value="20:00">20:00</option>
      <option value="21:00">21:00</option>
    </select>
  </label><br>
  <button type="submit">Reservar (pago en Ko‑fi)</button>
</form>
<div id="mensaje"></div>

<script>
  const WORKER_URL = 'https://tu-worker.tu-usuario.workers.dev';

  document.getElementById('reserva-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;

    // Consultar disponibilidad
    const disp = await fetch(`${WORKER_URL}/disponible-franja?fecha=${fecha}&hora=${hora}`);
    const dispData = await disp.json();
    if (!dispData.disponible) {
      document.getElementById('mensaje').innerHTML = '<p style="color:red">❌ Horario no disponible.</p>';
      return;
    }

    // Crear reserva temporal
    const res = await fetch(`${WORKER_URL}/reservar-temporal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, email, fecha, hora })
    });
    if (!res.ok) {
      const err = await res.json();
      document.getElementById('mensaje').innerHTML = `<p style="color:red">❌ ${err.error || 'Error'}</p>`;
      return;
    }

    // Redirigir a Ko‑fi para pagar
    window.location.href = 'https://ko-fi.com/s/2f998ea3b5';
  });
</script>
