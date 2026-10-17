# GDPval rubric-item labeling codebook (v2)

Each GDPval task has a rubric: a list of criteria a grader checks against the deliverable
(Excel/Word/PDF/PPT/audio/video etc.). You label EACH rubric item (criterion) with a 3-level
closedness grade, a binary narrative label, and one auxiliary category. Judge the criterion text
itself (use the task prompt only as context). Negative-score items (penalties, e.g. "-10 Includes
X") are labeled by what they check, exactly like positive ones.

## Label 1 — closed_level (0 / 1 / 2)
The question behind it: does the criterion demand a DETERMINATE result with a correct answer, and
could pass/fail be decided by a PROGRAM (明确要求取得一个可程序化核验的确定结果)?

### 2 = PROGRAMMATIC — a determinate result AND a deterministic script could check it
A developer could write a verifier from the criterion text + the task's reference files, using
file parsing, exact/normalized string match, a SHORT keyword/synonym list, regex, numeric
comparison with tolerance, counting, date arithmetic, cell/sheet/slide/page inspection, or signal
measurement. No reading comprehension or judgment needed. Examples:
- File / naming / structure: "is an .xlsx whose basename is 'Sample'", "worksheet named exactly
  X", "has a section/heading labeled 'Surveillance'", "10–12 slides", "under 500 words",
  "every slide has a title", "column K contains 1 for sampled rows", "is a PDF", "footer contains
  slide number", "a column titled 'Color' or 'Colour'".
- Exact values / calculations: "sample size is 59", "credit balance of 45,123.29", "38% ± 0.5%",
  "N equals the row count of the reference", "days' supply = floor(...)", "-17 to -15 LUFS".
- Named entities / literal strings that must appear or be chosen, matchable by keywords:
  "lists the medication as Vraylar", "signature blocks name Beth Cobb (City Clerk) and Robert
  Howell", "states Carpenter is the top-selling fit with 309 units and $30,693", "recommends
  Option B", "follow-up timeframe within 14 days", "cites the ACO REACH PY2025 report".
- Mechanical constraints / prohibitions: "no cells show Excel errors", "no work on weekends",
  "every vendor preferring Arena is assigned only Arena tables", "total assigned tables equals
  the sum in the reference", "no Store ID absent from the reference", "no photos of any kind".

### 1 = DETERMINATE BUT SEMANTIC — a specific expected content exists, but checking it needs reading
The criterion pins down WHAT must be said/shown (a specific fact, rule, proposition, step, item,
or decision — there is an answer key), but deciding pass/fail requires understanding paraphrased
natural language or interpreting a chart/image, not a keyword/regex match. Examples:
- "states that items not on the packing slip may experience delayed credit due to validation"
- "includes a clause stating there are no intended third-party beneficiaries"
- "the Monthly section includes reviewing the staff schedule to ensure the pharmacist-to-tech
  ratio complies with CA Board of Pharmacy requirements"
- "buyer consultation section explains that a buyer's agent represents the buyer"
- "includes a chart or table showing fit-level sales breakdown for Men Northeast"
- "the care plan documents 'Aranesp 10 mcg 2x/week' when the dose-decrease criteria are met"
  (requires applying clinical logic to decide which month qualifies) → 1 or 2 by how mechanical.

### 0 = OPEN / SUBJECTIVE — no single correct answer, or pass/fail needs judgment
- The criterion only names a TYPE or TOPIC of content the author must generate, not its specific
  content: "contains at least one prompt related to inventory levels", "provides a rationale",
  "states at least one difference between the new and existing order types", "gives an example",
  "describes how mixed-type POs are handled", "explains what warts are", "interprets the results".
- Quality / style / tone / clarity / adequacy / appropriateness / completeness: "clear",
  "concise", "professional", "persuasive", "appropriate for a mixed audience", "comprehensive",
  "well organized", "overall formatting and style", "realistic", "usable by case managers".
- Holistic accuracy or consistency judgments: "no material contradictions with the reference",
  "the conclusion is supported by the analysis".

Mixed criteria: grade by the DECISIVE (hardest) part. "Provides a comprehensive policy with a
scope section" → "comprehensive" decides → 0. A decorative adverb that does not change the check
("clearly labeled sheet named 'Summary'") is ignored → 2.

## Label 2 — is_narrative (0 / 1)  (1 = 明确衡量"如何讲故事")
is_narrative = 1 when the criterion evaluates the GLOBAL NARRATIVE ORDER / LOGICAL LAYOUT of how
the deliverable presents its content to the reader — RELATIONS AMONG MULTIPLE PARTS (what comes
first / next / last, hierarchy, flow), not whether some single element exists. Include:
- Presentation order / position: "opens with an executive summary / BLUF", "begins with the
  conclusion", "agenda slide near the beginning", "ends with a call to action / summary slide",
  "X is presented before Y", "sections follow Introduction → Methods → Results", "chronological".
- 总分 / 分总 / hierarchical structure: overview-then-details, summary up front followed by
  supporting sections, thesis then supporting paragraphs, "each paragraph develops/supports the
  central argument", "the conclusion follows from the preceding analysis".
- Relations among sub-points: parallel vs progressive (并列/递进), "builds from … to …",
  transitions linking sections, logical progression from one section to the next.
- Priority ordering for the reader: "most important / highest-risk items first", "ranked from
  most to least important" (as a presentation choice).
- Holistic organization / flow / coherence of the text or presentation: "logical flow",
  "slides follow a logical sequence", "structured logically", "coherent story arc".
- Story structure in creative work (scripts, videos, articles): "clear beginning, middle, end",
  "hook in the first 5 seconds", "builds to a climax", "lede first, then nut graf".
- Presentation sequence of procedures: "SOP steps are presented in a logical sequential order",
  "SBAR sections appear in the order S, B, A, R".
Exclude (is_narrative = 0):
- Existence of a section / heading / element ("includes a Scope section", "has an Introduction"),
  unless its POSITION or RELATION to other parts is judged.
- Single-point content checks (a statement, value, conclusion, or fact is present).
- Pure formatting (fonts, bullets, tables, headers/footers, colors, page numbers) and
  conventional boilerplate placement (title at top, signature block at the end of a contract,
  footer at bottom of page).
- Sorting / arrangement of data rows, columns, monthly blocks or form fields in a spreadsheet or
  form ("rows sorted by date", "rows keep original order", "12 monthly sections in sequence").
- Correctness of real-world sequencing that is domain content rather than presentation (e.g. "no
  post-production task begins before the shoot day", "delivery scheduled after inspection").
- Fidelity to a reference's process sequence that is domain content (e.g. "the workflow diagram
  lists the reference's steps in order"), or audio/music structure fidelity.
- "Organized clearly / usable" when it judges usability of a tool or spreadsheet, not the order
  or flow of a narrative.

## Auxiliary — check_type (one code, the PRIMARY nature of the check)
- FMT   file / format / naming / structural presence / formatting / length / count specs
- VAL   specific numeric / date / computed value or formula
- FACT  a specified fact / entity / term / decision / specified prohibited item
- OPEN  open-ended content requirement (explain, justify, analyze, provide examples, topic-only)
- QUAL  subjective quality / style / tone / clarity / professionalism / holistic accuracy
- ORD   ordering / organization / flow / narrative structure (often is_narrative=1, but data
        sorting or domain sequencing may be ORD with is_narrative=0)

closed_level and is_narrative are independent; e.g. "SBAR sections in order S, B, A, R" is
closed_level=2 and is_narrative=1; "the deck flows logically" is closed_level=0, is_narrative=1.

## Output format (TSV, no header, one line per item, every item exactly once, in input order)
<item_id>\t<closed_level 0/1/2>\t<is_narrative 0/1>\t<check_type>\t<note>
<note> is REQUIRED (≤ 15 words, English) when is_narrative = 1 (say what ordering/structure is
judged) or when the call was genuinely borderline (prefix "BORDERLINE: "); otherwise leave empty
(the line then ends with a trailing tab).
