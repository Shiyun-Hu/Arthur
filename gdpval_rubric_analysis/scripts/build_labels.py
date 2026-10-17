"""Merge annotation passes into final per-item labels and summary tables.

Usage: python3 scripts/build_labels.py <gdpval train parquet> <analysis dir>
"""
import glob
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adjudication import NARRATIVE, OVERRIDES  # noqa: E402


def read_tsv(pattern, names):
    rows = []
    for f in sorted(glob.glob(pattern)):
        for line in open(f, encoding='utf-8'):
            line = line.rstrip('\n')
            if not line.strip():
                continue
            p = line.split('\t')
            p += [''] * (len(names) - len(p))
            rows.append(dict(zip(names, p[:len(names)])))
    return pd.DataFrame(rows)


def kappa(a, b):
    a, b = pd.Series(a).reset_index(drop=True), pd.Series(b).reset_index(drop=True)
    cats = sorted(set(a) | set(b))
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in cats)
    return (po - pe) / (1 - pe)


def main(parquet, root):
    src = pd.read_parquet(parquet)
    items = []
    for ti, r in enumerate(src.itertuples()):
        for ii, it in enumerate(json.loads(r.rubric_json)):
            items.append(dict(item_id=f'{ti:03d}-{ii:03d}', task_idx=ti, task_id=r.task_id,
                              rubric_item_id=it['rubric_item_id'], sector=r.sector,
                              occupation=r.occupation, score=it['score'],
                              criterion=it['criterion'].strip()))
    df = pd.DataFrame(items)

    p1 = read_tsv(os.path.join(root, 'labels/pass1/*.tsv'),
                  ['item_id', 'p1_is_closed', 'p1_is_narrative', 'p1_check_type', 'p1_note'])
    p2 = read_tsv(os.path.join(root, 'labels/pass2/*.tsv'),
                  ['item_id', 'p2_closed_level', 'p2_is_narrative', 'p2_check_type', 'p2_note'])
    for c in ['p1_is_closed', 'p1_is_narrative']:
        p1[c] = p1[c].astype(int)
    for c in ['p2_closed_level', 'p2_is_narrative']:
        p2[c] = p2[c].astype(int)
    df = df.merge(p1, on='item_id', how='left').merge(p2, on='item_id', how='left')
    assert df.p1_is_closed.notna().all() and df.p2_closed_level.notna().all()

    # Final labels
    df['closed_level'] = df.p2_closed_level
    df['is_closed'] = (df.closed_level == 2).astype(int)
    df['is_narrative'] = df.item_id.map(lambda i: int(i in NARRATIVE))
    df['narrative_type'] = df.item_id.map(NARRATIVE).fillna('')
    df['check_type'] = df.p2_check_type
    df['adjudication_note'] = df.item_id.map(lambda i: OVERRIDES.get(i, (None, ''))[1])
    for i, (lab, _) in OVERRIDES.items():
        assert int(i in NARRATIVE) == lab, i
    df['points'] = df.score.clip(lower=0)

    data = os.path.join(root, 'data')
    cols = ['item_id', 'task_id', 'rubric_item_id', 'sector', 'occupation', 'score', 'criterion',
            'is_closed', 'closed_level', 'is_narrative', 'narrative_type', 'check_type',
            'p1_is_closed', 'p1_is_narrative', 'p1_check_type', 'p1_note',
            'p2_closed_level', 'p2_is_narrative', 'p2_check_type', 'p2_note', 'adjudication_note']
    df[cols].to_csv(os.path.join(data, 'gdpval_rubric_labels.csv'), index=False)
    nar = df[df.is_narrative == 1].sort_values(['narrative_type', 'item_id'])
    nar[['item_id', 'narrative_type', 'is_closed', 'closed_level', 'sector', 'occupation', 'score',
         'criterion', 'adjudication_note']].to_csv(os.path.join(data, 'narrative_items.csv'), index=False)

    def summarize(g):
        pos = g[g.score > 0]
        return pd.Series({
            'tasks': g.task_idx.nunique(),
            'items': len(g),
            'closed_items': int(g.is_closed.sum()),
            'closed_pct': round(100 * g.is_closed.mean(), 1),
            'closed_points_pct': round(100 * pos.loc[pos.is_closed == 1, 'score'].sum() / pos.score.sum(), 1),
            'level1_pct': round(100 * (g.closed_level == 1).mean(), 1),
            'level0_pct': round(100 * (g.closed_level == 0).mean(), 1),
            'narrative_items': int(g.is_narrative.sum()),
            'narrative_pct': round(100 * g.is_narrative.mean(), 2),
            'tasks_with_narrative': g[g.is_narrative == 1].task_idx.nunique(),
        })

    by_sector = df.groupby('sector').apply(summarize).sort_values('closed_pct')
    by_occ = df.groupby(['sector', 'occupation']).apply(summarize).sort_values('closed_pct')
    by_task = df.groupby(['task_id', 'sector', 'occupation']).apply(summarize).sort_values('closed_pct')
    by_sector.to_csv(os.path.join(data, 'summary_by_sector.csv'))
    by_occ.to_csv(os.path.join(data, 'summary_by_occupation.csv'))
    by_task.to_csv(os.path.join(data, 'summary_by_task.csv'))

    # ---- report numbers ----
    N = len(df)
    pos = df[df.score > 0]
    out = []
    out.append(f'items={N} tasks={df.task_id.nunique()} positive_items={len(pos)} negative_items={(df.score < 0).sum()}')
    for lv in [2, 1, 0]:
        n = (df.closed_level == lv).sum()
        pts = pos.loc[pos.closed_level == lv, 'score'].sum() / pos.score.sum()
        out.append(f'closed_level={lv}: {n} ({100*n/N:.1f}%), positive-point share {100*pts:.1f}%')
    out.append('check_type x closed_level:\n' + pd.crosstab(df.check_type, df.closed_level, margins=True).to_string())
    out.append(f'is_narrative=1: {df.is_narrative.sum()} ({100*df.is_narrative.mean():.2f}%), '
               f'tasks with >=1: {df[df.is_narrative==1].task_id.nunique()} / {df.task_id.nunique()}, '
               f'positive-point share {100*pos.loc[pos.is_narrative==1,"score"].sum()/pos.score.sum():.2f}%')
    out.append('narrative_type counts: ' + df[df.is_narrative == 1].narrative_type.value_counts().to_dict().__repr__())
    out.append('is_closed x is_narrative:\n' + pd.crosstab(df.is_closed, df.is_narrative, margins=True).to_string())
    out.append('narrative x closed_level:\n' + pd.crosstab(df[df.is_narrative == 1].narrative_type, df[df.is_narrative == 1].closed_level).to_string())
    tc = df.groupby('task_id').is_closed.mean()
    out.append(f'per-task closed share: median {100*tc.median():.1f}%, min {100*tc.min():.1f}%, max {100*tc.max():.1f}%, '
               f'tasks >=90%: {(tc>=0.9).sum()}, tasks <50%: {(tc<0.5).sum()}')

    # ---- agreement ----
    out.append('--- agreement ---')
    out.append(f'pass1 vs pass2 is_narrative: agree {100*(df.p1_is_narrative==df.p2_is_narrative).mean():.2f}%, '
               f'kappa {kappa(df.p1_is_narrative, df.p2_is_narrative):.3f}; both=1 {((df.p1_is_narrative==1)&(df.p2_is_narrative==1)).sum()}, '
               f'p1 only {((df.p1_is_narrative==1)&(df.p2_is_narrative==0)).sum()}, p2 only {((df.p1_is_narrative==0)&(df.p2_is_narrative==1)).sum()}')
    ge1 = (df.p2_closed_level >= 1).astype(int)
    out.append(f'pass1 is_closed(v1, lenient) vs pass2 level>=1: agree {100*(df.p1_is_closed==ge1).mean():.2f}%, kappa {kappa(df.p1_is_closed, ge1):.3f}')
    p3 = read_tsv(os.path.join(root, 'labels/pass3_reliability/*.tsv'),
                  ['item_id', 'p3_closed_level', 'p3_is_narrative', 'p3_check_type', 'p3_note'])
    if len(p3):
        p3['p3_closed_level'] = p3.p3_closed_level.astype(int)
        p3['p3_is_narrative'] = p3.p3_is_narrative.astype(int)
        m = p3.merge(df, on='item_id')
        out.append(f'pass3 reliability sample n={len(m)}')
        out.append(f'  closed_level exact agree {100*(m.p3_closed_level==m.closed_level).mean():.1f}%, kappa {kappa(m.p3_closed_level, m.closed_level):.3f}')
        a, b = (m.p3_closed_level == 2).astype(int), m.is_closed
        out.append(f'  is_closed (level 2) agree {100*(a==b).mean():.1f}%, kappa {kappa(a, b):.3f}; pass2 rate {100*b.mean():.1f}% vs pass3 rate {100*a.mean():.1f}%')
        a, b = (m.p3_closed_level >= 1).astype(int), (m.closed_level >= 1).astype(int)
        out.append(f'  level>=1 agree {100*(a==b).mean():.1f}%, kappa {kappa(a, b):.3f}')
        out.append('  confusion (rows=pass2/final, cols=pass3):\n' + pd.crosstab(m.closed_level, m.p3_closed_level).to_string())
        out.append(f'  is_narrative final vs pass3: agree {100*(m.p3_is_narrative==m.is_narrative).mean():.1f}%, '
                   f'final=1 {m.is_narrative.sum()}, pass3=1 {m.p3_is_narrative.sum()}, both {((m.is_narrative==1)&(m.p3_is_narrative==1)).sum()}')
    report = '\n'.join(out)
    open(os.path.join(data, 'stats.txt'), 'w').write(report + '\n')
    print(report)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
