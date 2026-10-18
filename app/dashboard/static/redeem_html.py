REDEEM_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Redeem Codes & Promos</title>
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

    /* Stats Grid */
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
    .stat-card { background: #121214; border: 1px solid #27272a; border-radius: 8px; padding: 1.25rem; }
    .stat-label { font-size: 0.8rem; color: #71717a; font-weight: 500; margin-bottom: 0.4rem; display: flex; align-items: center; justify-content: space-between; }
    .stat-val { font-size: 1.5rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }

    /* Generator Box */
    .create-card { background: #121214; border: 1px solid #27272a; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; }
    .card-title { font-size: 1rem; font-weight: 600; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; color: #10b981; }
    .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }
    .field-group { display: flex; flex-direction: column; gap: 0.4rem; }
    .field-label { font-size: 0.78rem; font-weight: 600; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.04em; }
    .input-field, .select-field { background: #18181b; border: 1px solid #27272a; color: #fff; padding: 0.6rem 0.85rem; border-radius: 6px; font-size: 0.85rem; outline: none; transition: border-color 0.15s; }
    .input-field:focus, .select-field:focus { border-color: #10b981; }
    .code-input-wrap { display: flex; gap: 0.5rem; }
    .btn-secondary { background: #27272a; border: 1px solid #3f3f46; color: #fafafa; padding: 0.6rem 0.9rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; white-space: nowrap; }
    .btn-secondary:hover { background: #3f3f46; }
    .btn-primary { background: #10b981; color: #09090b; border: none; padding: 0.65rem 1.5rem; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: background 0.15s; }
    .btn-primary:hover { background: #059669; }

    /* Filter Toolbar */
    .toolbar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem; }
    .filter-bar { display: flex; gap: 0.5rem; }
    .filter-btn { background: #18181b; border: 1px solid #27272a; color: #a1a1aa; padding: 0.45rem 0.9rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
    .filter-btn:hover { background: #27272a; color: #fafafa; }
    .filter-btn.active { background: #27272a; color: #10b981; border-color: #10b981; }
    .search-input { background: #18181b; border: 1px solid #27272a; padding: 0.5rem 0.85rem; border-radius: 6px; color: #fff; font-size: 0.85rem; outline: none; width: 280px; }
    .search-input:focus { border-color: #10b981; }

    /* Tables */
    .table-card { background: #121214; border: 1px solid #27272a; border-radius: 8px; overflow: hidden; margin-bottom: 2rem; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: #09090b; color: #71717a; font-weight: 600; padding: 0.75rem 1.25rem; border-bottom: 1px solid #27272a; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.05em; }
    td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #1f1f23; }
    tr:hover td { background: #18181b; }

    .code-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #10b981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); padding: 3px 8px; border-radius: 5px; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; }
    .code-badge:hover { background: rgba(16, 185, 129, 0.2); }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; }
    .badge-active { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-expired { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-used { background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
    .badge-disabled { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }

    .badge-type-balance { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-type-bonus { background: rgba(236, 72, 153, 0.15); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); }

    .btn-action-del { background: transparent; border: 1px solid #3f3f46; color: #ef4444; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; cursor: pointer; transition: all 0.15s; }
    .btn-action-del:hover { background: #ef4444; color: #fff; border-color: #ef4444; }
    .btn-action-toggle { background: transparent; border: 1px solid #3f3f46; color: #a1a1aa; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; cursor: pointer; margin-right: 4px; }
    .btn-action-toggle:hover { background: #27272a; color: #fff; }

    .alert { padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem; display: none; }
    .alert-success { background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #10b981; }
    .alert-error { background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #ef4444; }
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
      <li class="nav-item"><a href="/admin/redeem" class="nav-link active">🎁 Redeem Codes</a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.5.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Redeem Codes & Promo Rewards</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <!-- Alerts -->
      <div id="alertSuccess" class="alert alert-success"></div>
      <div id="alertError" class="alert alert-error"></div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">🟢 Working & Active Codes</div>
          <div class="stat-val" style="color: #10b981;" id="statActive">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">⌛ Expired Codes</div>
          <div class="stat-val" style="color: #f59e0b;" id="statExpired">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">🔴 Fully Used Codes</div>
          <div class="stat-val" style="color: #818cf8;" id="statExhausted">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">👥 Total Redemptions</div>
          <div class="stat-val" style="color: #fafafa;" id="statRedemptions">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">💰 Total Rewards Credited</div>
          <div class="stat-val" style="color: #10b981;" id="statCredited">$0.00</div>
        </div>
      </div>

      <!-- Generator Box -->
      <div class="create-card">
        <div class="card-title">✨ Create & Generate New Promo Code</div>
        <form id="createForm">
          <div class="form-grid">
            <div class="field-group">
              <label class="field-label">Promo Code</label>
              <div class="code-input-wrap">
                <input type="text" id="codeVal" class="input-field" placeholder="e.g. BONUS50 or GOLD-7X9K" style="flex: 1;" required>
                <button type="button" class="btn-secondary" onclick="generateRandom()">⚡ Auto</button>
              </div>
            </div>

            <div class="field-group">
              <label class="field-label">Reward Type / Category</label>
              <select id="codeType" class="select-field" onchange="toggleBonusFields()">
                <option value="balance">💰 Direct Balance (رصيد مباشر في المحفظة)</option>
                <option value="deposit_bonus">🚀 Deposit Bonus (عرض عند الإيداع - مثلاً إيداع 1$ والحصول على 0.5$)</option>
              </select>
            </div>

            <div class="field-group">
              <label class="field-label" id="rewardLabel">Reward Value ($ USD)</label>
              <input type="number" step="0.01" min="0.01" id="rewardAmount" class="input-field" placeholder="e.g. 0.50 or 5.00" required>
            </div>

            <div class="field-group" id="minDepositGroup" style="display: none;">
              <label class="field-label">Min Deposit Required ($ USD)</label>
              <input type="number" step="0.01" min="0" id="minDeposit" class="input-field" placeholder="e.g. 1.00" value="1.00">
            </div>

            <div class="field-group">
              <label class="field-label">Max Uses (عدد مرات الاستخدام الكلية)</label>
              <input type="number" min="1" id="maxUses" class="input-field" value="1" placeholder="1 = single-use, 100 = 100 users" required>
            </div>

            <div class="field-group">
              <label class="field-label">Expiration Date (Optional)</label>
              <input type="datetime-local" id="expiresAt" class="input-field">
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center;">
            <input type="text" id="codeNote" class="input-field" placeholder="Admin note / description (e.g. VIP Gift or Launch Promo)" style="width: 450px;">
            <button type="submit" class="btn-primary">➕ Create Promo Code</button>
          </div>
        </form>
      </div>

      <!-- Codes List Toolbar -->
      <div class="toolbar">
        <div class="filter-bar">
          <button class="filter-btn active" onclick="setTab('all')">All Codes</button>
          <button class="filter-btn" onclick="setTab('active')">🟢 Working / Active</button>
          <button class="filter-btn" onclick="setTab('used')">🔴 Fully Used</button>
          <button class="filter-btn" onclick="setTab('expired')">⌛ Expired</button>
        </div>
        <input type="text" class="search-input" id="searchInput" placeholder="🔍 Search code or note..." oninput="filterTable()">
      </div>

      <!-- Codes Table -->
      <div class="table-card">
        <table>
          <thead>
            <tr>
              <th>Code</th>
              <th>Type</th>
              <th>Reward</th>
              <th>Min Deposit</th>
              <th>Redeemed / Max</th>
              <th>Status</th>
              <th>Expires At</th>
              <th>Note</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="codesTbody">
            <tr><td colspan="9" style="text-align: center; color: #71717a; padding: 2rem;">Loading promo codes...</td></tr>
          </tbody>
        </table>
      </div>

      <!-- Recent Redemptions Table -->
      <div class="toolbar" style="margin-top: 3rem;">
        <div style="font-size: 1rem; font-weight: 600; color: #fafafa;">📜 Recent Code Redemptions Log</div>
      </div>
      <div class="table-card">
        <table>
          <thead>
            <tr>
              <th>User Account ID</th>
              <th>Telegram ID</th>
              <th>User Name</th>
              <th>Code Used</th>
              <th>Type</th>
              <th>Reward Credited</th>
              <th>Status</th>
              <th>Date & Time</th>
            </tr>
          </thead>
          <tbody id="usagesTbody">
            <tr><td colspan="8" style="text-align: center; color: #71717a; padding: 2rem;">Loading redemptions log...</td></tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>

  <script>
    let currentTab = 'all';
    let codesData = [];

    function showAlert(msg, isSuccess = true) {
      const s = document.getElementById('alertSuccess');
      const e = document.getElementById('alertError');
      if (isSuccess) {
        s.textContent = msg; s.style.display = 'block'; e.style.display = 'none';
        setTimeout(() => s.style.display = 'none', 4000);
      } else {
        e.textContent = msg; e.style.display = 'block'; s.style.display = 'none';
        setTimeout(() => e.style.display = 'none', 4000);
      }
    }

    function generateRandom() {
      const type = document.getElementById('codeType').value;
      const prefix = type === 'deposit_bonus' ? 'BONUS' : 'GOLD';
      const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
      let p1 = '', p2 = '';
      for (let i = 0; i < 4; i++) p1 += chars.charAt(Math.floor(Math.random() * chars.length));
      for (let i = 0; i < 4; i++) p2 += chars.charAt(Math.floor(Math.random() * chars.length));
      document.getElementById('codeVal').value = `${prefix}-${p1}-${p2}`;
    }

    function toggleBonusFields() {
      const type = document.getElementById('codeType').value;
      const minGroup = document.getElementById('minDepositGroup');
      const label = document.getElementById('rewardLabel');
      if (type === 'deposit_bonus') {
        minGroup.style.display = 'flex';
        label.textContent = 'Bonus Value ($ USD)';
      } else {
        minGroup.style.display = 'none';
        label.textContent = 'Balance Value ($ USD)';
      }
    }

    function copyCode(code) {
      navigator.clipboard.writeText(code).then(() => {
        showAlert(`📋 Code "${code}" copied to clipboard!`, true);
      });
    }

    function setTab(tab) {
      currentTab = tab;
      document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.toLowerCase().includes(tab) || (tab === 'all' && btn.textContent === 'All Codes'));
      });
      loadData();
    }

    async function loadData() {
      try {
        const [statsRes, codesRes, usagesRes] = await Promise.all([
          fetch('/admin/api/redeem/stats'),
          fetch(`/admin/api/redeem/codes?tab=${currentTab}`),
          fetch('/admin/api/redeem/usages'),
        ]);

        const stats = await statsRes.json();
        document.getElementById('statActive').textContent = stats.active_codes;
        document.getElementById('statExpired').textContent = stats.expired_codes;
        document.getElementById('statExhausted').textContent = stats.exhausted_codes;
        document.getElementById('statRedemptions').textContent = stats.total_redemptions;
        document.getElementById('statCredited').textContent = `$${stats.total_rewards_credited.toFixed(2)}`;

        codesData = await codesRes.json();
        renderCodes(codesData);

        const usages = await usagesRes.json();
        renderUsages(usages);
      } catch (err) {
        console.error(err);
      }
    }

    function renderCodes(list) {
      const tbody = document.getElementById('codesTbody');
      if (!list || list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: #71717a; padding: 2rem;">No promo codes found in this filter.</td></tr>';
        return;
      }

      tbody.innerHTML = list.map(c => {
        let statusBadge = '';
        if (c.status === 'active') statusBadge = '<span class="badge badge-active">🟢 Active</span>';
        else if (c.status === 'expired') statusBadge = '<span class="badge badge-expired">⌛ Expired</span>';
        else if (c.status === 'used') statusBadge = '<span class="badge badge-used">🔴 Used Up</span>';
        else statusBadge = '<span class="badge badge-disabled">Disabled</span>';

        const typeBadge = c.code_type === 'balance'
          ? '<span class="badge badge-type-balance">💰 Direct Balance</span>'
          : '<span class="badge badge-type-bonus">🚀 Deposit Bonus</span>';

        const rewardTxt = c.code_type === 'balance'
          ? `<strong>$${c.reward_amount.toFixed(2)}</strong> (${Math.round(c.reward_amount * 100)} pts)`
          : `+<strong>$${c.reward_amount.toFixed(2)}</strong> Bonus`;

        const minDepTxt = c.code_type === 'deposit_bonus'
          ? `$${c.min_deposit.toFixed(2)}`
          : '—';

        const expiryTxt = c.expires_at ? new Date(c.expires_at).toLocaleString() : '<span style="color:#71717a;">Never</span>';

        return `
          <tr>
            <td><span class="code-badge" onclick="copyCode('${c.code}')">${c.code} 📋</span></td>
            <td>${typeBadge}</td>
            <td>${rewardTxt}</td>
            <td>${minDepTxt}</td>
            <td><strong>${c.used_count}</strong> / ${c.max_uses} <span style="font-size:0.75rem; color:#71717a;">(${c.remaining_uses} left)</span></td>
            <td>${statusBadge}</td>
            <td style="font-size: 0.8rem; color: #a1a1aa;">${expiryTxt}</td>
            <td style="color: #71717a; font-size: 0.8rem;">${c.note || '—'}</td>
            <td>
              <button class="btn-action-toggle" onclick="toggleCode(${c.id}, ${!c.is_active})">${c.is_active ? 'Disable' : 'Enable'}</button>
              <button class="btn-action-del" onclick="deleteCode(${c.id}, '${c.code}')">Delete</button>
            </td>
          </tr>
        `;
      }).join('');
    }

    function renderUsages(list) {
      const tbody = document.getElementById('usagesTbody');
      if (!list || list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #71717a; padding: 2rem;">No code redemptions recorded yet.</td></tr>';
        return;
      }

      tbody.innerHTML = list.map(u => {
        const typeBadge = u.code_type === 'balance'
          ? '<span class="badge badge-type-balance">Direct Balance</span>'
          : '<span class="badge badge-type-bonus">Deposit Bonus</span>';

        const statusBadge = u.status === 'completed'
          ? '<span class="badge badge-active">Credited</span>'
          : '<span class="badge badge-expired">Pending Deposit</span>';

        return `
          <tr>
            <td><code style="color: #f59e0b;">${u.account_id}</code></td>
            <td><code>${u.user_id}</code></td>
            <td>${u.first_name || u.username || 'User'}</td>
            <td><span class="code-badge" style="font-size: 0.75rem;">${u.code}</span></td>
            <td>${typeBadge}</td>
            <td style="color: #10b981; font-weight: 700;">+$${u.reward_credited.toFixed(2)}</td>
            <td>${statusBadge}</td>
            <td style="font-size: 0.78rem; color: #a1a1aa;">${u.used_at ? new Date(u.used_at).toLocaleString() : '—'}</td>
          </tr>
        `;
      }).join('');
    }

    function filterTable() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const filtered = codesData.filter(c => c.code.toLowerCase().includes(q) || (c.note && c.note.toLowerCase().includes(q)));
      renderCodes(filtered);
    }

    async function toggleCode(id, newStatus) {
      try {
        const res = await fetch(`/admin/api/redeem/codes/${id}/toggle`, { method: 'POST' });
        if (res.ok) {
          showAlert('Code status updated!', true);
          loadData();
        }
      } catch (e) { showAlert(e.message, false); }
    }

    async function deleteCode(id, code) {
      if (!confirm(`Are you sure you want to delete code "${code}"?`)) return;
      try {
        const res = await fetch(`/admin/api/redeem/codes/${id}`, { method: 'DELETE' });
        if (res.ok) {
          showAlert(`Code "${code}" deleted.`, true);
          loadData();
        }
      } catch (e) { showAlert(e.message, false); }
    }

    document.getElementById('createForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const code = document.getElementById('codeVal').value.trim();
      const codeType = document.getElementById('codeType').value;
      const rewardAmount = parseFloat(document.getElementById('rewardAmount').value);
      const minDeposit = parseFloat(document.getElementById('minDeposit').value || 0);
      const maxUses = parseInt(document.getElementById('maxUses').value || 1);
      const expiresAt = document.getElementById('expiresAt').value || null;
      const note = document.getElementById('codeNote').value.trim();

      try {
        const res = await fetch('/admin/api/redeem/codes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            code,
            code_type: codeType,
            reward_amount: rewardAmount,
            min_deposit: minDeposit,
            max_uses: maxUses,
            expires_at: expiresAt,
            note,
          }),
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed to create code');

        showAlert(`✅ Code "${code}" created successfully!`, true);
        document.getElementById('createForm').reset();
        document.getElementById('maxUses').value = 1;
        toggleBonusFields();
        loadData();
      } catch (err) {
        showAlert(err.message, false);
      }
    });

    loadData();
    setInterval(loadData, 20000);
  </script>
</body>
</html>
"""
