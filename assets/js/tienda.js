// docs/assets/js/tienda.js

document.addEventListener('DOMContentLoaded', () => {
    const productsUrl = '/products.json';

    fetch(productsUrl)
        .then(response => response.json())
        .then(products => {
            mostrarProductos(products);
        })
        .catch(error => console.error('Error cargando los productos:', error));

    function mostrarProductos(products) {
        const container = document.getElementById('tienda-container');
        if (!container) return;
        container.innerHTML = '';
        products.forEach(product => {
            const card = crearTarjetaProducto(product);
            container.appendChild(card);
        });
    }

    function crearTarjetaProducto(product) {
        const div = document.createElement('div');
        div.className = 'producto-tarjeta';
        div.innerHTML = `
            ${product.image ? `<img src="${product.image}" alt="${product.title}" class="producto-imagen">` : ''}
            <div class="producto-info">
                <h3 class="producto-titulo">${product.title}</h3>
                <div class="producto-descripcion">${product.description}</div>
                <p class="producto-precio">${product.price} ${product.currency}</p>
                <!-- El botón "Comprar" usa el enlace de Ko-fi, que es externo y seguro -->
                <a href="${product.kofi_link}" class="producto-boton" target="_blank" rel="noopener noreferrer">Comprar en Ko-fi</a>
            </div>
        `;
        return div;
    }
});
