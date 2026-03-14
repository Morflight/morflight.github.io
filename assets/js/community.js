/* ============================================================
   Community Reference — filter and render
   ============================================================ */

function platformIcon(p) {
  return p === 'discord' ? 'Discord' : 'TeamSpeak';
}

function buildServerCard(s) {
  const tagPills = s.tags.map(t => `<span class="tag-pill">${t}</span>`).join('');
  const iconEl = s.icon
    ? `<img class="community-card__icon" src="${s.icon}" alt="${s.name} icon" loading="lazy">`
    : `<div class="community-card__icon community-card__icon--placeholder">${s.name.charAt(0)}</div>`;

  return `
    <article class="community-card" data-tags="${s.tags.join(',')}">
      <div class="community-card__header">
        ${iconEl}
        <div class="community-card__identity">
          <div class="community-card__top">
            <span class="community-card__name">${s.name}</span>
            <span class="badge badge--platform badge--${s.platform}">${platformIcon(s.platform)}</span>
          </div>
        </div>
      </div>
      <p class="community-card__desc">${s.desc}</p>
      <div class="community-card__tags">${tagPills}</div>
      <div class="community-card__footer">
        <a href="${s.invite}" class="btn-join" target="_blank" rel="noopener" data-i18n="community.join">Join →</a>
      </div>
    </article>
  `;
}

let activeTag = 'all';

function applyFilters() {
  const visible = SERVERS.filter(s =>
    activeTag === 'all' || s.tags.includes(activeTag)
  );

  const grid  = document.getElementById('community-grid');
  const empty = document.getElementById('empty-state');
  const count = document.getElementById('filter-count');

  grid.innerHTML = visible.map(buildServerCard).join('');
  if (window.i18n) window.i18n.applyTranslations();
  empty.hidden   = visible.length > 0;
  count.textContent = visible.length === SERVERS.length
    ? `${SERVERS.length} servers`
    : `${visible.length} of ${SERVERS.length} servers`;
}

applyFilters();

document.querySelectorAll('.tag-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tag-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeTag = btn.dataset.tag;
    applyFilters();
  });
});
