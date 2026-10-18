BROADCAST_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Broadcaster</title>
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
    textarea { width: 100%; height: 160px; background: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 0.75rem 1rem; color: #fafafa; font-size: 0.95rem; outline: none; font-family: inherit; resize: vertical; }
    textarea:focus { border-color: #10b981; }
    .btn-send { background: #10b981; color: #09090b; border: none; border-radius: 6px; padding: 0.75rem 1.5rem; font-size: 0.95rem; font-weight: 600; cursor: pointer; }
    .btn-send:hover { background: #059669; }
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
      <li class="nav-item"><a href="/admin/settings" class="nav-link">⚙️ Settings & Pricing</a></li>
      <li class="nav-item"><a href="/admin/broadcast" class="nav-link active">📢 Broadcaster</a></li>
    </ul>
    <div class="sidebar-footer"><span>v1.4.0</span><a href="/admin/logout" class="logout-btn">Logout ↗</a></div>
  </div>

  <div class="main-wrap">
    <div class="top-bar">
      <div class="top-title">Bulk Broadcaster</div>
      <div class="admin-pill">Admin: <span>{{ADMIN_USER}}</span></div>
    </div>

    <div class="content-area">
      <div class="card-box">
        <div class="card-header">Broadcast Message to All Telegram Users</div>
        <div class="card-body">
          <form id="broadcast-form" onsubmit="sendBroadcast(event)">
            <div class="form-group">
              <label for="broadcast-msg">Broadcast Text (Markdown Supported)</label>
              <textarea id="broadcast-msg" placeholder="Write your announcement, new offers, or server updates here..." required></textarea>
              <div class="help-text">This message will be dispatched asynchronously to all registered Telegram bot users.</div>
            </div>

            <button type="submit" class="btn-send" id="btn-submit">Dispatch Broadcast 🚀</button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <script>
    async function sendBroadcast(e) {
      e.preventDefault();
      const msg = document.getElementById('broadcast-msg').value.trim();
      if (!msg) return;

      if (!confirm('Are you sure you want to broadcast this message to ALL bot users?')) return;

      const btn = document.getElementById('btn-submit');
      btn.disabled = true;
      btn.textContent = 'Sending... ⏳';

      try {
        const res = await fetch('/admin/api/broadcast', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        const d = await res.json();
        if (res.ok) {
          alert(`Broadcast completed!\nDelivered: ${d.delivered || 0}\nFailed: ${d.failed || 0}`);
          document.getElementById('broadcast-msg').value = '';
        } else {
          alert('Failed to send broadcast');
        }
      } catch(err) {
        alert(err);
      } finally {
        btn.disabled = false;
        btn.textContent = 'Dispatch Broadcast 🚀';
      }
    }
  </script>
</body>
</html>"""
