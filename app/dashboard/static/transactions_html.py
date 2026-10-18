TRANSACTIONS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Transactions History</title>
  <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/static/logo.png">
  <link rel="icon" type="image/svg+xml" href="/static/logo.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #09090b; color: #fafafa; font-family: 'Inter', sans-serif; display: flex; min-height: 100vh; }
    a { color: inherit; text-decoration: none; }
    .sidebar { width: 240px; background: #0f0f11; border-right: 1px solid #27272a; display: flex; flex-direction: column; flex-shrink: 0; }
    .sidebar-header { padding: 1.5rem 1.25rem; border-bottom: 1px solid #1f1f23; display: flex; align-items: center; gap: 0.75rem; }
    .logo-img { width: 34px; height: 34px; border-radius: 6px; object-fit: cover; border: 1px solid #3f3f46; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2); }
    .logo-text { font-weight: 700; font-size: 1rem; letter-spacing: -0.01em; background: linear-gradient(135deg, #fafafa, #a1a1aa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
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
    .toolbar-actions { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
    .search-input { background: #18181b; border: 1px solid #27272a; padding: 0.5rem 0.85rem; border-radius: 6px; color: #fff; font-size: 0.85rem; outline: none; width: 300px; }
    .btn-bulk-delete { background: #ef4444; color: #fff; border: none; border-radius: 6px; padding: 0.5rem 1rem; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; gap: 0.35rem; }
    .btn-bulk-delete:hover { background: #dc2626; box-shadow: 0 0 12px rgba(239, 68, 68, 0.4); }
    .btn-action-del { background: transparent; border: 1px solid #3f3f46; color: #ef4444; padding: 5px 9px; border-radius: 5px; font-size: 0.8rem; cursor: pointer; transition: all 0.15s; }
    .btn-action-del:hover { background: rgba(239, 68, 68, 0.15); border-color: #ef4444; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: #09090b; color: #71717a; font-weight: 600; padding: 0.75rem 1.25rem; border-bottom: 1px solid #27272a; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; vertical-align: middle; }
    tr:hover td { background: #18181b; }
    .account-id-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #f59e0b; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); padding: 2px 7px; border-radius: 4px; }
    .tx-pos { color: #10b981; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .tx-neg { color: #ef4444; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .status-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header"><img src="/static/logo.png" alt="Logo" class="logo-img"><div class="logo-text">GoldenEra 5G</div></div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link">👥 Users & Accounts</a></li>
      <li class="nav-item"><a href="/admin/transactions" class="nav-link active">📜 Transactions History</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link">💳 Deposits</a></li>
      <li class="nav-item"><a href="/admin/redeem" class="nav-link">🎁 Redeem Codes</a></li>
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
            <div style="font-weight: 600; font-size: 1rem;">All Transactions (Deposits & Purchases)</div>
            <div style="color: #71717a; font-size: 0.78rem;">Live audit trail of all wallet deposits and proxy purchases.</div>
          </div>
          <div class="toolbar-actions">
            <button id="btn-bulk-delete" class="btn-bulk-delete" onclick="deleteSelected()" style="display: none;">
              🗑️ Delete Selected (<span id="selected-count">0</span>)
            </button>
            <input type="text" id="search-box" class="search-input" placeholder="🔍 Search transaction by ID, user, or ref..." oninput="filterTx()">
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th style="width: 42px; text-align: center;"><input type="checkbox" id="select-all" onclick="toggleSelectAll(this)" style="cursor: pointer; width: 16px; height: 16px; accent-color: #10b981;"></th>
              <th>Tx Ref</th>
              <th>Account ID</th>
              <th>User</th>
              <th>Type</th>
              <th>Method / Item</th>
              <th>Amount (USD)</th>
              <th>Status</th>
              <th>Date</th>
              <th style="text-align: right; width: 80px;">Action</th>
            </tr>
          </thead>
          <tbody id="tx-body">
            <tr><td colspan="10" style="text-align: center; color: #71717a; padding: 2rem;">Loading transactions ledger...</td></tr>
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
        tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; color: #71717a; padding: 2rem;">No transactions found.</td></tr>';
        updateSelectedCount();
        return;
      }
      tbody.innerHTML = txs.map(t => {
        const isPos = t.amount >= 0;
        const amtColor = isPos ? 'tx-pos' : 'tx-neg';
        const sign = isPos ? '+' : '';
        const isApprove = t.status === 'approved' || t.status === 'succeeded';
        const isPending = t.status === 'pending' || t.status === 'queued';
        const badgeColor = isApprove ? '#10b981' : (isPending ? '#f59e0b' : '#ef4444');
        const badgeBg = isApprove ? 'rgba(16,185,129,0.12)' : (isPending ? 'rgba(245,158,11,0.12)' : 'rgba(239,68,68,0.12)');

        return `
          <tr id="row-${t.id}">
            <td style="text-align: center;"><input type="checkbox" class="tx-checkbox" value="${t.id}" onchange="updateSelectedCount()" style="cursor: pointer; width: 16px; height: 16px; accent-color: #10b981;"></td>
            <td><code style="font-size: 0.75rem; color: #a1a1aa;">${t.id}</code></td>
            <td><span class="account-id-badge">🆔 ${t.account_id}</span></td>
            <td><strong>${t.username.startsWith('@') ? t.username : '@' + t.username}</strong></td>
            <td><span style="font-weight: 600; text-transform: uppercase; font-size: 0.72rem; color: ${isPos ? '#10b981' : '#60a5fa'};">${t.type}</span></td>
            <td>${t.method.toUpperCase()}</td>
            <td class="${amtColor}">${sign}$${Math.abs(t.amount).toFixed(2)}</td>
            <td><span class="status-badge" style="color: ${badgeColor}; background: ${badgeBg}; border: 1px solid ${badgeColor}40;">${t.status}</span></td>
            <td style="color: #71717a; font-size: 0.78rem;">${t.date ? new Date(t.date).toLocaleString() : '—'}</td>
            <td style="text-align: right; white-space: nowrap;">
              <button class="btn-action-del" onclick="deleteSingleTx('${t.id}')" title="Delete Transaction">🗑️</button>
            </td>
          </tr>
        `;
      }).join('');
      updateSelectedCount();
    }

    function toggleSelectAll(master) {
      const boxes = document.querySelectorAll('.tx-checkbox');
      boxes.forEach(cb => cb.checked = master.checked);
      updateSelectedCount();
    }

    function updateSelectedCount() {
      const selected = document.querySelectorAll('.tx-checkbox:checked');
      const count = selected.length;
      const bulkBtn = document.getElementById('btn-bulk-delete');
      const countSpan = document.getElementById('selected-count');
      const masterCb = document.getElementById('select-all');
      const allCbs = document.querySelectorAll('.tx-checkbox');

      countSpan.innerText = count;
      if (count > 0) {
        bulkBtn.style.display = 'inline-flex';
      } else {
        bulkBtn.style.display = 'none';
      }

      if (allCbs.length > 0 && count === allCbs.length) {
        masterCb.checked = true;
      } else {
        masterCb.checked = false;
      }
    }

    async function deleteSingleTx(id) {
      if (!confirm(`Are you sure you want to permanently delete transaction ${id}?`)) return;

      try {
        const res = await fetch(`/admin/api/transactions/${id}`, { method: 'DELETE' });
        if (res.ok) {
          allTx = allTx.filter(t => t.id !== id);
          renderTx(allTx);
        } else {
          const err = await res.json();
          alert('Failed to delete: ' + (err.detail || 'Error'));
        }
      } catch(e) {
        alert('Network error: ' + e);
      }
    }

    async function deleteSelected() {
      const checked = Array.from(document.querySelectorAll('.tx-checkbox:checked')).map(cb => cb.value);
      if (checked.length === 0) return;

      if (!confirm(`Are you sure you want to permanently delete ${checked.length} selected transaction(s)?`)) return;

      try {
        const res = await fetch('/admin/api/transactions/delete-batch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ids: checked })
        });

        if (res.ok) {
          const result = await res.json();
          const toRemove = new Set(checked);
          allTx = allTx.filter(t => !toRemove.has(t.id));
          renderTx(allTx);
        } else {
          const err = await res.json();
          alert('Failed to delete batch: ' + (err.detail || 'Error'));
        }
      } catch(e) {
        alert('Network error: ' + e);
      }
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
