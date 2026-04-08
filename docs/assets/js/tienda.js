// docs/assets/js/tienda.js

document.addEventListener('DOMContentLoaded', () => {
    // La URL de products.json después de la compilación de mkdocs
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

        // Usamos innerHTML para construir la tarjeta de forma más clara
        div.innerHTML = `
            ${product.image ? `<img src="${product.image}" alt="${product.title}" class="producto-imagen">` : ''}
            <div class="producto-info">
                <h3 class="producto-titulo">${product.title}</h3>
                <div class="producto-descripcion">${product.description}</div>
                <p class="producto-precio">${product.price} ${product.currency}</p>
                <a href="${product.link}" class="producto-boton" target="_blank">Comprar</a>
            </div>
        `;
        return div;
    }
});
