
const thumbnails = document.querySelectorAll('.thumbnails img');
const mainImage = document.getElementById('mainImage');

thumbnails.forEach(thumbnail => {
    thumbnail.addEventListener('click', () => {
        mainImage.src = thumbnail.src;
    });
});

const carousel = document.getElementById('carousel');

function update3D() {
    const cards = Array.from(carousel.children);
    const centerIndex = Math.floor(cards.length / 2);

    cards.forEach((card, index) => {
        const offset = index - centerIndex;
        const abs = Math.abs(offset);

        let scale = 1;
        let rotateY = 0;
        let translateY = 0;
        let zIndex = 1;

        if (offset === 0) {
            scale = 0.99;
            translateY = 50; // deeper
            zIndex = 10;
        } else if (abs === 1) {
            scale = 1.2;
            rotateY = offset > 0 ? -30 : 30;
            translateY = -5;
            zIndex = 9;
        } else if (abs === 2) {
            scale = 1.25;
            rotateY = offset > 0 ? -50 : 50;
            translateY = -15;
            zIndex = 8;
        } else {
            scale = 0.6;
            translateY = -40;
            zIndex = 7;
        }

        card.style.transform = `scale(${scale}) rotateY(${rotateY}deg) translateY(${translateY}px)`;
        card.style.zIndex = zIndex;
    });
}

function scrollRight() {
    const first = carousel.firstElementChild;
    carousel.appendChild(first);
    update3D();
}

function scrollLeft() {
    const last = carousel.lastElementChild;
    carousel.insertBefore(last, carousel.firstElementChild);
    update3D();
}

update3D();