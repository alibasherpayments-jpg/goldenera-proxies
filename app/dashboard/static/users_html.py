USERS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Users & Wallets</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
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
    .nav-link { display: flex; align-items: center; gap: 0.75rem; padding: 0.65rem 0.75rem; border-radius: 6px; font-size: 0.875rem; font-weight: 500; color: #a1a1aa; }
    .nav-link:hover { background: #18181b; color: #fafafa; }
    .nav-link.active { background: #18181b; color: #10b981; border: 1px solid #27272a; }
    .sidebar-footer { padding: 1rem 1.25rem; border-top: 1px solid #1f1f23; font-size: 0.8rem; color: #71717a; display: flex; justify-content: space-between; }
    .logout-btn { color: #ef4444; font-weight: 500; }
    .main-wrap { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
    .top-bar { height: 64px; border-bottom: 1px solid #27272a; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; background: #0f0f11; }
    .top-title { font-size: 1.1rem; font-weight: 600; }
    .admin-pill { background: #18181b; border: 1px solid #27272a; padding: 0.35rem 0.75rem; border-radius: 20px; font-size: 0.8rem; color: #a1a1aa; }
    .admin-pill span { color: #10b981; font-weight: 600; }
    .content-area { padding: 2rem; flex: 1; }
    .card-box { background: #121214; border: 1px solid #27272a; border-radius: 8px; overflow: hidden; }
    .card-header { padding: 1rem 1.25rem; border-bottom: 1px solid #27272a; display: flex; justify-content: space-between; align-items: center; }
    .search-input { background: #18181b; border: 1px solid #27272a; padding: 0.4rem 0.75rem; border-radius: 6px; color: #fff; font-size: 0.85rem; outline: none; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: #09090b; color: #71717a; font-weight: 600; padding: 0.75rem 1.25rem; border-bottom: 1px solid #27272a; text-transform: uppercase; font-size: 0.75rem; }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:hover td { background: #18181b; }
    .btn-action { padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; cursor: pointer; border: 1px solid #3f3f46; background: #18181b; color: #e4e4e7; }
    .btn-action:hover { border-color: #10b981; color: #10b981; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header"><div class="logo-box">G</div><div class="logo-text">GoldenEra 5G</div></div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link active">👥 Users & Wallets</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link">💳 Deposits</a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.4.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Users & Balances</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="card-box">
        <div class="card-header">
          <div style="font-weight: 600;">Registered Telegram Users</div>
          <input type="text" id="search-box" class="search-input" placeholder="Search by ID or username..." oninput="filterUsers()">
        </div>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Telegram ID</th>
              <th>Username</th>
              <th>Language</th>
              <th>Balance</th>
              <th>Total Spent</th>
              <th>Joined Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="users-body">
            <tr><td colspan="8" style="text-align: center; color: #71717a;">Loading users...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    let allUsers = [];

    async function loadUsers() {
      try {
        const res = await fetch('/admin/api/users');
        allUsers = await res.json();
        renderUsers(allUsers);
      } catch(e) {
        console.error(e);
      }
    }

    function renderUsers(users) {
      const tbody = document.getElementById('users-body');
      if (!users || users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #71717a;">No users found.</td></tr>';
        return;
      }
      tbody.innerHTML = users.map(u => `
        <tr>
          <td>#${u.id}</td>
          <td style="font-family: monospace;">${u.telegram_id}</td>
          <td><strong>${u.username ? '@' + u.username : (u.first_name || '—')}</strong></td>
          <td><span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 600; color: #10b981;">${u.language}</span></td>
          <td style="font-weight: 700; color: #10b981;">$${(u.balance || 0).toFixed(2)}</td>
          <td style="color: #71717a;">$${(u.total_spent || 0).toFixed(2)}</td>
          <td style="color: #71717a;">${new Date(u.created_at).toLocaleDateString()}</td>
          <td>
            <button class="btn-action" onclick="adjustBalance(${u.telegram_id})">Adjust Balance</button>
          </td>
        </tr>
      `).join('');
    }

    function filterUsers() {
      const q = document.getElementById('search-box').value.toLowerCase();
      const filtered = allUsers.filter(u => 
        String(u.telegram_id).includes(q) || 
        (u.username && u.username.toLowerCase().includes(q)) ||
        (u.first_name && u.first_name.toLowerCase().includes(q))
      );
      renderUsers(filtered);
    }

    async function adjustBalance(tgId) {
      const amountStr = prompt('Enter amount to add (positive) or deduct (negative) in USD:');
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
          alert('Balance updated successfully');
          loadUsers();
        } else {
          alert('Failed to update balance');
        }
      } catch(e) {
        alert(e);
      }
    }

    loadUsers();
  </script>
</body>
</html>"""
