DEPOSITS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Deposits Queue</title>
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
    .filter-bar { display: flex; gap: 0.5rem; }
    .filter-btn { background: #18181b; border: 1px solid #27272a; color: #a1a1aa; padding: 0.45rem 0.9rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
    .filter-btn:hover { background: #27272a; color: #fafafa; }
    .filter-btn.active { background: #27272a; color: #10b981; border-color: #10b981; }
    .search-input { background: #18181b; border: 1px solid #27272a; padding: 0.5rem 0.85rem; border-radius: 6px; color: #fff; font-size: 0.85rem; outline: none; width: 320px; }
    .search-input:focus { border-color: #10b981; }

    .card-box { background: #121214; border: 1px solid #27272a; border-radius: 8px; overflow: hidden; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: #09090b; color: #71717a; font-weight: 600; padding: 0.75rem 1.25rem; border-bottom: 1px solid #27272a; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.05em; }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:hover td { background: #18181b; }
    
    .account-id-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 600; color: #f59e0b; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); padding: 2px 7px; border-radius: 4px; display: inline-flex; align-items: center; gap: 4px; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; }
    .badge-pending { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-approved { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-rejected { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    .btn-action { padding: 5px 12px; border-radius: 5px; font-size: 0.75rem; font-weight: 600; cursor: pointer; border: none; transition: all 0.15s; }
    .btn-approve { background: #10b981; color: #09090b; }
    .btn-approve:hover { background: #059669; }
    .btn-reject { background: #ef4444; color: #fafafa; margin-left: 6px; }
    .btn-reject:hover { background: #dc2626; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header"><div class="logo-box">G</div><div class="logo-text">GoldenEra 5G</div></div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link">👥 Users & Accounts</a></li>
      <li class="nav-item"><a href="/admin/transactions" class="nav-link">📜 Transactions History</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link active">💳 Deposits</a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.4.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Deposit History & Approvals</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="toolbar">
        <div class="filter-bar">
          <button class="filter-btn active" onclick="setFilter('all', this)">All Deposits</button>
          <button class="filter-btn" onclick="setFilter('pending', this)">Pending Review ⏳</button>
          <button class="filter-btn" onclick="setFilter('approved', this)">Approved ✅</button>
          <button class="filter-btn" onclick="setFilter('rejected', this)">Rejected ❌</button>
        </div>
        <input type="text" id="search-box" class="search-input" placeholder="🔍 Search ID, Account ID, phone, or tx..." oninput="filterDeposits()">
      </div>

      <div class="card-box">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Account ID</th>
              <th>User</th>
              <th>Method</th>
              <th>Sender Phone / TxID</th>
              <th>Amount USD</th>
              <th>Local (EGP)</th>
              <th>Status</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="deposits-body">
            <tr><td colspan="10" style="text-align: center; color: #71717a; padding: 2rem;">Loading deposits ledger...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    let currentFilter = 'all';
    let rawDeposits = [];

    async function loadDeposits() {
      try {
        const url = currentFilter === 'all' ? '/admin/api/deposits' : `/admin/api/deposits?status=${currentFilter}`;
        const res = await fetch(url);
        const data = await res.json();
        rawDeposits = data.deposits || (Array.isArray(data) ? data : []);
        renderDeposits(rawDeposits);
      } catch(e) {
        console.error(e);
      }
    }

    function renderDeposits(deposits) {
      const tbody = document.getElementById('deposits-body');
      if (!deposits || deposits.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; color: #71717a; padding: 2rem;">No deposits found matching criteria.</td></tr>';
        return;
      }
      tbody.innerHTML = deposits.map(d => {
        const isTxHash = d.txid && d.txid.length > 20;
        const txDisplay = isTxHash 
          ? `<a href="https://tronscan.org/#/transaction/${d.txid}" target="_blank" style="color: #38bdf8; text-decoration: underline; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;">${d.txid.slice(0, 10)}...${d.txid.slice(-6)} ↗</a>`
          : `<code style="font-family: 'JetBrains Mono', monospace; color: #a1a1aa; font-size: 0.8rem;">${d.sender_phone || d.txid || '—'}</code>`;

        return `
          <tr>
            <td style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">#${d.id}</td>
            <td><span class="account-id-badge">🆔 ${d.user_account_id || d.user_telegram_id}</span></td>
            <td><strong>${d.user_name || d.user_telegram_id}</strong></td>
            <td><span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 700; color: #38bdf8;">${d.method}</span></td>
            <td>${txDisplay}</td>
            <td style="font-weight: 700; color: #10b981; font-family: monospace;">$${(d.amount_usd || 0).toFixed(2)}</td>
            <td style="color: #71717a; font-family: monospace;">${d.amount_local ? d.amount_local.toFixed(2) + ' EGP' : '—'}</td>
            <td><span class="badge badge-${d.status}">${d.status}</span></td>
            <td style="color: #71717a; font-size: 0.8rem;">${d.created_at ? new Date(d.created_at).toLocaleString() : '—'}</td>
            <td style="white-space: nowrap;">
              ${d.status === 'pending' ? `
                <button class="btn-action btn-approve" onclick="review(${d.id}, 'approve')">Approve</button>
                <button class="btn-action btn-reject" onclick="review(${d.id}, 'reject')">Reject</button>
              ` : '<span style="color: #52525b; font-size: 0.75rem;">Archived</span>'}
            </td>
          </tr>
        `;
      }).join('');
    }

    function setFilter(f, btn) {
      currentFilter = f;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadDeposits();
    }

    function filterDeposits() {
      const q = document.getElementById('search-box').value.toLowerCase().trim();
      const filtered = rawDeposits.filter(d => 
        String(d.id).includes(q) ||
        (d.user_account_id && d.user_account_id.toLowerCase().includes(q)) ||
        (d.user_name && d.user_name.toLowerCase().includes(q)) ||
        (d.sender_phone && d.sender_phone.toLowerCase().includes(q)) ||
        (d.txid && d.txid.toLowerCase().includes(q))
      );
      renderDeposits(filtered);
    }

    async function review(id, action) {
      if (!confirm(`Are you sure you want to ${action} deposit #${id}?`)) return;
      try {
        const res = await fetch(`/admin/api/deposits/${id}/${action}`, { method: 'POST' });
        if (res.ok) {
          loadDeposits();
        } else {
          alert('Action failed');
        }
      } catch(e) {
        alert(e);
      }
    }

    loadDeposits();
  </script>
</body>
</html>"""
