const search = document.querySelector('#chapter-search');
if (search) search.addEventListener('input', () => {
  const q = search.value.trim().toLocaleLowerCase();
  let count = 0;
  document.querySelectorAll('.chapter-card').forEach(card => {
    card.hidden = !card.dataset.search.toLocaleLowerCase().includes(q);
    if (!card.hidden) count++;
  });
  document.querySelectorAll('.part').forEach(part => {
    part.hidden = !part.querySelector('.chapter-card:not([hidden])');
  });
  document.querySelector('#search-status').textContent = q ? `找到 ${count} 章` : '';
});
