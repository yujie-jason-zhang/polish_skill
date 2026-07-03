---
name: journal-recommender
description: >-
  Recommend target journals for a finished or near-finished manuscript. Use when the user asks where to submit, wants a shortlist, checks fit for a journal, compares SCI/non-SCI, OA/subscription, Chinese/English, fast-review venues, or asks which journals are realistic. Gather indexing, OA/budget, language, deadline, avoid-list, subfield, keywords, abstract/results, article type, and level anchor; estimate paper level; then return about 10 journals each in reach, fast-review reach, safe, and fast-review safe tiers. Each journal must include a fit rationale, recent related-paper evidence from that journal, official-site and LetPub URLs, and an adjustment note when borderline. Web search is mandatory: verify the journal site, LetPub page, and recent related papers live, not from memory. Use before paper-cover-letter.
---

# Journal Recommender

## Scope

Use this skill when the manuscript is finished or nearly finished and the user needs to choose where to submit it: a target-journal shortlist, a fit check for a specific journal, a comparison across SCI/non-SCI, open-access/subscription, or Chinese/English options, or a realistic read on which journals a paper's level can support.

Read `references/journal_recommendation_guide.md` for the full intake question bank, the source-authority table, the fit-rationale and adjustment templates, the predatory/early-warning red flags, and the output template before producing a full recommendation. For a single-journal fit check, the rules below are enough.

Use another skill when the task is primarily:

- estimating whether the underlying idea is novel or strong enough to publish at all, before venue choice: use `idea-novelty-auditor` (if available). Reuse its level read here rather than re-deriving it;
- literature review, related work, or reference selection: use `problem-driven-literature-review` (if available);
- manuscript storyline, contribution framing, or section structure: use `paper-argument-reconstructor` (if available);
- drafting the cover letter once a target journal is chosen: use `paper-cover-letter` (if available). This skill runs *before* the cover letter;
- TeX-safe or final-language polishing: use `paper-polisher` (if available).

This skill matches a manuscript to venues. It does not judge whether the science is correct, and it does not write the submission letter.

## Verification Mode

This skill has two modes. By default it produces a recommendation as described above. When the input is a journal shortlist or a fit claim another tool, advisor, or skill has already produced, switch to verification mode instead of regenerating:

- do not overwrite the other source's list;
- check it against this skill's discipline: does each journal actually match the stated scope and the paper's level; does recent related-paper evidence support the scope fit; are indexing, open-access, APC, metric, and review-speed claims asserted as fact when they should be flagged; is any journal on an early-warning list or showing predatory red flags; is the paper's level over-estimated so that "reach" is really "unrealistic";
- report only the problems; correct one in place only if it breaks a non-negotiable rule (an asserted-as-fact metric, a predatory venue, or an early-warning-listed journal).

The suite's value is bounded, verifiable recommendations, not a competing list. Verify rather than replace what a stronger generator already produced.

## Non-Negotiable Rules

Journal metadata is the single most fabrication-prone part of this task, and the two dimensions the user usually cares most about — how ambitious a venue is and how fast it reviews — are the two the model is most likely to get wrong. Hold the line:

- **Web search is mandatory. Do not recommend from memory.** Every journal in the output must have been verified live in this session. For each one, search and open its official website *and* its LetPub page before listing it, and base the facts on those pages. If no web/search/browsing tool is available, say so and stop — do not fall back to recalled facts.
- **Do not invent journals.** Recommend only venues you have found and verified. Never fabricate a journal name, ISSN, or publisher to fill a tier.
- **Do not choose by manuscript template.** The current LaTeX/Word template, class file, citation style, or visible publisher format is not evidence that the paper must target that publisher or society. A manuscript written in an IEEE template can still be submitted to Elsevier, Springer Nature, Wiley, Taylor & Francis, MDPI, society journals, or other venues after reformatting. Use template information only as a later reformatting note, unless the user states a publisher or venue is a hard constraint.
- **Verify every fact against the sources, and prefer bands over false precision.** Confirm indexing, quartiles, Impact Factor/JIF, CiteScore, 中科院分区, 北大核心/CSSCI/CSCD, APC/page fees, and article types from the authoritative sources in the guide: journal site for scope, article types, and fees; Clarivate/JCR or Scopus for indexing and metrics; official Chinese/CAS catalogs where relevant; LetPub for review speed and other LetPub-reported signals. These drift year to year and journals get delisted, so trust live sources, not memory. Give the year of any metric.
- **Verify recent content fit.** For every journal in the final output, search the journal's own archive/site and at least one scholarly index for recent articles matching the manuscript's subfield and keywords. Use this as evidence for scope fit: 3+ close recent papers is strong evidence, 1-2 related papers is moderate, none is a weak-fit warning unless the aims & scope clearly supports the topic. Do not rely on generic aims & scope alone when recent contents suggest the journal rarely publishes the field.
- **Never invent URLs.** List only the real URLs you actually landed on. A LetPub journal link carries an internal id you cannot know from memory, so take it from the search result rather than constructing it. If you cannot find a journal's official site or its LetPub page, write "not found" instead of guessing one.
- **Review speed is the least reliable dimension.** Report the LetPub-reported turnaround with attribution and its URL, plus a qualitative band (fast / moderate / slow); note that crowd-sourced data is indicative, not guaranteed, and do not assert a precise figure the sources do not support.
- **Screen for predatory and early-warning venues.** Before listing any journal — especially fast, open-access, or high-APC ones — check for red flags (aggressive solicitation, fabricated metrics, no clear peer review, claims of open access without a DOAJ listing, hijacked/clone journals, or presence on the CAS international early-warning list, 中科院国际期刊预警名单). Flag or exclude them; never recommend a venue you would not defend to the user's advisor.
- **Level judgments are estimates, not verdicts.** Base the reach/safe split on an explicit, hedged read of the paper's level from what the user provides, state the basis, and recommend the user calibrate with an advisor. Do not present "reach" as attainable when the gap is large — label it honestly.
- **Coverage without padding.** For a full recommendation, aim for about 10 journals per tier, but every listed journal must be a genuine scope-and-level fit with a real rationale. When a tier is thin — "fast-review reach" often is, because more selective venues frequently review slowly — say so and explain why rather than inserting weak fits.

