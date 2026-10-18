LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GoldenEra Admin — Sign In</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: #09090b;
      color: #fafafa;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      background-image: radial-gradient(circle at 50% 20%, rgba(16, 185, 129, 0.05), transparent 40%);
    }
    .login-card {
      width: 100%;
      max-width: 380px;
      background: #111114;
      border: 1px solid #27272a;
      border-radius: 12px;
      padding: 2.25rem 2rem;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 0.85rem;
      margin-bottom: 2rem;
    }
    .brand-logo {
      width: 38px;
      height: 38px;
      background: #18181b;
      border: 1px solid #3f3f46;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      color: #10b981;
      font-size: 1.15rem;
    }
    .brand-title {
      font-size: 1.1rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .brand-sub {
      font-size: 0.72rem;
      color: #71717a;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }
    .form-group {
      margin-bottom: 1.25rem;
    }
    label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      color: #a1a1aa;
      margin-bottom: 0.4rem;
    }
    input {
      width: 100%;
      background: #18181b;
      border: 1px solid #27272a;
      border-radius: 6px;
      padding: 0.75rem 1rem;
      color: #fafafa;
      font-size: 0.95rem;
      outline: none;
      transition: all 0.15s ease;
    }
    input:focus {
      border-color: #10b981;
      box-shadow: 0 0 0 1px #10b981;
    }
    .btn-submit {
      width: 100%;
      background: #10b981;
      color: #09090b;
      border: none;
      border-radius: 6px;
      padding: 0.75rem;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      margin-top: 0.5rem;
      transition: background 0.15s ease;
    }
    .btn-submit:hover {
      background: #059669;
    }
    .error-msg {
      background: rgba(239, 68, 68, 0.15);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.3);
      border-radius: 6px;
      padding: 0.75rem;
      font-size: 0.82rem;
      margin-bottom: 1.25rem;
      text-align: center;
    }
    .card-footer {
      margin-top: 1.75rem;
      text-align: center;
      font-size: 0.75rem;
      color: #52525b;
    }
  </style>
</head>
<body>
  <div class="login-card">
    <div class="brand">
      <div class="brand-logo">G</div>
      <div>
        <div class="brand-title">GoldenEra Proxies</div>
        <div class="brand-sub">Admin Operations Center</div>
      </div>
    </div>

    <!--ERROR_SLOT-->

    <form method="POST" action="/admin/login">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required autocomplete="username" autofocus placeholder="admin">
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required autocomplete="current-password" placeholder="••••••••">
      </div>
      <button type="submit" class="btn-submit">Sign In to Dashboard →</button>
    </form>

    <div class="card-footer">
      Protected Enterprise Dashboard • GoldenEra 5G
    </div>
  </div>
</body>
</html>"""
