
const paginationButtons = document.querySelectorAll('.pagination button:not(.arrow-left):not(.arrow-right)');
const arrowLeft = document.querySelector('.arrow-left');
const arrowRight = document.querySelector('.arrow-right');

let currentPage = 1;

function updatePaginationUI() {
    paginationButtons.forEach(btn => {
        btn.classList.remove('current');
        if (parseInt(btn.textContent) === currentPage) {
            btn.classList.add('current');
        }
    });
}

paginationButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        currentPage = parseInt(btn.textContent);
        updatePaginationUI();
    });
});

arrowLeft.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        updatePaginationUI();
    }
});

arrowRight.addEventListener('click', () => {
    if (currentPage < paginationButtons.length) {
        currentPage++;
        updatePaginationUI();
    }
});

updatePaginationUI();

