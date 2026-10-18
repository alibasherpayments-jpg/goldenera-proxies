SETTINGS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Settings & Pricing</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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
    .content-area { padding: 2rem; max-width: 800px; }
    .card-box { background: #121214; border: 1px solid #27272a; border-radius: 8px; margin-bottom: 2rem; overflow: hidden; }
    .card-header { padding: 1rem 1.25rem; border-bottom: 1px solid #27272a; font-weight: 600; font-size: 0.95rem; }
    .card-body { padding: 1.5rem; }
    .form-group { margin-bottom: 1.5rem; }
    label { display: block; font-size: 0.85rem; font-weight: 500; color: #a1a1aa; margin-bottom: 0.5rem; }
    .help-text { font-size: 0.75rem; color: #71717a; margin-top: 0.35rem; }
    input { width: 100%; background: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 0.75rem 1rem; color: #fafafa; font-size: 0.95rem; outline: none; }
    input:focus { border-color: #10b981; }
    .btn-save { background: #10b981; color: #09090b; border: none; border-radius: 6px; padding: 0.75rem 1.5rem; font-size: 0.95rem; font-weight: 600; cursor: pointer; }
    .btn-save:hover { background: #059669; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header"><div class="logo-box">G</div><div class="logo-text">GoldenEra 5G</div></div>
    <ul class="nav-list">
      <li class="nav-item"><a href="/admin/dashboard" class="nav-link">📊 Dashboard</a></li>
      <li class="nav-item"><a href="/admin/users" class="nav-link">👥 Users & Wallets</a></li>
      <li class="nav-item"><a href="/admin/deposits" class="nav-link">💳 Deposits</a></li>
      <li class="nav-item"><a href="/admin/proxies" class="nav-link">🔌 Active Proxies</a></li>
      <li class="nav-item"><a href="/admin/settings" class="nav-link active">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.4.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">System Settings & Pricing</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="card-box">
        <div class="card-header">Margin & Exchange Rates</div>
        <div class="card-body">
          <form id="settings-form" onsubmit="saveSettings(event)">
            <div class="form-group">
              <label for="markup">Profit Markup Percentage (%)</label>
              <input type="number" step="0.1" id="markup" required>
              <div class="help-text">Percentage added automatically over Magnum base cost. Example: 30 = +30% profit.</div>
            </div>

            <div class="form-group">
              <label for="rate">USD to EGP Exchange Rate</label>
              <input type="number" step="0.01" id="rate" required>
              <div class="help-text">Used to convert Vodafone Cash EGP deposits into USD wallet balance (1$ = X EGP).</div>
            </div>

            <div class="form-group">
              <label for="vf-number">Vodafone Cash Receiving Number</label>
              <input type="text" id="vf-number" required>
              <div class="help-text">The phone number displayed to customers in the bot when they select Vodafone Cash deposit.</div>
            </div>

            <button type="submit" class="btn-save">Save Settings</button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <script>
    async function loadSettings() {
      try {
        const res = await fetch('/admin/api/settings');
        const d = await res.json();
        document.getElementById('markup').value = d.markup_percent || 30;
        document.getElementById('rate').value = d.usd_to_egp_rate || 52;
        document.getElementById('vf-number').value = d.vodafone_cash_number || '';
      } catch(e) {
        console.error(e);
      }
    }

    async function saveSettings(e) {
      e.preventDefault();
      const payload = {
        markup_percent: parseFloat(document.getElementById('markup').value),
        usd_to_egp_rate: parseFloat(document.getElementById('rate').value),
        vodafone_cash_number: document.getElementById('vf-number').value.trim()
      };
      try {
        const res = await fetch('/admin/api/settings', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          alert('Settings saved successfully!');
        } else {
          alert('Failed to save settings.');
        }
      } catch(err) {
        alert(err);
      }
    }

    loadSettings();
  </script>
</body>
</html>"""
