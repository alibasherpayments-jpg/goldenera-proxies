import base64

svg_text = open('static/logo.svg', 'r', encoding='utf-8').read()
png_b64 = base64.b64encode(open('static/logo_web.png', 'rb').read()).decode('ascii')
ico_b64 = base64.b64encode(open('static/favicon.ico', 'rb').read()).decode('ascii')

with open('app/dashboard/static/assets.py', 'w', encoding='utf-8') as f:
    f.write('"""\nEmbedded static assets for GoldenEra 5G dashboard branding.\nGuarantees assets are bundled into serverless python functions.\n"""\nimport base64\n\n')
    f.write(f'LOGO_SVG = """{svg_text}"""\n\n')
    f.write(f'LOGO_PNG_B64 = "{png_b64}"\n\n')
    f.write(f'FAVICON_ICO_B64 = "{ico_b64}"\n\n')
    f.write('def get_png_bytes() -> bytes:\n    return base64.b64decode(LOGO_PNG_B64)\n\n')
    f.write('def get_ico_bytes() -> bytes:\n    return base64.b64decode(FAVICON_ICO_B64)\n\n')
    f.write('def get_svg_bytes() -> bytes:\n    return LOGO_SVG.encode("utf-8")\n')

print('app/dashboard/static/assets.py successfully generated!')
