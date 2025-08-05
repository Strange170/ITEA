const product = document.getElementById('product');
const productImg = document.getElementById('product-img');
const productTitle = document.getElementById('product-title');
const productPrice = document.getElementById('product-price');

document.querySelectorAll('.object').forEach(object => {
    object.addEventListener('mouseenter', function () {
        const rect = object.getBoundingClientRect();

        productImg.src = object.getAttribute('data-img');
        productTitle.textContent = object.getAttribute('data-title');
        productPrice.textContent = object.getAttribute('data-price');

        product.style.top = `${rect.top + window.scrollY - 830}px`; // if product label appear more bottom increase this if appear more higher decrease this
        product.style.left = `${rect.left + window.scrollX - 500}px`;

        product.style.display = 'flex';
        product.style.visibility = 'visible';
        product.style.opacity = '1';
    });

    object.addEventListener('mouseleave', function () {
        product.style.display = 'none';
        product.style.visibility = 'hidden';
        product.style.opacity = '0';
        productImg.src = '';
        productTitle.textContent = '';
        productPrice.textContent = '';
    });

    object.addEventListener('click', function () {
        const link = object.getAttribute('data-link');
        window.location.href = link;
    });
});