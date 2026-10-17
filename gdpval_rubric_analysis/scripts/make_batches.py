import pandas as pd, json, sys, os
src, outdir, nb = sys.argv[1], sys.argv[2], int(sys.argv[3])
df = pd.read_parquet(src)
items = []
tasks = []
for ti, r in enumerate(df.itertuples()):
    its = json.loads(r.rubric_json)
    tasks.append((ti, r, its))
    for ii, it in enumerate(its):
        items.append(dict(item_id=f"{ti:03d}-{ii:03d}", task_idx=ti, task_id=r.task_id, sector=r.sector,
                          occupation=r.occupation, score=it['score'], criterion=it['criterion'],
                          rubric_item_id=it['rubric_item_id'], tags=it.get('tags')))
pd.DataFrame(items).to_json(os.path.join(outdir, '..', 'items.jsonl'), orient='records', lines=True, force_ascii=False)
total = len(items); target = total / nb
b, cnt, cur = 0, 0, []
batches = []
for t in tasks:
    cur.append(t); cnt += len(t[2])
    if cnt >= target * (len(batches) + 1) and len(batches) < nb - 1:
        batches.append(cur); cur = []
if cur: batches.append(cur)
for bi, bt in enumerate(batches):
    lines = []
    n = 0
    for ti, r, its in bt:
        p = r.prompt if len(r.prompt) <= 1800 else r.prompt[:1800] + ' …[truncated]'
        lines.append(f"\n#################### TASK {ti:03d} | {r.occupation} ({r.sector})")
        lines.append("PROMPT (context only):\n" + p.strip())
        lines.append("RUBRIC ITEMS (item_id | score | criterion):")
        for ii, it in enumerate(its):
            c = it['criterion'].replace('\n', ' ').strip()
            lines.append(f"{ti:03d}-{ii:03d} | {it['score']:+d} | {c}"); n += 1
    with open(os.path.join(outdir, f"batch_{bi:02d}.txt"), 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(bi, f"tasks {bt[0][0]:03d}-{bt[-1][0]:03d}", n, 'items')
