import sys, re
batch, labels = sys.argv[1], sys.argv[2]
ids = [l.split(' | ')[0] for l in open(batch) if re.match(r'^\d{3}-\d{3} \| ', l)]
seen, errs = {}, []
for n, l in enumerate(open(labels), 1):
    l = l.rstrip('\n')
    if not l.strip(): continue
    p = l.split('\t')
    if len(p) < 4: errs.append(f'line {n}: <4 fields: {l[:80]}'); continue
    iid, c, nv, t = p[:4]
    note = p[4] if len(p) > 4 else ''
    if c not in ('0', '1') or nv not in ('0', '1'): errs.append(f'line {n}: bad label {l[:80]}')
    if t not in ('FMT', 'VAL', 'FACT', 'OPEN', 'QUAL', 'ORD'): errs.append(f'line {n}: bad type {t}')
    if nv == '1' and not note.strip(): errs.append(f'line {n}: narrative=1 needs note')
    if iid in seen: errs.append(f'line {n}: duplicate {iid}')
    seen[iid] = 1
missing = [i for i in ids if i not in seen]
extra = [i for i in seen if i not in set(ids)]
print(f'expected {len(ids)} labeled {len(seen)} missing {len(missing)} extra {len(extra)} errors {len(errs)}')
for e in errs[:30]: print(' ', e)
if missing: print('  missing:', ' '.join(missing[:60]))
if extra: print('  extra:', ' '.join(extra[:30]))
sys.exit(1 if (errs or missing or extra) else 0)
