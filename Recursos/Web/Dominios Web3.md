Los dominios Web3 de Unstoppable Domains pueden redirigir a páginas web, pero existen varios métodos distintos y no todos funcionan igual que en el DNS tradicional.

1. Redirección a un sitio Web2 (HTTP/HTTPS)

Se puede hacer una redirección a una web normal usando el campo redirect_url o configurando el dominio en su panel.

Funcionamiento:

El dominio Web3 se resuelve a través del gateway de Unstoppable.

El gateway hace una redirección HTTP a la URL indicada.


Ejemplo conceptual:

midominio.crypto → https://miweb.com

Limitaciones:

Funciona solo cuando el dominio se abre mediante el gateway (por ejemplo https://midominio.crypto usando el resolver compatible).

No es una redirección DNS estándar como en dominios ICANN.


2. Apuntar a contenido descentralizado (IPFS)

También pueden apuntar a contenido en IPFS, que es el uso más habitual.

Ejemplo:

ipfs.html.value = Qm....

Entonces el dominio resuelve a:

https://gateway.ipfs.io/ipfs/Qm...

3. Usar un gateway compatible

Para que funcione en navegadores normales se suele usar un gateway como:

https://midominio.crypto (si el navegador soporta UD)

https://midominio.crypto.unstoppable.io


Ejemplo real:

midominio.crypto.unstoppable.io → redirige o muestra la web

4. Redirección mediante hosting descentralizado

Otra opción común:

1. Subir una página simple a IPFS.


2. Esa página hace un meta refresh o redirección JavaScript a la web final.



Esto funciona siempre porque el navegador solo carga una página HTML.

Resumen

Función	¿Se puede?	Cómo

Redirigir a web normal	Sí	redirect_url o página HTML
Apuntar a IPFS	Sí	registro ipfs.html.value
Redirección DNS clásica	No	no usan DNS ICANN


Nota técnica importante

Los dominios de Unstoppable no están en el DNS global. Funcionan mediante:

resolvers Web3

extensiones de navegador

gateways HTTP


Por eso algunas redirecciones dependen del gateway utilizado.