## Rule-Conflict Escalation

If the user pushes for a definitive review time, a guaranteed acceptance read, or insists a venue is indexed/legitimate when you cannot confirm it, stop and state what you can and cannot verify rather than asserting it. If the user asks you to recommend a journal that shows early-warning or predatory red flags, surface the concern before listing it and let the user decide. If your own draft drifts into stating a metric or turnaround the pages do not support, revise it back to what the sources actually show, attributed, without asking.

## Intake

Gather the constraints below before recommending. Ask them in two compact groups; if the user leaves some blank, proceed with a stated assumption rather than stalling, and echo every assumption back so it can be corrected. See the guide for the full question bank and sensible defaults.

Hard constraints (these gate the shortlist):

- required indexing, if any: SCIE / SSCI / A&HCI / EI / Scopus / 北大核心 / CSSCI / CSCD / none;
- open access: must be OA / OA optional / prefer subscription;
- publishing budget: APC or page-fee ceiling, or "must be free to publish";
- language: English / Chinese / either;
- deadline: any hard deadline (graduation, grant, tenure) and by when — this sets how much weight the fast-review tiers carry;
- avoid-list: early-warning list (中科院预警名单), institution blacklist, specific publishers, conflicts of interest, or venues that already rejected the paper.

Paper-fit inputs (these set scope and level):

- target subfield plus 3–6 keywords — journal scope is narrow, so this matters more than a broad field name;
- the abstract, or problem + method + main results;
- a level anchor: where the user's similar work usually lands, the advisor's read, or a self-assessed quartile;
- intended article type: full/regular paper, letter, brief, short paper, or review — this affects both fit and speed.
- current manuscript template or publisher format, if mentioned: record it only as a reformatting note, not as a journal-selection constraint unless the user explicitly says it is one.

## Workflow

1. Run intake. Collect the hard constraints and paper-fit inputs; state an assumption for anything left blank.
2. Estimate the paper's level (hedged) from significance, novelty, rigor, completeness of results, baselines beaten, and the user's anchor. Reuse `idea-novelty-auditor` output if it exists. State the basis in one or two lines.
3. Build a broad candidate set of venues whose aims and scope match the subfield and keywords, then drop any that clearly fail a hard constraint (wrong indexing, OA/budget mismatch, wrong language, on the avoid-list). Do not drop or prefer venues merely because the manuscript is currently written in a particular publisher or society template.
4. Narrow the broad set into a finalist pool large enough to support about 10 genuine entries per tier after verification losses. If the field or constraints make that unrealistic, keep only defensible finalists and state that the tier is thin.
5. For every finalist that may appear in the final list, web-search and open its official website and its LetPub page. Take aims & scope, article types, and APC/page fees from the official site; take review speed and LetPub-reported signals from LetPub; confirm indexing and metrics on the authoritative sources in the guide, including Master Journal List/JCR, Scopus, DOAJ, and official Chinese/CAS catalogs where relevant. Record the real URLs you land on.
6. For every finalist that may appear in the final list, search for recent papers in that journal using the manuscript's subfield and 3-6 keywords, plus broader synonyms if needed. Prefer the journal's own archive/search, then PubMed/Crossref/OpenAlex/Semantic Scholar/discipline databases or another available scholarly search source. Record 1-3 representative related articles with year and DOI/URL, or write "no close recent match found" when none is found.
7. Use the recent-paper evidence to re-evaluate scope fit: keep strong/moderate fits, downgrade borderline fits, and exclude journals whose recent contents show little connection to the manuscript unless there is a clear strategic reason to keep them with a caution.
8. Screen the survivors for predatory and early-warning red flags; exclude or flag.
9. Sort into the four tiers by combining the paper's estimated level with each venue's selectivity, its LetPub-reported review speed, and the strength of its recent related-paper evidence.
10. For each journal, write the fit rationale (scope + recent-content evidence + level + constraint match), attach its official-site and LetPub URLs (the real ones from step 5; write "not found" if either was missing), include representative related papers from step 6, and, when the fit is borderline, a concrete adjustment note.
11. Assemble the output: constraints echo, level estimate, the four tiers (about 10 entries per tier when genuine verified fits exist, each carrying both URLs and related-paper evidence), and a red-flag section. Point the user to `paper-cover-letter` for the chosen venue.

