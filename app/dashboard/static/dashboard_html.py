DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: #09090b;
      color: #fafafa;
      font-family: 'Inter', -apple-system, sans-serif;
      display: flex;
      min-height: 100vh;
    }
    a { color: inherit; text-decoration: none; }
    
    /* Sidebar */
    .sidebar {
      width: 240px;
      background: #0f0f11;
      border-right: 1px solid #27272a;
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }
    .sidebar-header {
      padding: 1.5rem 1.25rem;
      border-bottom: 1px solid #1f1f23;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .logo-box {
      width: 32px;
      height: 32px;
      background: #18181b;
      border: 1px solid #3f3f46;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      color: #10b981;
    }
    .logo-text { font-weight: 600; font-size: 0.95rem; }
    .nav-list { list-style: none; padding: 1rem 0.75rem; flex: 1; }
    .nav-item { margin-bottom: 0.25rem; }
    .nav-link {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.65rem 0.75rem;
      border-radius: 6px;
      font-size: 0.875rem;
      font-weight: 500;
      color: #a1a1aa;
      transition: all 0.15s ease;
    }
    .nav-link:hover { background: #18181b; color: #fafafa; }
    .nav-link.active { background: #18181b; color: #10b981; border: 1px solid #27272a; }
    .nav-badge {
      margin-left: auto;
      background: #92400e;
      color: #fef3c7;
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 10px;
      font-weight: 600;
    }
    .sidebar-footer {
      padding: 1rem 1.25rem;
      border-top: 1px solid #1f1f23;
      font-size: 0.8rem;
      color: #71717a;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logout-btn { color: #ef4444; font-weight: 500; }

    /* Main Content */
    .main-wrap { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
    .top-bar {
      height: 64px;
      border-bottom: 1px solid #27272a;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 2rem;
      background: #0f0f11;
    }
    .top-title { font-size: 1.1rem; font-weight: 600; }
    .admin-pill {
      background: #18181b;
      border: 1px solid #27272a;
      padding: 0.35rem 0.75rem;
      border-radius: 20px;
      font-size: 0.8rem;
      color: #a1a1aa;
    }
    .admin-pill span { color: #10b981; font-weight: 600; }
    .content-area { padding: 2rem; flex: 1; }

    /* KPI Grid */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }
    .kpi-card {
      background: #121214;
      border: 1px solid #27272a;
      border-radius: 8px;
      padding: 1.25rem;
    }
    .kpi-label { font-size: 0.8rem; color: #71717a; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; }
    .kpi-value { font-size: 1.75rem; font-weight: 700; margin: 0.5rem 0 0.25rem; font-family: 'JetBrains Mono', monospace; }
    .kpi-sub { font-size: 0.75rem; color: #10b981; font-weight: 500; }

    /* Tables */
    .card-box {
      background: #121214;
      border: 1px solid #27272a;
      border-radius: 8px;
      margin-bottom: 2rem;
      overflow: hidden;
    }
    .card-header {
      padding: 1rem 1.25rem;
      border-bottom: 1px solid #27272a;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .card-title { font-size: 0.95rem; font-weight: 600; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th {
      background: #09090b;
      color: #71717a;
      font-weight: 600;
      padding: 0.75rem 1.25rem;
      border-bottom: 1px solid #27272a;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
    }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #18181b; }
    
    /* Badges & Buttons */
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
    }
    .badge-pending { background: #451a03; color: #f59e0b; border: 1px solid #92400e; }
    .badge-approved, .badge-succeeded { background: #022c22; color: #10b981; border: 1px solid #065f46; }
    .badge-rejected, .badge-failed { background: #450a0a; color: #ef4444; border: 1px solid #991b1b; }
    
    .btn-action {
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: opacity 0.15s;
    }
    .btn-action:hover { opacity: 0.85; }
    .btn-approve { background: #10b981; color: #09090b; }
    .btn-reject { background: #ef4444; color: #fafafa; margin-left: 4px; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="logo-box">G</div>
      <div class="logo-text">GoldenEra 5G</div>
    </div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link active">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link">👥 Users & Wallets</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link">💳 Deposits <span class="nav-badge" id="pending-badge" style="display:none">0</span></a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer">
      <span>v1.4.0</span>
      <a href="/admin/logout" class="logout-btn">Logout ↗</a>
    </div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Dashboard Overview</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">Total Users</div>
          <div class="kpi-value" id="kpi-users">—</div>
          <div class="kpi-sub">Bot Subscribers</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Active Proxies</div>
          <div class="kpi-value" id="kpi-proxies" style="color: #10b981;">—</div>
          <div class="kpi-sub">Currently Running</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Today Revenue</div>
          <div class="kpi-value" id="kpi-revenue">—</div>
          <div class="kpi-sub" id="kpi-orders-count">0 orders today</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Magnum API Credit</div>
          <div class="kpi-value" id="kpi-magnum">—</div>
          <div class="kpi-sub" id="kpi-magnum-status">Connected</div>
        </div>
      </div>

      <div class="card-box">
        <div class="card-header">
          <div class="card-title">Pending Deposits (Vodafone Cash)</div>
          <a href="/admin/deposits" style="font-size: 0.8rem; color: #10b981;">View All →</a>
        </div>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>Method</th>
              <th>Sender Phone</th>
              <th>TxID</th>
              <th>Amount (USD / EGP)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="pending-deposits-body">
            <tr><td colspan="7" style="text-align: center; color: #71717a;">Loading deposits...</td></tr>
          </tbody>
        </table>
      </div>

      <div class="card-box">
        <div class="card-header">
          <div class="card-title">Recent Proxy Orders</div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Order ID</th>
              <th>User ID</th>
              <th>Product Code</th>
              <th>Status</th>
              <th>Amount</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody id="recent-orders-body">
            <tr><td colspan="6" style="text-align: center; color: #71717a;">Loading orders...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    async function loadStats() {
      try {
        const res = await fetch('/admin/api/stats');
        if (!res.ok) return;
        const d = await res.json();
        document.getElementById('kpi-users').textContent = d.total_users;
        document.getElementById('kpi-proxies').textContent = d.active_proxies;
        document.getElementById('kpi-revenue').textContent = '$' + (d.today_revenue || 0).toFixed(2);
        document.getElementById('kpi-orders-count').textContent = d.today_orders + ' orders today';
        document.getElementById('kpi-magnum').textContent = '$' + (d.magnum_balance || 0).toFixed(2);

        if (d.pending_deposits_count > 0) {
          const badge = document.getElementById('pending-badge');
          badge.textContent = d.pending_deposits_count;
          badge.style.display = 'inline-block';
        }

        // Render Recent Orders
        const ordBody = document.getElementById('recent-orders-body');
        if (d.recent_orders && d.recent_orders.length > 0) {
          ordBody.innerHTML = d.recent_orders.map(o => `
            <tr>
              <td style="font-family: monospace;">#${o.id}</td>
              <td>${o.telegram_id || o.user_id}</td>
              <td style="font-family: monospace;">${o.product_code}</td>
              <td><span class="badge badge-${o.status}">${o.status}</span></td>
              <td style="font-weight: 600;">$${o.amount.toFixed(2)}</td>
              <td style="color: #71717a;">${new Date(o.created_at).toLocaleString()}</td>
            </tr>
          `).join('');
        } else {
          ordBody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #71717a;">No orders yet.</td></tr>';
        }
      } catch (e) {
        console.error(e);
      }
    }

    async function loadPendingDeposits() {
      try {
        const res = await fetch('/admin/api/deposits?status=pending');
        if (!res.ok) return;
        const deposits = await res.json();
        const tbody = document.getElementById('pending-deposits-body');
        if (!deposits || deposits.length === 0) {
          tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #71717a;">No pending deposits right now.</td></tr>';
          return;
        }
        tbody.innerHTML = deposits.map(dep => `
          <tr>
            <td>#${dep.id}</td>
            <td><strong>${dep.username || dep.telegram_id}</strong></td>
            <td>${dep.method}</td>
            <td style="font-family: monospace;">${dep.sender_phone || '—'}</td>
            <td style="font-family: monospace; font-size: 0.75rem;">${dep.txid}</td>
            <td><strong>$${dep.amount_usd.toFixed(2)}</strong> <span style="color:#71717a">(${dep.amount_local || 0} EGP)</span></td>
            <td>
              <button class="btn-action btn-approve" onclick="reviewDeposit(${dep.id}, 'approve')">Approve</button>
              <button class="btn-action btn-reject" onclick="reviewDeposit(${dep.id}, 'reject')">Reject</button>
            </td>
          </tr>
        `).join('');
      } catch (e) {
        console.error(e);
      }
    }

    async function reviewDeposit(id, action) {
      if (!confirm(`Are you sure you want to ${action} deposit #${id}?`)) return;
      try {
        const res = await fetch(`/admin/api/deposits/${id}/${action}`, { method: 'POST' });
        if (res.ok) {
          loadPendingDeposits();
          loadStats();
        } else {
          alert('Action failed');
        }
      } catch(e) {
        alert(e);
      }
    }

    loadStats();
    loadPendingDeposits();
  </script>
</body>
</html>"""
