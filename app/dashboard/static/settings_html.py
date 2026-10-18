SETTINGS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — System Settings</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
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
    .content-area { padding: 2rem; max-width: 820px; }
    
    .card-box { background: #121214; border: 1px solid #27272a; border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; }
    .card-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid #27272a; font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; justify-content: space-between; }
    .card-body { padding: 1.5rem; }
    .form-group { margin-bottom: 1.5rem; }
    label { display: block; font-size: 0.85rem; font-weight: 600; color: #e4e4e7; margin-bottom: 0.4rem; }
    .help-text { font-size: 0.75rem; color: #71717a; margin-top: 0.4rem; }
    input { width: 100%; background: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 0.75rem 1rem; color: #fafafa; font-size: 0.95rem; outline: none; font-family: 'JetBrains Mono', monospace; transition: border-color 0.15s; }
    input:focus { border-color: #10b981; }
    .btn-save { background: #10b981; color: #09090b; border: none; border-radius: 6px; padding: 0.75rem 1.75rem; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
    .btn-save:hover { background: #059669; }
    
    .toast { display: none; position: fixed; bottom: 2rem; right: 2rem; background: #10b981; color: #09090b; font-weight: 600; padding: 0.75rem 1.25rem; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 100; animation: fadeIn 0.2s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
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
        <div class="card-header">
          <div>Margins & FX Rates</div>
          <span style="font-size: 0.75rem; color: #10b981; font-weight: 600;">Active in Real-Time</span>
        </div>
        <div class="card-body">
          <form id="settings-form" onsubmit="saveSettings(event)">
            <div class="form-group">
              <label for="markup">Profit Markup Percentage (%)</label>
              <input type="number" step="0.1" id="markup" required>
              <div class="help-text">Applied automatically over Magnum base cost (e.g., 30 adds a +30% profit margin to customer prices).</div>
            </div>

            <div class="form-group">
              <label for="rate">USD to EGP Exchange Rate</label>
              <input type="number" step="0.01" id="rate" required>
              <div class="help-text">Rate applied to Vodafone Cash deposits when crediting USD wallet balance ($1.00 USD = X EGP).</div>
            </div>

            <div class="form-group">
              <label for="vf-number">Vodafone Cash Receiving Wallet Phone Number</label>
              <input type="text" id="vf-number" required>
              <div class="help-text">The official receiving mobile wallet number presented to customers in the Telegram bot deposit wizard.</div>
            </div>

            <div style="border-top: 1px solid #27272a; margin: 1.75rem 0; padding-top: 1.5rem;">
              <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: #f59e0b;">🟡 Binance Pay & Auto-Verification Settings</div>
              <div style="font-size: 0.78rem; color: #71717a; margin-bottom: 1.25rem;">Configure your Binance ID for customer transfers and optional API keys for 100% automatic real-time verification.</div>
              
              <div class="form-group">
                <label for="binance-id">Official Binance ID / Pay ID</label>
                <input type="text" id="binance-id" required placeholder="538860756">
                <div class="help-text">Presented directly to customers in the bot when they choose Binance Pay deposit.</div>
              </div>

              <div class="form-group">
                <label for="binance-api-key">Binance API Key (For 100% Instant Auto-Credit)</label>
                <input type="text" id="binance-api-key" placeholder="Paste your Binance API Key (Read-Only)">
                <div class="help-text">Allows the bot to query incoming Binance Pay transactions in real-time and credit user balances instantly without manual approval.</div>
              </div>

              <div class="form-group">
                <label for="binance-secret-key">Binance Secret Key</label>
                <input type="password" id="binance-secret-key" placeholder="Paste your Binance Secret Key">
                <div class="help-text">Used to sign requests to Binance API securely. Leave blank if not changing.</div>
              </div>
            </div>

            <button type="submit" class="btn-save" id="btn-save">Save Settings 💾</button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div id="toast" class="toast">✅ Settings saved and applied successfully!</div>

  <script>
    async function loadSettings() {
      try {
        const res = await fetch('/admin/api/settings');
        const d = await res.json();
        document.getElementById('markup').value = d.markup_percent || 30;
        document.getElementById('rate').value = d.usd_to_egp_rate || 52;
        document.getElementById('vf-number').value = d.vodafone_cash_number || '';
        document.getElementById('binance-id').value = d.binance_id || '538860756';
        document.getElementById('binance-api-key').value = d.binance_api_key || '';
        if (d.has_binance_secret) {
          document.getElementById('binance-secret-key').placeholder = '•••••••••••••••• (Secret Key is saved)';
        }
      } catch(e) {
        console.error(e);
      }
    }

    async function saveSettings(e) {
      e.preventDefault();
      const btn = document.getElementById('btn-save');
      btn.disabled = true;
      btn.innerText = 'Saving... ⏳';

      const payload = {
        markup_percent: parseFloat(document.getElementById('markup').value),
        usd_to_egp_rate: parseFloat(document.getElementById('rate').value),
        vodafone_cash_number: document.getElementById('vf-number').value.trim(),
        binance_id: document.getElementById('binance-id').value.trim(),
        binance_api_key: document.getElementById('binance-api-key').value.trim(),
        binance_secret_key: document.getElementById('binance-secret-key').value.trim() || undefined
      };
      try {
        const res = await fetch('/admin/api/settings', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          showToast('✅ Settings updated and synchronized!');
        } else {
          alert('Failed to save settings.');
        }
      } catch(err) {
        alert(err);
      } finally {
        btn.disabled = false;
        btn.innerText = 'Save Settings 💾';
      }
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.style.display = 'block';
      setTimeout(() => { toast.style.display = 'none'; }, 3500);
    }

    loadSettings();
  </script>
</body>
</html>"""
