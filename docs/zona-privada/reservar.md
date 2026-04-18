---
title: Reservar una sesión personalizada
description: Agenda una hora en exclusiva con Jim Raynor a través de Telegram
---

# Reservar una hora conmigo



## ¿Cómo funciona?

1. **Elige fecha y hora** disponibles en el calendario.<br>
2. **Rellena tus datos** (nombre y email). Te enviaremos la confirmación.<br>
3. **Realiza el pago** en Ko‑fi (28,10€). Una vez confirmado, recibirás un email con la referencia de la compra (ej. `S-XXXXXXXXXX`).<br>
4. **Vuelve a esta página e introduce la referencia** para obtener el enlace al grupo privado de Telegram.<br>
5. **Únete a la videollamada** en la hora acordada.<br>

<div class="reserva-container"></div>

---

## 📅 Horarios disponibles

- **Mañana:** 11:00, 12:00, 13:00
- **Tarde/noche:** 19:00, 20:00, 21:00

*(Las sesiones duran una hora. Elige una franja que no esté ya ocupada.)*

---

## ✏️ Formulario de reserva (para elegir día y hora)

<div class="formulario-reserva">

<form id="reserva-form">
  <div class="form-group">
    <label for="nombre">Tu nombre o alias:</label>
    <input type="text" id="nombre" name="nombre" required placeholder="Ej: Jim Raynor">
  </div>

  <div class="form-group">
    <label for="email">Correo electrónico:</label>
    <input type="email" id="email" name="email" required placeholder="tucorreo@ejemplo.com">
    <small>Usaremos este email para asociar tu reserva.</small>
  </div>

  <div class="form-group">
    <label for="fecha">Fecha:</label>
    <input type="date" id="fecha" name="fecha" required>
  </div>

  <div class="form-group">
    <label for="hora">Hora:</label>
    <select id="hora" name="hora" required>
      <option value="">-- Selecciona una hora --</option>
      <option value="11:00">11:00</option>
      <option value="12:00">12:00</option>
      <option value="13:00">13:00</option>
      <option value="19:00">19:00</option>
      <option value="20:00">20:00</option>
      <option value="21:00">21:00</option>
    </select>
  </div>

  <div id="disponibilidad-msg" class="info-mensaje"></div>

  <button type="submit" class="reservar-btn">Reservar y pagar en Ko‑fi</button>
</form>

</div>

---

## 🔐 Validar tu compra (obtener enlace a Telegram)

Si ya has pagado y recibiste la referencia de Ko‑fi, introdúcela aquí junto con tu email para acceder al grupo.

<div class="validacion-container">

<div class="form-group">
  <label for="ref-email">Tu email (el mismo que usaste en la reserva):</label>
  <input type="email" id="ref-email" placeholder="tucorreo@ejemplo.com">
</div>

<div class="form-group">
  <label for="ref-code">Referencia de Ko‑fi:</label>
  <input type="text" id="ref-code" placeholder="Ej: S-Y8Y81XWQP3">
  <small>Es el código que recibiste por email, empieza por <code>S-</code>.</small>
</div>

<button id="validar-ref-btn" class="validar-btn">Validar y obtener enlace</button>

<div id="resultado-validacion" style="margin-top: 1rem;"></div>

</div>

---

## 💬 ¿Por qué Telegram?

La sesión se realizará a través de un **grupo privado de Telegram**. Allí podremos hacer videollamada, compartir pantalla, enviar archivos y chatear. Telegram es multiplataforma y gratuito.

### Clientes recomendados

