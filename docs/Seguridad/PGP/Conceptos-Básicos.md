
## 🔐 Conceptos básicos (para todos)

1. **¿Qué es OpenPGP?**
   Es un estándar de cifrado que permite proteger tus mensajes y archivos con un sistema de claves pública y privada, garantizando confidencialidad y autenticidad.

2. **¿Qué diferencia hay con PGP?**
   PGP fue el software original, privado y de los 90. OpenPGP es el estándar abierto y compatible, que todos pueden implementar.

3. **¿Qué es una clave pública y una privada?**
   La pública se comparte con otros para que te envíen mensajes cifrados. La privada la guardas en secreto para descifrarlos y firmar tus propios mensajes.

4. **¿Qué es un fingerprint?**
   Es una “huella digital” única de tu clave pública. Sirve para verificar que una clave realmente pertenece a la persona que dice ser.

5. **¿Qué diferencia hay entre cifrar y firmar?**
   Cifrar protege la confidencialidad (solo el destinatario puede leerlo). Firmar garantiza autenticidad (demuestra que tú lo escribiste y no fue modificado).

6. **¿Qué pasa si olvido mi contraseña?**
   No podrás descifrar nada. Por eso es vital hacer copias de seguridad y guardar tu contraseña en un lugar seguro.

7. **¿Qué es una clave de revocación?**
   Es un “botón de emergencia” que invalida tu clave si la pierdes o te la roban, evitando que alguien se haga pasar por ti.

8. **¿Qué tamaño de clave debo elegir?**
   Hoy se recomienda al menos 3072 bits en RSA o usar curvas elípticas modernas (ECC) para equilibrar seguridad y rapidez.

9. **¿Qué es la “web of trust”?**
   Es un sistema donde los usuarios validan las claves de otros. Cuantas más personas confíen en tu clave, más difícil es que alguien suplante tu identidad.

10. **¿Qué diferencia hay entre OpenPGP y un certificado digital oficial?**
    Los certificados oficiales dependen de una autoridad central. OpenPGP es descentralizado y tú controlas completamente tus claves.

---

## 📱 Uso cotidiano y personal

11. **Proteger fotos privadas:** cifras fotos antes de enviarlas o subirlas a la nube; nadie podrá verlas sin tu clave privada.
12. **Proteger tu diario personal digital:** guarda tus notas cifradas con OpenPGP para que solo tú las leas.
13. **Cifrar contraseñas en un archivo:** puedes almacenar tus contraseñas en un texto cifrado, controlando tú el acceso.
14. **Compartir claves WiFi seguras:** cifra tu contraseña WiFi y solo quien tenga tu clave privada podrá usarla.
15. **Guardar documentos en la nube de forma privada:** sube archivos a Drive, Dropbox o iCloud cifrados, evitando que la plataforma los lea.
16. **Proteger facturas digitales:** cifra o firma tus facturas para garantizar privacidad y autenticidad.
17. **Cifrar un vídeo personal:** incluso archivos grandes como vídeos pueden cifrarse antes de enviarlos.
18. **Cifrar un archivo de calendario:** protege tus citas y planes privados compartidos.
19. **Firmar tus posts de blog:** demuestra autoría y que no fueron modificados.
20. **Compartir mensajes privados en redes sociales:** cifrando textos o archivos antes de enviarlos.

---

## 👨‍👩‍👧‍👦 Uso familiar

21. **Compartir fotos o vídeos familiares de forma segura.**
22. **Intercambiar historiales médicos entre familiares** con privacidad total.
23. **Enseñar a los hijos a usar cifrado básico** para que aprendan seguridad digital.
24. **Mantener seguros documentos de la casa** como contratos de alquiler o hipotecas.
25. **Compartir recetas médicas digitalizadas** entre familiares o cuidadores.

---

## 💼 Uso en trabajo y empresa

26. **Proteger contratos laborales o de alquiler** mediante firma digital y cifrado.
27. **Firmar facturas electrónicas** para garantizar autenticidad ante clientes.
28. **Enviar presupuestos confidenciales** cifrados para que solo el destinatario los lea.
29. **Usarlo en pymes para intercambiar archivos internos** sin depender de plataformas externas.
30. **Verificar actualizaciones de software** para evitar instalar malware.
31. **Firmar código de programación** y paquetes para garantizar origen y autenticidad.
32. **Firmar paquetes o distribuciones de software** para su seguridad.
33. **Integrarlo en negocios online** (pedidos, facturas, datos de clientes) para proteger información.
34. **Firmar documentos académicos o papers de investigación** antes de publicarlos.
35. **Proteger backups de la empresa** cifrando la información sensible.

---

## 📰 Periodismo, activismo y sociedad

36. **Proteger fuentes periodísticas** mediante envío de archivos cifrados.
37. **Intercambiar documentos políticos o sociales sin riesgo** de espionaje o filtración.
38. **Firmar comunicados colectivos** para verificar autenticidad de la información.
39. **Activistas que viajan a países con censura** pueden comunicarse de forma segura.
40. **Proteger la identidad de denunciantes** o informantes sensibles.

---

## 💬 Comunicación y mensajería

41. **Usar en correos electrónicos** (el clásico uso de PGP).
42. **Cifrar mensajes en Telegram** enviándolos como archivo cifrado.
43. **Usar en WhatsApp** para enviar archivos cifrados dentro de la app.
44. **Cifrar chats completos en apps compatibles** como DeltaChat o Proton Mail.
45. **Enviar mensajes firmados** para evitar suplantaciones de identidad.
46. **Detectar mensajes manipulados** si la firma ya no coincide.

---

## ☁️ Archivos y nube

