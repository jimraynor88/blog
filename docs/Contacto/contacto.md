document.getElementById('sendViaCloudflareBtn').addEventListener('click', async () => {
  const encryptedMsg = document.getElementById('encryptedResult').value;
  if (!encryptedMsg.trim()) {
    alert('Primero cifra el mensaje.');
    return;
  }
  const workerUrl = 'https://mimail.jimraynor.workers.dev';  // ← reemplaza con la URL real
  const response = await fetch(workerUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: encryptedMsg })
  });
  if (response.ok) {
    alert('Mensaje enviado correctamente. Recibiré tu mensaje cifrado por correo.');
  } else {
    alert('Error al enviar. Inténtalo de nuevo más tarde.');
  }
});
