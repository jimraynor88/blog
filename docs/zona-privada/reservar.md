---
title: Reservar una sesión personalizada
description: Agenda una hora en exclusiva con Jim Raynor a través de Telegram
---

# Reservar una hora conmigo

<div class="reserva-container">

## ¿Cómo funciona?

1. **Elige fecha y hora** disponibles en el calendario.
2. **Rellena tus datos** (nombre y email). Te enviaremos la confirmación.
3. **Realiza el pago** en Ko‑fi (50€). Una vez confirmado, recibirás un email con el enlace a un grupo privado de Telegram.
4. **Únete a la videollamada** en la hora acordada. Podrás usar cualquier cliente de Telegram, aunque para Android se recomienda **MoMoGram** (con soporte PGP integrado).

</div>

---

## 📅 Horarios disponibles

- **Mañana:** 11:00, 12:00, 13:00
- **Tarde/noche:** 19:00, 20:00, 21:00

*(Las sesiones duran una hora. Elige una franja que no esté ya ocupada.)*

---

## ✏️ Formulario de reserva

<div class="formulario-reserva">

<form id="reserva-form">
  <div class="form-group">
    <label for="nombre">Tu nombre o alias:</label>
    <input type="text" id="nombre" name="nombre" required placeholder="Ej: Jim Raynor">
  </div>

  <div class="form-group">
    <label for="email">Correo electrónico:</label>
    <input type="email" id="email" name="email" required placeholder="tucorreo@ejemplo.com">
    <small>Te enviaremos la confirmación y el enlace al grupo.</small>
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

## 💬 ¿Por qué Telegram?

La sesión se realizará a través de un **grupo privado de Telegram**. Allí podremos hacer videollamada, compartir pantalla, enviar archivos y chatear. Telegram es multiplataforma y gratuito.

### Clientes recomendados

- **MoMoGram** (Android): [Descargar en F-Droid](https://f-droid.org/packages/org.telegram.momogram/) | [GitHub](https://github.com/telegrammomogram/momogram)
  *Ventaja: integra OpenKeychain para cifrar mensajes con PGP.*
- **Telegram oficial**: [Web](https://web.telegram.org), [iOS](https://apps.apple.com/app/telegram-messenger/id686449807), [Android](https://play.google.com/store/apps/details?id=org.telegram.messenger)

> **Nota:** Si no tienes Telegram, regístrate con tu número de móvil (es rápido y no requiere datos personales).

---

## 🔐 Privacidad y seguridad

- Tu email solo se usará para enviarte la confirmación y el enlace.
- El grupo de Telegram es efímero: se crea una nueva sala para cada reserva (o se reutiliza el mismo grupo, pero con acceso controlado por el enlace de invitación). En cualquier caso, tus datos están protegidos.

<style>
.reserva-container, .formulario-reserva {
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
.reservar-btn {
  background-color: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.reservar-btn:hover {
  background-color: var(--md-accent-fg-color);
}
</style>

<script>
  const WORKER_URL = 'https://tu-worker.tu-usuario.workers.dev';  // CAMBIA ESTO

  const fechaInput = document.getElementById('fecha');
  const horaSelect = document.getElementById('hora');
  const disponibilidadMsg = document.getElementById('disponibilidad-msg');

  // Validar disponibilidad cuando cambia fecha u hora
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

    // Primero comprobar disponibilidad otra vez (por si acaso)
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
</script>