- **MoMoGram** (Android): [GitHub](https://github.com/dic1911/Momogram) | [Canal de Telegram](https://t.me/s/momogram_update)
  *Ventaja: integra OpenKeychain para cifrar mensajes con PGP.*
- **Telegram oficial**: [Web](https://web.telegram.org), [iOS](https://apps.apple.com/app/telegram-messenger/id686449807), [Android](https://play.google.com/store/apps/details?id=org.telegram.messenger)

---

## 🔐 Privacidad y seguridad

- Tu email solo se usará para asociar la reserva y enviarte el enlace.
- El grupo de Telegram es privado y el enlace de invitación es fijo (puedes regenerarlo si lo deseas).

<style>
.reserva-container, .formulario-reserva, .validacion-container {
  background: var(--md-default-bg-color);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.form-group {
  margin-bottom: 1.2rem;
}
.form-group label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.3rem;
}
.form-group input, .form-group select {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 4px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
}
.form-group small {
  display: block;
  margin-top: 0.2rem;
  color: var(--md-default-fg-color--light);
}
.info-mensaje {
  margin-top: 1rem;
  padding: 0.5rem;
  border-radius: 4px;
}
.info-mensaje.success {
  background: #d4edda;
  color: #155724;
}
.info-mensaje.error {
  background: #f8d7da;
  color: #721c24;
}
.reservar-btn, .validar-btn {
  background-color: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.reservar-btn:hover, .validar-btn:hover {
  background-color: var(--md-accent-fg-color);
}
.validacion-container {
  border-top: 2px solid var(--md-primary-fg-color);
}
</style>

<script>
  const WORKER_URL = 'https://ko-fi-unified-worker.jimraynor.workers.dev';  // Ajusta si es diferente

  // --- Lógica del formulario de reserva (ya existente) ---
  const fechaInput = document.getElementById('fecha');
  const horaSelect = document.getElementById('hora');
  const disponibilidadMsg = document.getElementById('disponibilidad-msg');

  async function checkDisponibilidad() {
    const fecha = fechaInput.value;
    const hora = horaSelect.value;
    if (!fecha || !hora) return;
    try {
      const res = await fetch(`${WORKER_URL}/disponible-franja?fecha=${fecha}&hora=${hora}`);
      const data = await res.json();
      if (data.disponible) {
        disponibilidadMsg.innerHTML = '<span class="success">✅ Horario disponible. Puedes reservar.</span>';
        disponibilidadMsg.className = 'info-mensaje success';
      } else {
        disponibilidadMsg.innerHTML = '<span class="error">❌ Horario no disponible. Elige otro.</span>';
        disponibilidadMsg.className = 'info-mensaje error';
      }
    } catch (err) {
      disponibilidadMsg.innerHTML = '<span class="error">Error al verificar disponibilidad.</span>';
      disponibilidadMsg.className = 'info-mensaje error';
    }
  }

  fechaInput.addEventListener('change', checkDisponibilidad);
  horaSelect.addEventListener('change', checkDisponibilidad);

  document.getElementById('reserva-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const fecha = fechaInput.value;
    const hora = horaSelect.value;

    // Verificar disponibilidad otra vez
    const dispRes = await fetch(`${WORKER_URL}/disponible-franja?fecha=${fecha}&hora=${hora}`);
    const disp = await dispRes.json();
    if (!disp.disponible) {
      disponibilidadMsg.innerHTML = '<span class="error">❌ Horario no disponible. Elige otro.</span>';
      disponibilidadMsg.className = 'info-mensaje error';
      return;
    }

    // Crear reserva temporal
    const tempRes = await fetch(`${WORKER_URL}/reservar-temporal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, email, fecha, hora })
    });
    if (!tempRes.ok) {
      const errorData = await tempRes.json();
      disponibilidadMsg.innerHTML = `<span class="error">❌ ${errorData.error || 'Error al reservar temporalmente'}</span>`;
      disponibilidadMsg.className = 'info-mensaje error';
      return;
    }

    // Redirigir a Ko‑fi para pagar
    window.location.href = 'https://ko-fi.com/s/2f998ea3b5';
  });

  // --- Lógica de validación de referencia ---
  document.getElementById('validar-ref-btn').addEventListener('click', async () => {
    const email = document.getElementById('ref-email').value.trim();
    const ref = document.getElementById('ref-code').value.trim();
    const resultadoDiv = document.getElementById('resultado-validacion');

    if (!email || !ref) {
      resultadoDiv.innerHTML = '<p style="color: red;">❌ Debes introducir tu email y la referencia.</p>';
      return;
    }

    resultadoDiv.innerHTML = '<p>🔍 Verificando...</p>';
    try {
      const res = await fetch(`${WORKER_URL}/verificar-referencia`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, referencia: ref })
      });
      const data = await res.json();
      if (data.success && data.enlace) {
        resultadoDiv.innerHTML = `
          <p style="color: green;">✅ Cita confirmada. Haz clic en el enlace para unirte al grupo de Telegram:</p>
          <p><a href="${data.enlace}" target="_blank" rel="noopener noreferrer">${data.enlace}</a></p>
          <small>El enlace es válido para la sesión reservada. Preséntate con tu nombre y la hora acordada.</small>
        `;
      } else {
        resultadoDiv.innerHTML = `<p style="color: red;">❌ ${data.error || 'No se pudo validar la referencia. Comprueba que el email y la referencia son correctos.'}</p>`;
      }
    } catch (err) {
      resultadoDiv.innerHTML = '<p style="color: red;">❌ Error de conexión. Inténtalo de nuevo más tarde.</p>';
    }
  });
</script>
