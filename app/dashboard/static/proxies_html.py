PROXIES_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Active Proxies</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #09090b; color: #fafafa; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; display: flex; min-height: 100vh; }
    a { color: inherit; text-decoration: none; }
    .sidebar { width: 240px; background: #0f0f11; border-right: 1px solid #27272a; display: flex; flex-direction: column; flex-shrink: 0; }
    .sidebar-header { padding: 1.5rem 1.25rem; border-bottom: 1px solid #1f1f23; display: flex; align-items: center; gap: 0.75rem; }
    .logo-box { width: 32px; height: 32px; background: #18181b; border: 1px solid #3f3f46; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #10b981; }
    .logo-text { font-weight: 600; font-size: 0.95rem; }
    .nav-list { list-style: none; padding: 1rem 0.75rem; flex: 1; }
    .nav-item { margin-bottom: 0.25rem; }
    .nav-link { display: flex; align-items: center; gap: 0.75rem; padding: 0.65rem 0.75rem; border-radius: 6px; font-size: 0.875rem; font-weight: 500; color: #a1a1aa; transition: all 0.15s; }
    .nav-link:hover { background: #18181b; color: #fafafa; }
    .nav-link.active { background: #18181b; color: #10b981; border: 1px solid #27272a; font-weight: 600; }
    .sidebar-footer { padding: 1rem 1.25rem; border-top: 1px solid #1f1f23; font-size: 0.8rem; color: #71717a; display: flex; justify-content: space-between; }
    .logout-btn { color: #ef4444; font-weight: 500; }
    .main-wrap { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
    .top-bar { height: 64px; border-bottom: 1px solid #27272a; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; background: #0f0f11; }
    .top-title { font-size: 1.1rem; font-weight: 600; }
    .admin-pill { background: #18181b; border: 1px solid #27272a; padding: 0.35rem 0.75rem; border-radius: 20px; font-size: 0.8rem; color: #a1a1aa; }
    .admin-pill span { color: #10b981; font-weight: 600; }
    .content-area { padding: 2rem; flex: 1; }
    
    .toolbar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem; }
    .search-input { background: #18181b; border: 1px solid #27272a; padding: 0.5rem 0.85rem; border-radius: 6px; color: #fff; font-size: 0.85rem; outline: none; width: 340px; }
    .search-input:focus { border-color: #10b981; }

    .card-box { background: #121214; border: 1px solid #27272a; border-radius: 8px; overflow: hidden; }
    .card-header { padding: 1rem 1.25rem; border-bottom: 1px solid #27272a; display: flex; justify-content: space-between; align-items: center; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: #09090b; color: #71717a; font-weight: 600; padding: 0.75rem 1.25rem; border-bottom: 1px solid #27272a; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.05em; }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:hover td { background: #18181b; }

    .account-id-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 600; color: #f59e0b; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); padding: 2px 7px; border-radius: 4px; display: inline-flex; align-items: center; gap: 4px; }
    .badge-active { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; }
    .badge-inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; }
    .code-box { font-family: 'JetBrains Mono', monospace; background: #18181b; border: 1px solid #27272a; padding: 3px 7px; border-radius: 4px; font-size: 0.78rem; color: #e4e4e7; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; }
    .code-box:hover { border-color: #10b981; color: #10b981; }
    .btn-refresh { background: #18181b; border: 1px solid #27272a; color: #fafafa; padding: 0.45rem 0.9rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
    .btn-refresh:hover { background: #27272a; border-color: #3f3f46; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header"><div class="logo-box">G</div><div class="logo-text">GoldenEra 5G</div></div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link">👥 Users & Accounts</a></li>
      <li class="nav-item"><a href="/admin/transactions" class="nav-link">📜 Transactions History</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link">💳 Deposits</a></li>
      <li class="nav-item"><a href="/admin/redeem" class="nav-link">🎁 Redeem Codes</a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link active">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.4.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Active Proxies Monitor</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="toolbar">
        <div>
          <div style="font-weight: 600; font-size: 1rem;">Live Proxy Fleet</div>
          <div style="color: #71717a; font-size: 0.78rem;">Monitor real-time allocated 5G/4G/Residential proxies and expiration windows.</div>
        </div>
        <div style="display: flex; gap: 0.75rem;">
          <input type="text" id="search-box" class="search-input" placeholder="🔍 Search by Account ID, IP, user, or product..." oninput="filterProxies()">
          <button onclick="loadProxies()" class="btn-refresh">Refresh 🔄</button>
        </div>
      </div>

      <div class="card-box">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Owner Account ID</th>
              <th>User</th>
              <th>Category</th>
              <th>Protocol / Mode</th>
              <th>Location</th>
              <th>Host : Port</th>
              <th>Auth Credentials</th>
              <th>Expires At</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="proxies-body">
            <tr><td colspan="10" style="text-align: center; color: #71717a; padding: 2rem;">Loading proxies...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    let rawProxies = [];

    async function loadProxies() {
      try {
        const res = await fetch('/admin/api/proxies');
        const data = await res.json();
        rawProxies = data.proxies || (Array.isArray(data) ? data : []);
        renderProxies(rawProxies);
      } catch(e) {
        console.error(e);
      }
    }

    function renderProxies(proxies) {
      const tbody = document.getElementById('proxies-body');
      if (!proxies || proxies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; color: #71717a; padding: 2rem;">No active proxies currently allocated.</td></tr>';
        return;
      }
      tbody.innerHTML = proxies.map(p => {
        const flag = p.flag || '🌐';
        const loc = p.location || p.country_name || p.country || 'Global';
        const hostPort = (p.host && p.port) ? `${p.host}:${p.port}` : '—';
        const auth = (p.auth_username && p.auth_password) ? `${p.auth_username}:${p.auth_password}` : 'IP Whitelist';

        return `
          <tr>
            <td style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">#${p.id}</td>
            <td><span class="account-id-badge">🆔 ${p.user_account_id || p.user_telegram_id}</span></td>
            <td><strong>${p.user_name || p.user_telegram_id}</strong></td>
            <td><span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 700; color: #38bdf8;">${p.category}</span></td>
            <td><code style="font-size: 0.75rem; color: #a1a1aa;">${(p.protocol || 'SOCKS5').toUpperCase()} • ${p.mode || 'rotate'}</code></td>
            <td><span>${flag} ${loc}</span></td>
            <td>
              ${hostPort !== '—' 
                ? `<span class="code-box" onclick="copyText('${hostPort}')" title="Click to copy">${hostPort} 📋</span>` 
                : '<span style="color:#71717a">—</span>'}
            </td>
            <td>
              ${auth !== 'IP Whitelist'
                ? `<span class="code-box" onclick="copyText('${auth}')" title="Click to copy">${auth} 📋</span>`
                : '<span style="color:#71717a; font-size: 0.78rem;">IP Whitelist</span>'}
            </td>
            <td style="color: #71717a; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace;">
              ${p.expiry_date ? new Date(p.expiry_date).toLocaleString() : 'Never'}
            </td>
            <td>
              <span class="${p.is_active ? 'badge-active' : 'badge-inactive'}">
                ${p.is_active ? 'Active' : 'Expired'}
              </span>
            </td>
          </tr>
        `;
      }).join('');
    }

    function filterProxies() {
      const q = document.getElementById('search-box').value.toLowerCase().trim();
      const filtered = rawProxies.filter(p =>
        String(p.id).includes(q) ||
        (p.user_account_id && p.user_account_id.toLowerCase().includes(q)) ||
        (p.user_name && p.user_name.toLowerCase().includes(q)) ||
        (p.host && p.host.toLowerCase().includes(q)) ||
        (p.category && p.category.toLowerCase().includes(q)) ||
        (p.product_code && p.product_code.toLowerCase().includes(q))
      );
      renderProxies(filtered);
    }

    function copyText(str) {
      navigator.clipboard.writeText(str).then(() => {
        alert('Copied to clipboard: ' + str);
      });
    }

    loadProxies();
  </script>
</body>
</html>"""