47. **Diferencia entre permisos en Drive y cifrado real.**
48. **Subir documentos a iCloud o Dropbox cifrados.**
49. **Proteger copias de seguridad** cifrando discos o archivos.
50. **Enviar archivos grandes cifrados** por USB o nube sin perder seguridad.

---

## 🎮 Juegos, ocio y creatividad

51. **Firmar mods o archivos de videojuegos** para evitar manipulación.
52. **Guardar partidas cifradas** y mantenerlas privadas.
53. **Usar en comunidades de gamers privadas** para garantizar identidad.
54. **Firmar tus obras creativas** (música, libros, arte digital).
55. **Proteger guiones o proyectos de cine** antes de publicarlos o compartirlos.

---

## 🌍 Legalidad y contexto

56. **¿Es legal usarlo en todos los países?** Depende, algunos limitan el cifrado fuerte.
57. **Riesgos de viajar con claves en dispositivos** si te las pueden confiscar.
58. **Diferencia con ZIP/PDF con contraseña**: PGP es mucho más seguro.
59. **Seguridad frente a ataques de fuerza bruta**: claves modernas tardarían miles de años en romperse.
60. **Limitaciones legales en países con censura.**

---

## 🧑‍💻 Casos técnicos (pero sin comandos)

61. **¿Qué pasa si alguien envía un archivo corrupto?** La app lo detectará.
62. **¿Se puede usar offline?** Sí, todo cifrado y descifrado funciona sin internet.
63. **¿Qué pasa si cambio de móvil o PC?** Solo importa exportar/importar tus claves.
64. **¿Qué ocurre si dos personas tienen la misma clave pública?** Las claves deben ser únicas; si no, lo detectas con fingerprints.
65. **¿Qué tamaño ocupan los archivos cifrados?** Un poco más que el original, pero manejable.
66. **¿Se puede usar para autenticación en servicios web?** Sí, reemplaza usuario/contraseña firmando retos.
67. **¿Sirve para validar actualizaciones?** Sí, garantiza que provienen del desarrollador original.
68. **¿Qué ocurre si alguien intenta descifrar mis mensajes?** Con claves modernas, no podrá.
69. **Diferencia con cifrado simétrico**: OpenPGP no requiere compartir contraseñas.
70. **Cifrar para varios destinatarios**: puedes añadir varias claves públicas al mismo archivo.

---

## 🚀 Usos avanzados e innovadores

71. **Usar en transacciones de criptomonedas** para firmar mensajes de propiedad.
72. **Proteger identidad digital en foros** con firmas que validen tu seudónimo.
73. **Publicar tu clave pública en internet** es seguro; solo permite cifrar mensajes para ti.
74. **Crear una red privada de amigos/familiares** usando claves PGP para compartir información.
75. **Usarlo en cooperativas o comunidades pequeñas** para intercambiar archivos seguros.
76. **Firmar entradas de calendario compartidas** con otros miembros.
77. **Integrarlo en un blog o web personal** para verificar autoría de posts.
78. **Proteger datos de smart home (IoT)** cifrando actualizaciones o información sensible.
79. **Mantener chats privados fuera de apps comerciales** cifrando archivos.
80. **Verificar identidad en entrevistas online** firmando mensajes de verificación.

---

## 🧩 Comparaciones y preguntas frecuentes

81. **Diferencia entre OpenPGP y Signal/WhatsApp**: OpenPGP te da control absoluto sobre la clave.
82. **Diferencia entre PGP y OpenPGP**: OpenPGP es estándar abierto, PGP fue el software original.
83. **Ventaja sobre contraseñas ZIP o PDF**: más seguro, con firma digital y control de identidad.
84. **¿Vale la pena aprenderlo si no soy técnico?** Sí, protege tu privacidad digital.
85. **¿Por qué usarlo si ya tengo SSL/HTTPS en webs?** SSL protege canales, PGP protege contenido.
86. **¿Qué ventajas da frente a gestores de contraseñas?** Control total y almacenamiento offline posible.
87. **¿Cómo se compara con firmas electrónicas oficiales?** Es independiente, no necesita autoridad central.
88. **¿Qué diferencia hay con blockchain?** Blockchain registra transacciones; PGP cifra y firma mensajes.
89. **¿Por qué no lo usan más personas si es tan seguro?** La complejidad inicial y falta de apps amigables.
90. **¿Qué pasa si Google o Apple fallan, pero cifro con OpenPGP?** Tus datos siguen seguros porque tú controlas la clave.

---

## 🧭 Futuro y reflexión

91. **¿Será útil en la era de la computación cuántica?** Algunas claves modernas son resistentes; habrá que adaptarlas.
92. **¿Es práctico para todo el mundo?** Sí, si las apps móviles lo hacen fácil.
93. **¿Puede combinarse con biometría (huella, cara)?** Sí, como capa adicional de seguridad para abrir la clave privada.
94. **¿Puede servir en la educación digital?** Sí, para enseñar seguridad y privacidad desde jóvenes.
95. **¿Ayuda a la privacidad de los menores?** Sí, protege comunicación y documentos.
96. **¿Tiene sentido en un mundo donde casi todo se guarda en la nube?** Sí, porque evita que terceros vean tus datos.
97. **¿Es una herramienta política además de técnica?** Sí, refuerza la soberanía digital y privacidad frente a terceros.
98. **¿Puede convertirse en un estándar masivo?** Potencialmente, si las apps lo hacen amigable.
99. **¿Cómo cambia la mentalidad al aprenderlo?** Te hace más consciente de la privacidad y el control de tu información.
100. **¿Por qué debería empezar hoy mismo?** Para proteger tus datos antes de que sea demasiado tarde o demasiado caro.
101. **¿Qué futuro tendrá si lo adaptan a apps móviles sencillas?** Podría ser tan natural como usar WhatsApp, pero seguro y privado.

