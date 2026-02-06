async function loadServers() {
  const container = document.getElementById('mcp-servers');
  try {
    const res = await fetch('/servers');
    const data = await res.json();
    const servers = data.servers || {};
    Object.keys(servers).forEach(name => {
      const s = servers[name];
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `<strong>${name}</strong><br/><small>${s.url}</small><br/>Type: <code>${s.type}</code>`;
      container.appendChild(el);
    });
  } catch (e) {
    container.innerHTML = '<em>Failed to load MCP servers</em>';
  }
}

async function loadAcceptance() {
  const section = document.createElement('section');
  section.innerHTML = '<h2>Acceptance Criteria</h2>';
  try {
    const res = await fetch('/acceptance');
    const data = await res.json();
    const pre = document.createElement('pre');
    pre.textContent = JSON.stringify(data, null, 2);
    section.appendChild(pre);
  } catch (e) {
    section.innerHTML += '<p class="hint">Failed to load acceptance criteria.</p>';
  }
  document.querySelector('main').appendChild(section);
}

loadServers();
loadAcceptance();
