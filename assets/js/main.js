/* Mobile nav toggle */
const toggle = document.querySelector('.nav__toggle');
const links  = document.querySelector('.nav__links');

if (toggle && links) {
  toggle.addEventListener('click', () => {
    toggle.classList.toggle('open');
    links.classList.toggle('open');
  });
}

/* Mark active nav link */
const currentPage = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav__links a').forEach(a => {
  const href = a.getAttribute('href');
  if (href === currentPage || (currentPage === '' && href === 'index.html')) {
    a.classList.add('active');
  }
});
