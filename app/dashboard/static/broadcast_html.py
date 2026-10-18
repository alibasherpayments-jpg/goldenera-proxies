BROADCAST_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Broadcaster</title>
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
    .content-area { padding: 2rem; max-width: 900px; }

    .card-box { background: #121214; border: 1px solid #27272a; border-radius: 8px; margin-bottom: 2rem; overflow: hidden; }
    .card-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid #27272a; font-weight: 600; font-size: 0.95rem; display: flex; justify-content: space-between; align-items: center; }
    .card-body { padding: 1.5rem; }
    .form-group { margin-bottom: 1.25rem; }
    label { display: block; font-size: 0.85rem; font-weight: 600; color: #e4e4e7; margin-bottom: 0.5rem; }
    .toolbar-tools { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; }
    .tool-btn { background: #18181b; border: 1px solid #27272a; color: #a1a1aa; padding: 4px 10px; border-radius: 4px; font-size: 0.78rem; cursor: pointer; transition: all 0.15s; }
    .tool-btn:hover { color: #fafafa; border-color: #3f3f46; }
    textarea { width: 100%; height: 180px; background: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 0.85rem 1rem; color: #fafafa; font-size: 0.95rem; outline: none; font-family: 'JetBrains Mono', monospace; resize: vertical; line-height: 1.5; }
    textarea:focus { border-color: #10b981; }
    .meta-bar { display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: #71717a; margin-top: 0.5rem; }
    .btn-send { background: #10b981; color: #09090b; border: none; border-radius: 6px; padding: 0.75rem 1.75rem; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
    .btn-send:hover { background: #059669; }
    .btn-send:disabled { opacity: 0.5; cursor: not-allowed; }
    .preview-card { background: #18181b; border: 1px dashed #27272a; border-radius: 6px; padding: 1.25rem; margin-top: 1.5rem; }
    .preview-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #71717a; margin-bottom: 0.75rem; letter-spacing: 0.05em; }
    .preview-content { font-size: 0.9rem; line-height: 1.6; white-space: pre-wrap; color: #e4e4e7; }
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
      <li class="nav-item"><a href="/admin/redeem" class="nav-link">🎁 Redeem Codes</a></li>
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
        <div class="card-header">
          <div>Telegram Broadcast Dispatcher</div>
          <span style="font-size: 0.75rem; color: #38bdf8;">HTML / Markdown Supported</span>
        </div>
        <div class="card-body">
          <form id="broadcast-form" onsubmit="sendBroadcast(event)">
            <div class="form-group">
              <label for="broadcast-msg">Broadcast Message</label>
              <div class="toolbar-tools">
                <button type="button" class="tool-btn" onclick="wrapText('<b>', '</b>')"><b>B</b> Bold</button>
                <button type="button" class="tool-btn" onclick="wrapText('<i>', '</i>')"><i>I</i> Italic</button>
                <button type="button" class="tool-btn" onclick="wrapText('<code>', '</code>')"><code>&lt;&gt;</code> Code</button>
                <button type="button" class="tool-btn" onclick="wrapText('<a href=\\'https://...\\'>', '</a>')">🔗 Link</button>
              </div>
              <textarea id="broadcast-msg" placeholder="Type your announcement, promo codes, or service updates here..." required oninput="updatePreview()"></textarea>
              <div class="meta-bar">
                <span id="char-count">0 characters | 0 words</span>
                <span>Dispatches asynchronously to all bot subscribers</span>
              </div>
            </div>

            <div class="preview-card">
              <div class="preview-title">👁️ Telegram Message Live Preview</div>
              <div id="preview-box" class="preview-content">Type a message above to see preview...</div>
            </div>

            <div style="margin-top: 1.5rem;">
              <button type="submit" class="btn-send" id="btn-submit">Dispatch Broadcast 🚀</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <script>
    function updatePreview() {
      const val = document.getElementById('broadcast-msg').value;
      const box = document.getElementById('preview-box');
      const counter = document.getElementById('char-count');
      
      const words = val.trim() ? val.trim().split(/\\s+/).length : 0;
      counter.innerText = `${val.length} characters | ${words} words`;

      if (!val.trim()) {
        box.innerText = 'Type a message above to see preview...';
      } else {
        box.innerHTML = val;
      }
    }

    function wrapText(open, close) {
      const area = document.getElementById('broadcast-msg');
      const start = area.selectionStart;
      const end = area.selectionEnd;
      const sel = area.value.substring(start, end) || 'text';
      area.value = area.value.substring(0, start) + open + sel + close + area.value.substring(end);
      updatePreview();
      area.focus();
    }

    async function sendBroadcast(e) {
      e.preventDefault();
      const msg = document.getElementById('broadcast-msg').value.trim();
      if (!msg) return;

      if (!confirm('Are you sure you want to broadcast this message to ALL bot users?')) return;

      const btn = document.getElementById('btn-submit');
      btn.disabled = true;
      btn.textContent = 'Broadcasting... ⏳';

      try {
        const res = await fetch('/admin/api/broadcast', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        const d = await res.json();
        if (res.ok) {
          alert(`Broadcast completed!\\n\\n✅ Delivered: ${d.delivered || 0}\\n❌ Failed/Blocked: ${d.failed || 0}`);
          document.getElementById('broadcast-msg').value = '';
          updatePreview();
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
