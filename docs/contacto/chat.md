---
title: Chat Cifrado
---

<div id="conversejs" style="height: 500px; width: 100%;"></div>

<link rel="stylesheet" type="text/css" href="https://cdn.conversejs.org/11.0.0/css/converse.min.css">
<script src="https://cdn.conversejs.org/11.0.0/dist/converse.min.js"></script>

<script>
  converse.initialize({
    view_mode: 'embedded', // Cambiado de 'fullscreen' a 'embedded'
    // ... el resto de tu configuración (bosh_service_url, i18n, etc.)
  });
</script>
<style>
  /* Ajusta la altura del contenedor principal del chat */
  #conversejs {
    height: 400px; /* Ajusta esta altura a tu gusto */
    width: 100%;
    margin: 0 auto; /* Centra el chat si el contenedor es más pequeño */
  }

  /* Elimina la imagen de fondo o los logos de patrocinadores */
  .conversejs .chat-head {
    background-image: none !important;
  }
  .conversejs .sponsor {
    display: none !important;
  }

  /* Reduce el tamaño de la cabecera y otros elementos */
  .conversejs .chat-head .chat-head-chatbox-title {
    font-size: 0.9rem;
  }
  .conversejs .chat-head .chat-head__buttons {
    transform: scale(0.9);
  }
</style>
