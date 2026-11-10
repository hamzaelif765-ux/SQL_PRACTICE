"""Builds dist/index.html AND root index.html (for GitHub Pages). Usage: python3 build.py"""
import json, glob, os, sys
T = next((f for f in ('index.template.html', 'index_template.html') if os.path.exists(f)), None)
if not T: sys.exit('template not found (index.template.html)')
L = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob('lessons/m[0-9]*.json'))]
D = {os.path.basename(f)[:-4]: open(f, encoding='utf-8').read() for f in glob.glob('data/sqlite/*.sql')}
for l in L:
    for ds in {l['dataset']} | {e['dataset'] for e in l['exercises'] if 'dataset' in e}:
        if ds not in D: sys.exit('lesson %s needs data/sqlite/%s.sql -> run: python3 gen_data.py sqlite' % (l['id'], ds))
h = open(T, encoding='utf-8').read()
h = h.replace('/*@LESSONS@*/[]', json.dumps(L, ensure_ascii=False).replace('</', '<\\/')).replace('/*@DATASETS@*/{}', json.dumps(D).replace('</', '<\\/'))
os.makedirs('dist', exist_ok=True)
for p in ('dist/index.html', 'index.html'): open(p, 'w', encoding='utf-8').write(h)
print('built index.html + dist/index.html', len(h), 'bytes,', len(L), 'lessons')
