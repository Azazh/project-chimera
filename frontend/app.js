const servers = [
  { name: 'MoltBook', env: 'MOLTBOOK_API_KEY', url: 'https://api.moltbook.example/mcp' },
  { name: 'Coinbase AgentKit', env: 'COINBASE_API_KEY', url: 'https://api.coinbase.com/agentkit/mcp' },
  { name: 'OpenAI', env: 'OPENAI_API_KEY', url: 'https://api.openai.com/v1/mcp' },
  { name: 'Weaviate', env: 'WEAVIATE_ENDPOINT', url: 'http://weaviate:8080/mcp' },
  { name: 'Twitter', env: 'TWITTER_BEARER_TOKEN', url: 'https://api.twitter.example/mcp' },
];

const container = document.getElementById('mcp-servers');
servers.forEach(s => {
  const el = document.createElement('div');
  el.className = 'card';
  el.innerHTML = `<strong>${s.name}</strong><br/><small>${s.url}</small><br/>Env: <code>${s.env}</code>`;
  container.appendChild(el);
});
