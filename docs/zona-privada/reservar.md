---
title: Reservar una sesión
---

# Reservar una hora conmigo

<div id="disponibilidad">Cargando...</div>

<a href="https://ko-fi.com/s/TU_CODIGO_CITA" class="kofi-button">Reservar por 50€</a>

<script>
  fetch('https://tu-worker.tu-usuario.workers.dev/disponible')
    .then(r => r.json())
    .then(data => {
      const div = document.getElementById('disponibilidad');
      if (data.disponible) {
        div.innerHTML = '<p style="color: green;">✅ Hay disponibilidad para hoy. ¡Puedes reservar!</p>';
      } else {
        div.innerHTML = '<p style="color: red;">❌ Hoy ya hay una cita reservada. Prueba mañana.</p>';
      }
    })
    .catch(() => {
      document.getElementById('disponibilidad').innerHTML = '<p>Error al consultar disponibilidad.</p>';
    });
</script>
