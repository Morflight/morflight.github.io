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
const currentPath = location.pathname.replace(/\/$/, '') || '/';
document.querySelectorAll('.nav__links a').forEach(a => {
  const href = a.getAttribute('href').replace(/\/$/, '') || '/';
  if (href === currentPath) a.classList.add('active');
});
