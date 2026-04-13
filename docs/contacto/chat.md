---
title: Chat Cifrado
description: Comunícate conmigo de forma segura.
---

# Chat Cifrado

<div id="conversejs" style="height: 600px; width: 100%;"></div>

<link rel="stylesheet" type="text/css" href="https://cdn.conversejs.org/11.0.0/css/converse.min.css">
<script src="https://cdn.conversejs.org/11.0.0/dist/converse.min.js"></script>

<script>
  converse.initialize({
    view_mode: 'fullscreen',
    bosh_service_url: 'https://xmpp.jp:5281/http-bind/', 
    i18n: 'es',
    auto_login: false,
    allow_logout: false,
    allow_contact_deletion: false,
    allow_contact_requests: false,
    allow_registration: false,
    hide_open_bookmarks: false,
    show_controlbox_by_default: true,
    message_archiving: 'always',
    enable_emojis: true,
    enable_smileys: true,
    enable_omemo: true,
    omemo_auto_trust_own_devices: true,
  });
</script>