## The Four Tiers

The tiers cross two axes — ambition and review speed. For a full recommendation, aim for about 10 journals per tier. Populate each broadly but honestly; if a tier has fewer than 10 genuine verified fits, say so rather than padding it.

- **Reach (可冲):** venues at or slightly above the paper's estimated level. Acceptance is uncertain but plausible with a strong submission; normal review timeline. Higher payoff, higher risk.
- **Fast-review reach (审稿快的可冲):** reach-level venues that also tend to turn around quickly. State honestly when this tier is thin — selective venues often review slowly — instead of padding it.
- **Safe (稳的):** venues at or slightly below the paper's level where acceptance is more likely. The dependable fallback.
- **Fast-review safe (快速审稿稳的):** safe-tier venues with fast turnaround — the bucket for a hard deadline. Reliable-and-fast sometimes means large open-access journals, which is fine when legitimate (DOAJ-listed), but screen these hardest for predatory red flags and always surface the APC.

## Fact Verification

This skill requires web search. Do not produce recommendations from recalled facts; if no web/search/browsing tool is available, say so and stop. See the source-authority table in the guide for what each source is authoritative for.

For every journal you list, you must have opened both:

- its **official website** — for indexing claims, aims & scope, article types, and APC/page fees;
- its **LetPub page** — for review-speed signal and LetPub-reported 中科院分区, impact metric, or acceptance-rate data. LetPub aggregates and crowd-sources these, so attribute the figures to LetPub and prefer primary metric sources when available.

Also confirm indexing on the Clarivate Master Journal List and/or the Scopus source list, open-access legitimacy on DOAJ, and screen against the CAS international early-warning list (中科院国际期刊预警名单).

For every journal you list, also verify **recent related-paper evidence**:

- Search the journal's own site/archive for the manuscript's exact keywords and broader synonyms.
- Search at least one scholarly index or general scholarly search source with a query like `"<journal title>" <keyword1> <keyword2>` when the journal site search is weak.
- Prefer the most recent 3-5 years unless the field is slow-moving; include 1-3 representative article titles with year and DOI/URL.
- Treat the result as fit evidence, not a mechanical pass/fail: no close recent match is a warning, while several close matches strengthen scope fit.

List the real URLs you actually landed on. Never construct or guess a URL — a LetPub journal link carries an internal id you cannot know from memory, so take it from the search result. If you cannot find a journal's official site or its LetPub page, write "not found" rather than inventing one.

For review speed: report the LetPub-reported turnaround with attribution and its URL, plus a qualitative band (fast / moderate / slow). Note that crowd-sourced data is indicative, not guaranteed; do not assert a precise figure the sources do not support.

## Output Format

For a full recommendation, return, in this order:

```text
Constraints (as gathered / assumed):
- indexing / OA / budget / language / deadline / avoid-list
- [assumptions flagged]

Estimated paper level (estimate):
- level band + one-line basis

Each tier: aim for about 10 entries; if fewer genuine verified fits exist, state why the tier is thin.

Reach (可冲):
- Journal — indexing · OA/APC · review speed [band + LetPub-reported figure]
  Official site: <real URL, or "not found">
  LetPub: <real URL, or "not found">
  Recent related papers: <1-3 representative papers with year + DOI/URL, or "no close recent match found">
  Fit: scope + recent-content evidence + level + constraint match
  Adjust if borderline: concrete change that would improve fit

Fast-review reach (审稿快的可冲):
- ... (same fields per entry; state if this tier is thin and why)

Safe (稳的):
- ... (same fields per entry)

Fast-review safe (快速审稿稳的):
- ... (same fields per entry; surface the APC)

Red flags / cautions:
- any early-warning, predatory, or hijacked-journal concerns found during verification

Next step:
- pick a target, then use paper-cover-letter.
```

Every journal entry carries its official-site and LetPub URLs. Facts come from those live pages, not memory.

For a single-journal fit check, return only the scope/level/constraint match, the verification flags, and — if borderline — the adjustment that would make it fit.
