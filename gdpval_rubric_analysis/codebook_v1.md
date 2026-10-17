# GDPval rubric-item labeling codebook

Each GDPval task has a rubric: a list of criteria a grader checks against the deliverable
(Excel/Word/PDF/PPT/audio/video etc.). You label EACH rubric item (criterion) with two binary
labels plus one auxiliary category. Judge the criterion text itself (use the task prompt only as
context for what the deliverable is). Negative-score items (penalties, e.g. "-10 Includes X")
are labeled by what they check, exactly like positive ones.

## Label 1 — is_closed  (1 = 明确要求取得一个可程序化核验的确定结果)

is_closed = 1 when the criterion demands a DETERMINATE result — there is an answer key — AND
pass/fail could be decided MECHANICALLY by a program (file parsing, string / keyword / regex match
with a small synonym list, numeric comparison with tolerance, counting, schema / structure checks,
date arithmetic, signal measurement), with no judgment of quality, adequacy or appropriateness.
Two competent graders would never disagree.

Typical is_closed = 1:
- File / format / structure specs: "deliverable is an .xlsx named 'Sample'", "worksheet named
  exactly X", "contains a section/heading labeled 'Surveillance'", "has 10–12 slides",
  "under 500 words", "footer on every slide with slide number", "column K contains 1 for
  sampled rows", "is a PDF".
- Exact values / calculations / derived numbers: "sample size is 59", "credit balance of
  45,123.29", "z = 1.645", "N equals number of rows in the reference", "variance = (Q3-Q2)/Q2",
  "integrated loudness between -17 and -15 LUFS", "total rounds to $1.2M".
- Specific named fact / entity / term / categorical answer that must appear or must be chosen:
  "lists the medication as Vraylar", "identifies the vendor as Acme", "recommends Option B",
  "states the deadline is 30 days", "includes hand hygiene as an intervention", "selects rooms
  302, 308, 411", "lists these 5 entities: ...", "states that >10 missed items requires a
  corrective action plan to the District Manager" (anchor terms/values fully specified).
- Mechanically decidable prohibitions / constraints: "no cells show Excel errors", "no
  photos of any kind", "no work scheduled on weekends", "all rows belong only to systems A,B,C",
  "does not exceed -0.1 dBTP", "no Store ID absent from the reference file".
- Exact sequence specs that are fully determined: "lists the steps in this order: A → B → C".

Typical is_closed = 0:
- Open-ended content where the content is not predetermined: "explains why…", "provides a
  rationale", "describes the student's situation", "analyzes the risks", "offers at least one
  example of …", "discusses implications", "recommendations are supported by the data".
- Subjective quality / style / tone: "clearly", "concise", "professional", "persuasive",
  "appropriate for the audience", "comprehensive", "well organized", "engaging", "accurate
  and complete" (where accuracy is holistic), "visually appealing".
- Holistic / gestalt checks: "the narrative flows logically", "the plan is realistic",
  "no material contradictions with the reference" (requires reading & judgment).
Mixed criteria: if the DECISIVE part requires judgment (e.g. "provides a comprehensive policy
with a scope section" → "comprehensive" decides), label 0. If a judgment word is merely
decorative and the check is really mechanical ("clearly labeled sheet named 'Summary'"), label 1.
Tie-break: verbs like states / lists / names / includes <specified X> / equals / contains /
labeled / exactly → lean 1; explains / describes / discusses / justifies / analyzes /
synthesizes / addresses / evaluates / appropriately / effectively → lean 0.

## Label 2 — is_narrative  (1 = 明确衡量"如何讲故事")

is_narrative = 1 when the criterion evaluates the GLOBAL NARRATIVE ORDER / LOGICAL LAYOUT of how
the deliverable presents its content to the reader — i.e. RELATIONS AMONG MULTIPLE PARTS
(what comes first / next / last, hierarchy, flow), not whether some single element exists.
Include:
- Presentation order / position: "opens with an executive summary / BLUF", "begins with the
  conclusion", "ends with a call to action / next steps", "X is presented before Y",
  "sections follow the order Introduction → Methods → Results", "chronological narrative".
- 总分 / 分总 / hierarchical structure: overview-then-details, summary up front followed by
  supporting sections, a thesis then supporting paragraphs, "each paragraph develops/supports
  the central argument", "conclusion follows from / is built up by the preceding analysis".
- Relations among sub-points: parallel vs progressive (并列/递进), "builds from … to …",
  transitions linking sections, "each section leads into the next", logical progression.
- Priority ordering for the reader: "most important / highest-risk items first",
  "ranked/prioritized list from most to least important" (as a presentation choice).
- Holistic organization / flow / coherence of the document or presentation: "well organized
  with a logical flow", "the story arc is coherent", "slides follow a logical sequence",
  "structured logically", "the email is organized so the ask is up front".
- Scene / story structure in creative work (scripts, videos, articles): "the piece has a clear
  beginning, middle and end", "hook in the first 5 seconds then reveal", "the edit builds to a
  climax", "lede first, then nut graf".
Exclude (is_narrative = 0):
- Existence of a section / heading / element ("includes a Scope section", "has an Introduction"),
  even though it mentions structure, unless its POSITION or RELATION to other parts is judged.
- Single-point content checks (a statement, value, conclusion, or fact is present).
- Pure formatting (fonts, bullets, tables, headers/footers, colors, page numbers, labels).
- Sorting of data rows/columns in a table or spreadsheet ("rows sorted by date"), template
  layout of a form/spreadsheet, field arrangement — these are data layout, not storytelling.
- Correctness of domain sequencing that is about the real-world plan, not the presentation
  (e.g. "no post-production task begins before the shoot day", "vendor visits scheduled in a
  feasible order", "dosage titration schedule order") — that's content correctness.
- Fidelity to a reference's sequence where the sequence is domain content (e.g. "lists the
  workflow steps in the reference's order: schedule → travel → draw …") → usually 0 unless
  it is explicitly about the order in which the document presents its argument/story.
  (A song structure / music arrangement unchanged → 0, it's audio content fidelity.)
Gray zone guidance: a procedural SOP whose criterion says "steps are presented in a logical,
sequential order" → 1 (judging presentation order). "Paragraph order" edits in an editing task
→ 1 if it judges whether the order improves the flow; 0 if it only checks a comment exists.

## Auxiliary — check_type (one code, the PRIMARY nature of the check)
- FMT   file / format / naming / structural presence / formatting / length / count specs
- VAL   specific numeric / date / computed value or formula
- FACT  a specified fact / entity / term / categorical answer / specified prohibited item
- OPEN  open-ended content requirement (explain, justify, analyze, provide examples)
- QUAL  subjective quality / style / tone / clarity / professionalism / holistic accuracy
- ORD   ordering / organization / flow / narrative structure (often is_narrative=1, but data
        sorting or domain sequencing may be ORD with is_narrative=0)

is_closed and is_narrative are independent; both can be 1 (e.g. "the memo opens with the
sentence 'Recommendation: approve'" — exact position + exact content).

## Output format (TSV, no header, one line per item, every item exactly once, in input order)
<item_id>\t<is_closed 0/1>\t<is_narrative 0/1>\t<check_type>\t<note>
<note> is REQUIRED (≤ 15 words, English) when is_narrative = 1 (say what ordering/structure is
judged) or when the call was genuinely borderline (prefix "BORDERLINE: "); otherwise leave empty
(the line then ends with a trailing tab).
