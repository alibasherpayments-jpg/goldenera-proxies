DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: #09090b;
      color: #fafafa;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
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
    .nav-link.active { background: #18181b; color: #10b981; border: 1px solid #27272a; font-weight: 600; }
    .nav-badge {
      margin-left: auto;
      background: rgba(245, 158, 11, 0.2);
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.4);
      font-size: 0.7rem;
      padding: 1px 7px;
      border-radius: 10px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
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
      position: relative;
      overflow: hidden;
    }
    .kpi-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: #27272a;
    }
    .kpi-card.accent-emerald::before { background: #10b981; }
    .kpi-card.accent-blue::before { background: #3b82f6; }
    .kpi-card.accent-amber::before { background: #f59e0b; }
    .kpi-card.accent-purple::before { background: #a855f7; }

    .kpi-label { font-size: 0.75rem; color: #71717a; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; }
    .kpi-value { font-size: 1.85rem; font-weight: 700; margin: 0.5rem 0 0.25rem; font-family: 'JetBrains Mono', monospace; }
    .kpi-sub { font-size: 0.75rem; color: #a1a1aa; font-weight: 500; }

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
    .card-title { font-size: 0.95rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th {
      background: #09090b;
      color: #71717a;
      font-weight: 600;
      padding: 0.75rem 1.25rem;
      border-bottom: 1px solid #27272a;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.05em;
    }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #18181b; }
    
    /* Badges & Buttons */
    .account-id-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 600;
      color: #f59e0b;
      background: rgba(245, 158, 11, 0.1);
      border: 1px solid rgba(245, 158, 11, 0.25);
      padding: 2px 7px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
    }
    .badge-pending, .badge-queued { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-approved, .badge-succeeded { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-rejected, .badge-failed { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    .btn-action {
      padding: 5px 12px;
      border-radius: 5px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.15s;
    }
    .btn-approve { background: #10b981; color: #09090b; }
    .btn-approve:hover { background: #059669; }
    .btn-reject { background: #ef4444; color: #fafafa; margin-left: 6px; }
    .btn-reject:hover { background: #dc2626; }
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
      <li class="nav-item"><a href="/admin/users" class="nav-link">👥 Users & Accounts</a></li>
      <li class="nav-item"><a href="/admin/transactions" class="nav-link">📜 Transactions History</a></li>
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
        <div class="kpi-card accent-blue">
          <div class="kpi-label">Total Users</div>
          <div class="kpi-value" id="kpi-users">—</div>
          <div class="kpi-sub">Bot Accounts Registered</div>
        </div>
        <div class="kpi-card accent-emerald">
          <div class="kpi-label">Active Proxies</div>
          <div class="kpi-value" id="kpi-proxies" style="color: #10b981;">—</div>
          <div class="kpi-sub">Live Instances Active</div>
        </div>
        <div class="kpi-card accent-purple">
          <div class="kpi-label">Today Revenue</div>
          <div class="kpi-value" id="kpi-revenue">—</div>
          <div class="kpi-sub" id="kpi-orders-count">0 orders today</div>
        </div>
        <div class="kpi-card accent-amber">
          <div class="kpi-label">Magnum API Credit</div>
          <div class="kpi-value" id="kpi-magnum">—</div>
          <div class="kpi-sub" id="kpi-magnum-status">Upstream Provider Balance</div>
        </div>
      </div>

      <div class="card-box">
        <div class="card-header">
          <div class="card-title">💳 Pending Deposits (Action Required)</div>
          <a href="/admin/deposits" style="font-size: 0.8rem; color: #10b981; font-weight: 500;">View All Deposits →</a>
        </div>
        <table>
          <thead>
            <tr>
              <th>Deposit ID</th>
              <th>Account ID</th>
              <th>Customer</th>
              <th>Method</th>
              <th>Sender Phone / TxID</th>
              <th>Amount (USD / EGP)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="pending-deposits-body">
            <tr><td colspan="7" style="text-align: center; color: #71717a; padding: 2rem;">Loading pending queue...</td></tr>
          </tbody>
        </table>
      </div>

      <div class="card-box">
        <div class="card-header">
          <div class="card-title">⚡ Recent Orders & Dispatch Log</div>
          <a href="/admin/transactions" style="font-size: 0.8rem; color: #3b82f6; font-weight: 500;">All Transactions →</a>
        </div>
        <table>
          <thead>
            <tr>
              <th>Order Ref</th>
              <th>Account ID</th>
              <th>Customer</th>
              <th>Product Code</th>
              <th>Status</th>
              <th>Amount (USD)</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody id="recent-orders-body">
            <tr><td colspan="7" style="text-align: center; color: #71717a; padding: 2rem;">Loading orders...</td></tr>
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
        document.getElementById('kpi-orders-count').textContent = (d.today_orders || 0) + ' orders today';
        document.getElementById('kpi-magnum').textContent = (d.magnum_balance >= 0) ? ('$' + d.magnum_balance.toFixed(2)) : 'N/A';

        if (d.pending_deposits_count > 0) {
          const badge = document.getElementById('pending-badge');
          badge.textContent = d.pending_deposits_count;
          badge.style.display = 'inline-block';
        }

        // Render Recent Orders
        const ordBody = document.getElementById('recent-orders-body');
        const orders = d.recent_orders || [];
        if (orders.length > 0) {
          ordBody.innerHTML = orders.map(o => `
            <tr>
              <td style="font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #a1a1aa;">#${o.id}</td>
              <td><span class="account-id-badge">🆔 ${o.account_id || o.telegram_id}</span></td>
              <td><strong>${o.username ? '@' + o.username : (o.telegram_id || '—')}</strong></td>
              <td style="font-family: 'JetBrains Mono', monospace; color: #38bdf8;">${o.product_code}</td>
              <td><span class="badge badge-${o.status}">${o.status}</span></td>
              <td style="font-weight: 700; color: #10b981; font-family: monospace;">$${(o.amount || 0).toFixed(2)}</td>
              <td style="color: #71717a; font-size: 0.8rem;">${o.created_at ? new Date(o.created_at).toLocaleString() : '—'}</td>
            </tr>
          `).join('');
        } else {
          ordBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #71717a; padding: 2rem;">No orders recorded yet.</td></tr>';
        }
      } catch (e) {
        console.error(e);
      }
    }

    async function loadPendingDeposits() {
      try {
        const res = await fetch('/admin/api/deposits?status=pending');
        if (!res.ok) return;
        const data = await res.json();
        const deposits = data.deposits || (Array.isArray(data) ? data : []);
        const tbody = document.getElementById('pending-deposits-body');
        if (!deposits || deposits.length === 0) {
          tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #71717a; padding: 2rem;">No pending deposits in queue.</td></tr>';
          return;
        }
        tbody.innerHTML = deposits.map(dep => `
          <tr>
            <td style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">#${dep.id}</td>
            <td><span class="account-id-badge">🆔 ${dep.user_account_id || dep.user_telegram_id}</span></td>
            <td><strong>${dep.user_name || dep.user_telegram_id}</strong></td>
            <td><span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 700; color: #38bdf8;">${dep.method}</span></td>
            <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;">${dep.sender_phone || dep.txid || '—'}</td>
            <td><strong style="color: #10b981; font-family: monospace;">$${(dep.amount_usd || 0).toFixed(2)}</strong> <span style="color:#71717a; font-size: 0.78rem;">(${dep.amount_local || 0} EGP)</span></td>
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
