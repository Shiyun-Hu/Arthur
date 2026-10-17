"""Final is_narrative adjudication.

Candidates = every item flagged by pass 1 or pass 2, plus a keyword/ORD-type recall sweep over
items both passes left at 0. Each candidate was read in full and assigned under these rules
(see README for the full statement):

  FLOW  - judges overall organization / flow / coherence / argument development / story arc
  ORDER - judges the relative order of >= 2 content parts (section/slide order, X before Y,
          chronological or step-by-step presentation, prioritized / front-loaded ordering)
  FRAME - a framing element (summary / BLUF / overview / roadmap / purpose / hook / lead, or a
          closing synthesis / conclusion / recommendation / CTA) with an explicit opening or
          closing position, or an explicit framing relation (previews / synthesizes)

Excluded: boilerplate placement (title, headline, TOC, greeting, sign-off, courteous closing,
logos, links, references, appendix), data/tab/column/row/field order, chart ranking order,
real-world plan or process sequencing, bare existence of a named section, content merely located
in a section.
"""

NARRATIVE = {
    # FLOW
    '050-004': 'FLOW', '050-008': 'FLOW', '050-014': 'FLOW', '055-028': 'FLOW', '068-049': 'FLOW',
    '126-003': 'FLOW', '126-005': 'FLOW', '128-028': 'FLOW', '175-011': 'FLOW',
    # ORDER
    '023-003': 'ORDER', '024-004': 'ORDER', '032-056': 'ORDER', '032-057': 'ORDER',
    '032-058': 'ORDER', '032-059': 'ORDER', '036-010': 'ORDER', '037-002': 'ORDER',
    '040-001': 'ORDER', '055-021': 'ORDER', '058-021': 'ORDER', '068-005': 'ORDER',
    '081-007': 'ORDER', '098-034': 'ORDER', '103-020': 'ORDER', '104-001': 'ORDER',
    '104-016': 'ORDER', '104-049': 'ORDER', '111-071': 'ORDER', '112-002': 'ORDER',
    '130-002': 'ORDER', '131-003': 'ORDER', '133-005': 'ORDER', '140-034': 'ORDER',
    '147-005': 'ORDER', '147-019': 'ORDER', '159-002': 'ORDER', '159-014': 'ORDER',
    '180-008': 'ORDER', '195-004': 'ORDER',
    # FRAME
    '019-053': 'FRAME', '023-047': 'FRAME', '035-003': 'FRAME', '041-050': 'FRAME',
    '057-009': 'FRAME', '057-021': 'FRAME', '062-013': 'FRAME', '068-034': 'FRAME',
    '070-023': 'FRAME', '077-000': 'FRAME', '077-054': 'FRAME', '093-014': 'FRAME',
    '098-032': 'FRAME', '099-042': 'FRAME', '107-010': 'FRAME', '117-003': 'FRAME',
    '128-036': 'FRAME', '140-029': 'FRAME', '140-030': 'FRAME', '148-008': 'FRAME',
    '148-040': 'FRAME', '149-033': 'FRAME', '153-048': 'FRAME', '163-047': 'FRAME',
    '192-004': 'FRAME', '192-039': 'FRAME', '193-028': 'FRAME', '194-032': 'FRAME',
    '205-023': 'FRAME', '206-035': 'FRAME', '212-037': 'FRAME',
}

# Items where the final label differs from at least one pass, with the reason.
OVERRIDES = {
    '016-003': (0, 'P1=1: "logical organization" is defined by headings/sections, i.e. formatting'),
    '058-006': (0, 'P1=1: logo as first shot is branding boilerplate'),
    '058-007': (0, 'P1=1: logo as final shot is branding boilerplate'),
    '147-033': (0, 'P1=1: courteous contact-us closing is boilerplate (cf. 149-046, 155-051)'),
    '037-002': (1, 'P2=0: day sections presented in chronological order (cf. 036-010)'),
    '070-023': (1, 'P2=0: headline at top summarizes the thesis = BLUF (cf. 068-034)'),
    '107-010': (1, 'P2=0: roadmap previewing the memo = overview-first (cf. 163-047)'),
    '023-003': (1, 'P1=0: report sections must follow template order (cf. 081-007, 112-002)'),
    '024-004': (1, 'P1=0: headings must follow guide order (cf. 081-007, 112-002)'),
    '098-034': (1, 'P1=0: process presented as ordered step sequence (cf. 040-001, 195-004)'),
    '140-029': (1, 'P1=0: concluding summary synthesizing key differences (cf. 206-035)'),
    '099-042': (1, 'both=0: purpose line at the top frames the form (cf. 194-032)'),
    '140-030': (1, 'both=0: intro outlining concepts to be covered = roadmap (cf. 163-047)'),
    '148-040': (1, 'both=0: conclusion synthesizes the observations (cf. 149-033)'),
    '193-028': (1, 'both=0: executive summary / closing section summarizing recommendations'),
}
