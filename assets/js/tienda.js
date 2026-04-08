// docs/assets/js/tienda.js

document.addEventListener('DOMContentLoaded', () => {
    // Añadir un timestamp a la URL del JSON para evitar la caché del navegador
    const productsUrl = `/products.json?t=${new Date().getTime()}`;

    fetch(productsUrl)
        .then(response => response.json())
        .then(products => {
            const container = document.getElementById('tienda-container');
            if (!container) return;
            container.innerHTML = '';
            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'producto-tarjeta';
                card.innerHTML = `
                    ${product.image ? `<img src="${product.image}" alt="${product.title}" class="producto-imagen">` : ''}
                    <div class="producto-info">
                        <h3 class="producto-titulo">${product.title}</h3>
                        <div class="producto-descripcion">${product.description}</div>
                        <p class="producto-precio">${product.price} ${product.currency}</p>
                        <a href="${product.kofi_link}" class="producto-boton" target="_blank" rel="noopener noreferrer">Comprar</a>
                    </div>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => console.error('Error cargando productos:', error));
});
