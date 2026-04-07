---
title: Tienda
description: Servicios de asesoría y cartas natales
---

# Mis servicios

Aquí puedes ver los productos que ofrezco.

<script defer src="https://cdn.ko-fi.tools/v2/js/shop.js"></script>
<div id="kofi-shop-embed" data-shop-id="Y8Y227YY4" data-shop-currency="€" data-shop-theme="none" data-shop-soldout="show"></div>

<script>
window.addEventListener('load', function() {
    setTimeout(function() {
        // Traducir botones
        document.querySelectorAll('.kofi-shop-item button, .kofi-shop-item a.btn-buy').forEach(btn => {
            if (btn.innerText === 'Buy Now') btn.innerText = 'Comprar ahora';
            else if (btn.innerText === 'View product') btn.innerText = 'Ver producto';
        });
        const allBtn = document.querySelector('.kofi-shop-view-all, .kofi-shop-view-all-button');
        if (allBtn && allBtn.innerText === 'All') allBtn.innerText = 'Ver todos';
        // Ocultar créditos
        const credit = document.querySelector('.kofi-tools-credit, .kofi-shop-credit');
        if (credit) credit.style.display = 'none';
    }, 1000);
});
</script>

<style>
/* Opcional: estilos adicionales para que la tienda se vea bien */
.kofi-shop-item {
    border: 1px solid #ddd;
    padding: 1rem;
    margin: 1rem;
    border-radius: 8px;
    background: var(--md-default-bg-color);
}
.kofi-shop-item button {
    background-color: var(--md-primary-fg-color);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
}
.kofi-shop-item button:hover {
    background-color: var(--md-accent-fg-color);
}
</style>
