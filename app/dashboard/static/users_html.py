USERS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Users & Accounts</title>
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
    .search-input:focus { border-color: #10b981; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: #09090b; color: #71717a; font-weight: 600; padding: 0.75rem 1.25rem; border-bottom: 1px solid #27272a; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:hover td { background: #18181b; }
    .account-id-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #f59e0b; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); padding: 3px 8px; border-radius: 4px; display: inline-flex; align-items: center; gap: 4px; }
    .points-badge { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #10b981; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25); padding: 2px 7px; border-radius: 4px; font-size: 0.8rem; }
    .btn-action { padding: 5px 10px; border-radius: 5px; font-size: 0.75rem; font-weight: 600; cursor: pointer; border: 1px solid #3f3f46; background: #18181b; color: #e4e4e7; transition: all 0.15s; }
    .btn-action:hover { border-color: #10b981; color: #10b981; background: #27272a; }
    .btn-history { border-color: #3b82f6; color: #93c5fd; }
    .btn-history:hover { border-color: #60a5fa; color: #bfdbfe; background: rgba(59, 130, 246, 0.15); }
    
    /* Modal styles */
    .modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.8); display: none; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; backdrop-filter: blur(4px); }
    .modal-card { background: #121214; border: 1px solid #27272a; border-radius: 12px; width: 100%; max-width: 760px; max-height: 85vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
    .modal-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid #27272a; display: flex; justify-content: space-between; align-items: center; background: #0f0f11; }
    .modal-body { padding: 1.5rem; overflow-y: auto; flex: 1; }
    .modal-close { background: none; border: none; color: #71717a; font-size: 1.5rem; cursor: pointer; line-height: 1; }
    .modal-close:hover { color: #fff; }
    .tx-item { display: flex; justify-content: space-between; align-items: center; padding: 0.85rem 1rem; border: 1px solid #27272a; border-radius: 8px; margin-bottom: 0.6rem; background: #18181b; }
    .tx-pos { color: #10b981; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .tx-neg { color: #ef4444; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header"><div class="logo-box">G</div><div class="logo-text">GoldenEra 5G</div></div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link active">👥 Users & Accounts</a></li>
      <li class="nav-item"><a href="/admin/transactions" class="nav-link">📜 Transactions History</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link">💳 Deposits</a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.4.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Users & Account Management</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="card-box">
        <div class="card-header">
          <div>
            <div style="font-weight: 600; font-size: 1rem;">Customer Accounts</div>
            <div style="color: #71717a; font-size: 0.78rem;">Track customer random numeric IDs, points balance, and transactions history.</div>
          </div>
          <input type="text" id="search-box" class="search-input" placeholder="🔍 Search by Account ID, Telegram ID, or Username..." oninput="filterUsers()">
        </div>
        <table>
          <thead>
            <tr>
              <th>Account ID</th>
              <th>Telegram ID</th>
              <th>Username</th>
              <th>Language</th>
              <th>Points</th>
              <th>Balance (USD)</th>
              <th>Total Spent</th>
              <th>Joined Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="users-body">
            <tr><td colspan="9" style="text-align: center; color: #71717a; padding: 2rem;">Loading users...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Transactions Modal -->
  <div id="tx-modal" class="modal-overlay" onclick="closeModalOnOverlay(event)">
    <div class="modal-card">
      <div class="modal-header">
        <div>
          <div id="modal-title" style="font-weight: 700; font-size: 1rem;">📜 Transactions History</div>
          <div id="modal-subtitle" style="font-size: 0.8rem; color: #a1a1aa; font-family: monospace;"></div>
        </div>
        <button class="modal-close" onclick="closeModal()">×</button>
      </div>
      <div class="modal-body" id="modal-content">
        Loading transactions...
      </div>
    </div>
  </div>

  <script>
    let allUsers = [];

    async function loadUsers() {
      try {
        const res = await fetch('/admin/api/users');
        const data = await res.json();
        allUsers = data.users || [];
        renderUsers(allUsers);
      } catch(e) {
        console.error(e);
      }
    }

    function renderUsers(users) {
      const tbody = document.getElementById('users-body');
      if (!users || users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: #71717a; padding: 2rem;">No users found.</td></tr>';
        return;
      }
      tbody.innerHTML = users.map(u => `
        <tr>
          <td><span class="account-id-badge">🆔 ${u.account_id || u.telegram_id}</span></td>
          <td style="font-family: 'JetBrains Mono', monospace; color: #a1a1aa;">${u.telegram_id}</td>
          <td><strong>${u.username ? '@' + u.username : (u.first_name || '—')}</strong></td>
          <td><span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 600; color: #10b981;">${u.language || 'ar'}</span></td>
          <td><span class="points-badge">${u.points || 0} pts</span></td>
          <td style="font-weight: 700; color: #10b981; font-family: monospace;">$${(u.balance || 0).toFixed(2)}</td>
          <td style="color: #71717a; font-family: monospace;">$${(u.total_spent || 0).toFixed(2)}</td>
          <td style="color: #71717a; font-size: 0.8rem;">${u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}</td>
          <td style="white-space: nowrap;">
            <button class="btn-action" onclick="adjustBalance(${u.telegram_id})">💰 Adjust</button>
            <button class="btn-action btn-history" onclick="viewHistory(${u.telegram_id}, '${u.account_id || u.telegram_id}')">📜 History</button>
          </td>
        </tr>
      `).join('');
    }

    function filterUsers() {
      const q = document.getElementById('search-box').value.toLowerCase().trim();
      const filtered = allUsers.filter(u => 
        (u.account_id && u.account_id.toLowerCase().includes(q)) ||
        String(u.telegram_id).includes(q) || 
        (u.username && u.username.toLowerCase().includes(q)) ||
        (u.first_name && u.first_name.toLowerCase().includes(q))
      );
      renderUsers(filtered);
    }

    async function adjustBalance(tgId) {
      const amountStr = prompt('Enter amount to add (+) or deduct (-) in USD:\\n(Note: Every $1.00 = 100 Points)');
      if (!amountStr) return;
      const amount = parseFloat(amountStr);
      if (isNaN(amount)) return alert('Invalid amount');

      try {
        const res = await fetch(`/admin/api/users/${tgId}/balance`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ amount: amount, note: 'Admin manual adjustment' })
        });
        if (res.ok) {
          alert('Balance and points updated successfully');
          loadUsers();
        } else {
          alert('Failed to update balance');
        }
      } catch(e) {
        alert(e);
      }
    }

    async function viewHistory(tgId, accId) {
      const modal = document.getElementById('tx-modal');
      const subtitle = document.getElementById('modal-subtitle');
      const content = document.getElementById('modal-content');
      
      modal.style.display = 'flex';
      subtitle.innerText = `Account ID: ${accId} | Telegram ID: ${tgId}`;
      content.innerHTML = '<div style="text-align: center; color: #a1a1aa; padding: 2rem;">Loading transactions history...</div>';

      try {
        const res = await fetch(`/admin/api/users/${tgId}/transactions`);
        const data = await res.json();
        const txs = data.transactions || [];

        if (txs.length === 0) {
          content.innerHTML = '<div style="text-align: center; color: #71717a; padding: 2rem;">No transactions recorded for this user yet.</div>';
          return;
        }

        content.innerHTML = txs.map(t => {
          const isPos = t.amount >= 0;
          const amtColor = isPos ? 'tx-pos' : 'tx-neg';
          const sign = isPos ? '+' : '';
          const ptsSign = t.points >= 0 ? '+' : '';
          const badgeBg = t.status === 'approved' || t.status === 'succeeded' ? '#10b981' : (t.status === 'pending' || t.status === 'queued' ? '#f59e0b' : '#ef4444');

          return `
            <div class="tx-item">
              <div>
                <div style="font-weight: 600; font-size: 0.9rem;">${t.details}</div>
                <div style="font-size: 0.75rem; color: #71717a; margin-top: 3px;">
                  <span>Ref: <code style="color: #a1a1aa;">${t.txid}</code></span> • 
                  <span>${t.date ? new Date(t.date).toLocaleString() : '—'}</span>
                </div>
              </div>
              <div style="text-align: right;">
                <div class="${amtColor}">${sign}$${Math.abs(t.amount).toFixed(2)} <span style="font-size: 0.75rem; opacity: 0.85;">(${ptsSign}${t.points} pts)</span></div>
                <span style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: ${badgeBg};">${t.status}</span>
              </div>
            </div>
          `;
        }).join('');

      } catch(e) {
        content.innerHTML = '<div style="color: #ef4444; text-align: center; padding: 2rem;">Failed to load transactions.</div>';
      }
    }

    function closeModal() {
      document.getElementById('tx-modal').style.display = 'none';
    }

    function closeModalOnOverlay(e) {
      if (e.target.id === 'tx-modal') closeModal();
    }

    loadUsers();
  </script>
</body>
</html>"""
