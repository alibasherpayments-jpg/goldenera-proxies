TRANSACTIONS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Transactions History</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #09090b; color: #fafafa; font-family: 'Inter', sans-serif; display: flex; min-height: 100vh; }
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
    .card-box { background: #121214; border: 1px solid #27272a; border-radius: 8px; overflow: hidden; }
    .card-header { padding: 1rem 1.25rem; border-bottom: 1px solid #27272a; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
    .search-input { background: #18181b; border: 1px solid #27272a; padding: 0.5rem 0.85rem; border-radius: 6px; color: #fff; font-size: 0.85rem; outline: none; width: 320px; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: #09090b; color: #71717a; font-weight: 600; padding: 0.75rem 1.25rem; border-bottom: 1px solid #27272a; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:hover td { background: #18181b; }
    .account-id-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #f59e0b; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); padding: 2px 7px; border-radius: 4px; }
    .tx-pos { color: #10b981; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .tx-neg { color: #ef4444; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .status-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header"><div class="logo-box">G</div><div class="logo-text">GoldenEra 5G</div></div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link">👥 Users & Accounts</a></li>
      <li class="nav-item"><a href="/admin/transactions" class="nav-link active">📜 Transactions History</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link">💳 Deposits</a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.4.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Global Transactions Ledger</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="card-box">
        <div class="card-header">
          <div>
            <div style="font-weight: 600; font-size: 1rem;">All Transactions (Deposits, Purchases & Points)</div>
            <div style="color: #71717a; font-size: 0.78rem;">Live audit trail of all wallet deposits, proxy orders, and points deductions.</div>
          </div>
          <input type="text" id="search-box" class="search-input" placeholder="🔍 Search transaction by ID, user, or ref..." oninput="filterTx()">
        </div>
        <table>
          <thead>
            <tr>
              <th>Tx Ref</th>
              <th>Account ID</th>
              <th>User</th>
              <th>Type</th>
              <th>Method / Item</th>
              <th>Amount (USD)</th>
              <th>Points</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody id="tx-body">
            <tr><td colspan="9" style="text-align: center; color: #71717a; padding: 2rem;">Loading transactions ledger...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    let allTx = [];

    async function loadTransactions() {
      try {
        const res = await fetch('/admin/api/transactions');
        const data = await res.json();
        allTx = data.transactions || [];
        renderTx(allTx);
      } catch(e) {
        console.error(e);
      }
    }

    function renderTx(txs) {
      const tbody = document.getElementById('tx-body');
      if (!txs || txs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: #71717a; padding: 2rem;">No transactions found.</td></tr>';
        return;
      }
      tbody.innerHTML = txs.map(t => {
        const isPos = t.amount >= 0;
        const amtColor = isPos ? 'tx-pos' : 'tx-neg';
        const sign = isPos ? '+' : '';
        const ptsSign = t.points >= 0 ? '+' : '';
        const isApprove = t.status === 'approved' || t.status === 'succeeded';
        const isPending = t.status === 'pending' || t.status === 'queued';
        const badgeColor = isApprove ? '#10b981' : (isPending ? '#f59e0b' : '#ef4444');
        const badgeBg = isApprove ? 'rgba(16,185,129,0.12)' : (isPending ? 'rgba(245,158,11,0.12)' : 'rgba(239,68,68,0.12)');

        return `
          <tr>
            <td><code style="font-size: 0.75rem; color: #a1a1aa;">${t.id}</code></td>
            <td><span class="account-id-badge">🆔 ${t.account_id}</span></td>
            <td><strong>${t.username.startsWith('@') ? t.username : '@' + t.username}</strong></td>
            <td><span style="font-weight: 600; text-transform: uppercase; font-size: 0.72rem; color: ${isPos ? '#10b981' : '#60a5fa'};">${t.type}</span></td>
            <td>${t.method.toUpperCase()}</td>
            <td class="${amtColor}">${sign}$${Math.abs(t.amount).toFixed(2)}</td>
            <td style="font-family: monospace; font-weight: 700;">${ptsSign}${t.points} pts</td>
            <td><span class="status-badge" style="color: ${badgeColor}; background: ${badgeBg}; border: 1px solid ${badgeColor}40;">${t.status}</span></td>
            <td style="color: #71717a; font-size: 0.78rem;">${t.date ? new Date(t.date).toLocaleString() : '—'}</td>
          </tr>
        `;
      }).join('');
    }

    function filterTx() {
      const q = document.getElementById('search-box').value.toLowerCase().trim();
      const filtered = allTx.filter(t => 
        (t.account_id && t.account_id.toLowerCase().includes(q)) ||
        (t.id && t.id.toLowerCase().includes(q)) ||
        (t.username && t.username.toLowerCase().includes(q)) ||
        (t.reference && t.reference.toLowerCase().includes(q)) ||
        (t.type && t.type.toLowerCase().includes(q))
      );
      renderTx(filtered);
    }

    loadTransactions();
  </script>
</body>
</html>"""
