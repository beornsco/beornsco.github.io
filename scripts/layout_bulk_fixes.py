#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path('/home/beorndlatch/.openclaw/workspace/site')
FOOTER = '''<footer>
  <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px 16px;color:#9ca3af;font-size:.875rem">
    <span>© 2026 Beorns Co</span>
    <a href="mailto:beornsco@proton.me" style="color:#9ca3af">beornsco@proton.me</a>
    <a href="/terms/" style="color:#9ca3af">Terms</a>
    <a href="/privacy/" style="color:#9ca3af">Privacy</a>
    <a href="/about/" style="color:#9ca3af">About</a>
    <a href="https://twitter.com/beornsco" target="_blank" rel="noopener" style="color:#9ca3af">X/Twitter</a>
    <a href="https://medium.com/@beornsco" target="_blank" rel="noopener" style="color:#9ca3af">Medium</a>
    <a href="https://beornsco.lemonsqueezy.com" target="_blank" rel="noopener" style="color:#9ca3af">Lemon Squeezy</a>
  </div>
</footer>'''

NAV_LABEL = '.nav-dd-label{padding:8px 16px 3px;font-size:.68rem;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em}'
NAV_SEP = '.nav-dd-sep{border:none;border-top:1px solid #f3f4f6;margin:6px 8px}'
CODE_BLOCK = 'pre, code { white-space: pre-wrap; word-break: break-word; overflow-x: auto; }\npre { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; font-size: .88rem; }'
READABILITY = '.post-content, article { max-width: 780px; margin: 0 auto; padding: 0 24px; }'

changed=[]

for f in ROOT.rglob('*.html'):
    old = f.read_text()
    new = old

    # Fix 6 footer on all pages
    if '<footer' in new:
        new = re.sub(r'<footer[\s\S]*?</footer>', FOOTER, new, count=1)

    # Fix 4 nav dropdown label/separator css on all pages
    new = re.sub(r'\.nav-dd-label\{[^}]*\}', NAV_LABEL, new)
    new = re.sub(r'\.nav-dd-sep\{[^}]*\}', NAV_SEP, new)

    # Fix 7 and 8 on blog article pages
    if f.parent.name == 'blog' and f.name != 'index.html':
        if CODE_BLOCK not in new:
            new = re.sub(r'@media\(prefers-reduced-motion:no-preference\)\{', CODE_BLOCK + '\n' + READABILITY + '\n@media(prefers-reduced-motion:no-preference){', new, count=1)
        elif READABILITY not in new:
            new = new.replace(CODE_BLOCK, CODE_BLOCK + '\n' + READABILITY)

    # Fix 8 on pSEO pages
    if f.parent.name.startswith('ai-prompts-for-'):
        if READABILITY not in new:
            new = re.sub(r'@media\(prefers-reduced-motion:no-preference\)\{', READABILITY + '\n@media(prefers-reduced-motion:no-preference){', new, count=1)

    if new != old:
        if len(new.encode()) < 0.9 * len(old.encode()):
            raise SystemExit(f'Safety stop: {f} dropped below 90 percent size')
        if '—' in new or '–' in new:
            raise SystemExit(f'Dash stop: {f} contains em/en dash')
        f.write_text(new)
        if f.stat().st_size < int(0.9 * len(old.encode())):
            raise SystemExit(f'Safety stop after write: {f}')
        changed.append(str(f.relative_to(ROOT)))

print('\n'.join(changed))
print(f'Total changed: {len(changed)}')
