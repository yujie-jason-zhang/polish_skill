# Journal Recommendation Guide

## Contents

- Goal
- Core principle
- Intake question bank
- Estimating the paper's level
- The four tiers
- Field-top reference candidates
- Fact verification and source authority
- Predatory and early-warning red flags
- Fit rationale template
- Adjustment playbook (when a journal is not a fit)
- Output template
- Worked example

## Goal

Match a finished or near-finished manuscript to a realistic set of target journals, sorted by ambition and review speed, so the user can choose where to submit. The output is a shortlist with a defensible reason for each venue, an honest read on the paper's level, and a clear record of what still needs to be verified before submission.

This is a matching task, not a science review and not a sales pitch. It reuses the paper's established scope and level; it does not invent strengths the manuscript does not have, and it does not assert journal facts it cannot stand behind.

## Core principle

```text
gather hard constraints -> estimate level -> match scope -> drop clear constraint failures -> build a finalist pool -> verify each listed journal's official site + LetPub + source-authority records -> verify recent related papers in the journal -> screen for red flags -> sort into tiers -> optionally add field-top reference candidates outside the tiers -> explain fit, list URLs, related-paper evidence, and how to adjust
```

This skill is online-only: every recommended journal is verified live against its official website, its LetPub page, and recent papers in that journal related to the manuscript field. Nothing is recommended from memory; if no web/search/browsing tool is available, say so and stop.

Two failure modes to avoid:

- fabrication: inventing journals, URLs, or related-paper evidence, or asserting indexing, quartile, impact metric, APC, or review speed that the live pages do not support. Review speed is the least reliable field, so take it from LetPub and attribute it;
- over-reach: labeling a venue "reach" when the level gap is large, so the user wastes a submission cycle.
- prestige drift: using cross-field prestige titles as generic "top recommendations." The top-reference lane should usually name field-specific high-visibility venues close to the manuscript's discipline, not Nature/Science/Cell-family style journals unless the user explicitly asks for that level or the manuscript evidence genuinely supports it.

## Intake question bank

Ask these in two compact groups. If the user leaves an item blank, proceed with the default in brackets and echo the assumption back so it can be corrected.

Hard constraints (gate the shortlist):

- Required indexing: SCIE / SSCI / A&HCI / EI / Scopus / 北大核心 / CSSCI / CSCD / none. [default: none — but confirm, since many institutions require a specific index]
- Open access: must be OA / OA optional / prefer subscription. [default: OA optional]
- Publishing budget: APC or page-fee ceiling, or "must be free to publish." [default: ask — do not assume a budget]
- Language: English / Chinese / either. [default: English]
- Deadline: any hard deadline (graduation, grant, tenure) and by when. [default: none — but if present, weight the fast-review tiers]
- Avoid-list: early-warning list (中科院预警名单), institution blacklist, specific publishers, conflicts of interest, venues that already rejected the paper. [default: none]

Paper-fit inputs (set scope and level):

- Target subfield + 3–6 keywords. Scope is narrow; a broad field name is not enough.
- Abstract, or problem + method + main results.
- Level anchor: where the user's similar work usually lands, the advisor's read, or a self-assessed quartile. [default: infer from the abstract and say so]
- Intended article type: full/regular paper, letter, brief, short paper, review. [default: full paper]
- Current manuscript template or publisher format, if mentioned. [use only as a reformatting note; do not treat IEEE/Elsevier/Springer/etc. formatting as a venue constraint unless the user explicitly says so]

Optional but useful:

- Any journals already considered or that an advisor suggested.
- Whether the user wants breadth beyond the default of about 10 journals per tier, or a tighter top-few per tier.

## Estimating the paper's level

The reach/safe split depends on an honest read of the paper's level. Base it on:

- problem significance and audience breadth;
- novelty and defensibility of the contribution (reuse `idea-novelty-auditor` output if available);
- rigor and completeness of results: baselines beaten, ablations, breadth of evaluation, statistical support;
- the user's own anchor, which usually outweighs a cold read of the abstract.

State the level as a band with a one-line basis, and mark it an estimate. Recommend the user calibrate with an advisor. Do not convert a specialized-sounding topic into a high level by itself. When the abstract is thin, say the estimate is low-confidence and lean on the user's anchor.

## The four tiers

The tiers cross two axes: ambition (reach vs safe) and review speed (fast vs normal). For a full recommendation, aim for about 10 journals per tier, but only with genuine fits. If a tier has fewer than 10 defensible verified journals, state why the tier is thin rather than padding.

- Reach (可冲): at or slightly above the estimated level. Acceptance uncertain but plausible with a strong submission; normal review timeline.
- Fast-review reach (审稿快的可冲): reach-level venues that also tend to review quickly. Frequently thin, because selective venues often review slowly — say so rather than padding.
- Safe (稳的): at or slightly below the level, where acceptance is more likely. The dependable fallback.
- Fast-review safe (快速审稿稳的): safe venues with fast turnaround, for a hard deadline. Reliable-and-fast sometimes means large open-access journals; screen these hardest for predatory red flags and always show the APC.

A venue can legitimately appear in two tiers (e.g., a safe venue that also reviews fast belongs in both "safe" and "fast-review safe"). That is fine; note it rather than duplicating the full rationale.

Do not use the manuscript's current formatting template to assign the venue family. A paper drafted in an IEEE LaTeX template can still be a good fit for Elsevier, Springer Nature, Wiley, Taylor & Francis, MDPI, society, or university-press journals after reformatting. Treat template mismatch as an operational reformatting task after target selection, not as scope or level evidence.

## Field-top reference candidates

Add an optional "Field-top reference candidates (outside the four tiers)" lane when it helps the user understand the ceiling of the direction. This lane is a calibration reference, not a fifth tier, not an acceptance prediction, and not part of the four-tier shortlist. Include at most 1-3 venues.

Choose candidates with all of the following discipline:

- The venue is a recognized high-visibility destination in the manuscript's actual subfield: a flagship society journal, leading transactions journal, elite subfield journal, or equivalent field-native venue.
- The venue is usually only about half a step to one step above the "Reach" tier. If the level gap is several steps, omit it or label it explicitly unrealistic rather than presenting it as a useful target.
- The venue's scope and recent contents match the manuscript's topic closely enough that a strengthened version of the paper could be legible there.
- The venue has been verified with the same official-site, LetPub, indexing, recent-related-paper, and red-flag checks as the four tiers.

Do not default to cross-field mega-journals, broad prestige brands, or unrelated clinical/biomedical/physical-science titles just because they are famous. For example, an engineering or robotics manuscript's top-reference lane should usually be built from field-native flagship venues, not generic Nature/Science/Cell-family targets. If the user specifically asks for those ultra-high-risk targets, present them separately as "ultra-long-shot prestige venues" and make the gap explicit.

For each field-top candidate, write:

- why it is top for this direction, grounded in scope and recent contents;
- current realism: realistic stretch / long-shot / unrealistic;
- what must be strengthened before attempting it: e.g., stronger theory, a decisive benchmark, broader baselines, ablations, real-system deployment, clinical/field validation, larger dataset, reproducibility package, or audience reframing.

## Fact verification and source authority

This skill requires web search. For every journal you list, open its **official website** and its **LetPub page** first; the table below shows which source is authoritative for each fact. Do not recommend from memory; if no search/browsing tool is available, say so and stop.

| Fact | Authoritative source | Notes |
|---|---|---|
| Web of Science indexing (SCIE/SSCI/A&HCI/ESCI) | Clarivate Master Journal List | Indexing changes; journals get delisted. Confirm current status, not memory. |
| Scopus indexing | Scopus source list (title list) | Titles are added and discontinued regularly. |
| Impact Factor / JIF quartile | Clarivate JCR | Released yearly; cite the year. Prefer quartile over a precise decimal. |
| CiteScore | Scopus / journal site | Different metric from JIF; do not conflate. |
| 中科院分区 (CAS tier) | Official 中科院分区 catalog | Basic vs upgraded editions differ; state which. |
| 北大核心 / CSSCI / CSCD | The respective official catalogs | For Chinese-language and China-context venues. |
| Open-access legitimacy | DOAJ | A real OA journal is normally DOAJ-listed. Absence is a red flag, not proof, but worth surfacing. |
| APC / page fees / article types | The journal's own site | Changes often; always the primary source. |
| Predatory / early-warning status | CAS international early-warning list (中科院国际期刊预警名单); reputable predatory-publisher trackers | Surface any hit before recommending. |
| Review speed | LetPub (crowd-sourced) and the journal's own reported time-to-first-decision | Least reliable; report LetPub's figure with attribution + its URL and a band, never a bare precise figure. |
| Recent related-paper evidence | Journal archive/search plus PubMed/Crossref/OpenAlex/Semantic Scholar/discipline databases or another available scholarly search source | Use the manuscript's exact keywords and broader synonyms; prefer recent 3-5 years; cite 1-3 representative papers with year and DOI/URL. |

URL honesty: list only the real URLs you land on. Never construct a LetPub link (it carries an internal journal id you cannot know from memory) or guess a journal's domain — take both URLs from the search results, and write "not found" if a page cannot be located.

Review-speed protocol: report the LetPub-reported turnaround with attribution and its URL, plus a band (fast / moderate / slow). Crowd-sourced data is indicative, not guaranteed; do not present a precise week or month count the pages do not support.

Recent-content protocol: before listing a journal, search inside the journal's archive/site for the manuscript's subfield and 3-6 keywords. If the journal's own search is weak, search available scholarly sources with queries such as `"<journal title>" <keyword1> <keyword2>` and verify the article actually appeared in that journal. Record 1-3 representative recent papers with year and DOI/URL. Use broad synonyms when the exact terms are too narrow, but do not count generic papers as close evidence.

Interpretation bands:

- Strong recent-content fit: at least 3 close papers in the last 3-5 years, or a visible special issue/recurring cluster in the topic.
- Moderate fit: 1-2 close papers, or several adjacent papers that serve the same readership.
- Weak fit: no close recent paper found. Keep only if aims & scope, article type, and audience still make the venue strategically plausible; otherwise exclude or downgrade.

Do not make recent-paper evidence a blind rule. New or interdisciplinary topics may lack exact matches, and some journals are intentionally broad. In those cases, explain the mismatch and what framing would make the submission legible to that journal's audience.

## Predatory and early-warning red flags

Screen every finalist that may be listed, and screen fast/OA/high-APC venues hardest. Flag or exclude on any of:

- aggressive or personalized solicitation to submit, promises of unusually fast acceptance;
- impact metrics that are invented or from non-standard "index" bodies rather than JCR/Scopus;
- no clear description of peer review, or implausibly short review claims;
- claims of open access without a DOAJ listing;
- hijacked or clone journals: a site imitating a legitimate title's name/ISSN;
- presence on the CAS international early-warning list or a known predatory tracker;
- publisher or editorial-board information that is missing, fake, or unverifiable.

Never recommend a venue you would not defend to the user's advisor. When in doubt, list it with the concern stated and let the user decide.

## Fit rationale template

For each recommended journal, give three things:

- Scope match: how the paper's topic and keywords map to the journal's aims and scope, and the kind of paper it publishes.
- Recent-content match: whether the journal has published recent papers in or near the manuscript's topic, with 1-3 representative examples or a clear "no close recent match found" caution.
- Level match: how the paper's estimated level lines up with the journal's selectivity/tier, and therefore why it sits in this tier.
- Constraint match: how it satisfies (or where it strains) the user's indexing, OA, budget, language, and speed requirements.
- Reformatting note only when relevant: if the current manuscript template differs from the target publisher's format, mention that reformatting is needed after choosing the venue, but do not treat it as a fit problem.

Keep each concise. Attach the journal's official-site and LetPub URLs to every entry, include related-paper evidence, and note anything the pages did not confirm.

## Adjustment playbook (when a journal is not a fit)

When a venue is a near-miss, give a concrete adjustment rather than dropping it silently. Common moves:

- Scope drift: reframe the framing/keywords/introduction toward the journal's aims, or emphasize the aspect of the contribution the journal's readership cares about.
- Sparse recent-topic evidence: if the journal has only adjacent or no recent papers on the topic, reframe the manuscript toward the closest recurring theme found in the journal, or move the venue down a tier.
- Level gap (paper below venue): add the experiment, baseline, ablation, or real-world validation the venue's reviewers expect; strengthen the evaluation before attempting it. Or drop to a safe-tier venue.
- Level gap (paper above venue): fine for a fast/safe target, but note the paper may be undersold.
- Article-type mismatch: switch to the article type the journal offers (e.g., submit as a letter or brief), which can also change the review speed.
- Template mismatch: reformat to the target journal's template after selection; do not move a venue down solely because the draft currently uses another publisher's template.
- Constraint strain: if OA is required but the budget is low, look for fee waivers, or for subscription venues in the same scope; if indexing is missing, find the nearest indexed venue in scope.
- Special issues: a relevant special issue can improve fit and sometimes speed; note it as an option, and still screen it.

## Output template

```text
Constraints (as gathered / assumed):
- indexing: ... | OA: ... | budget: ... | language: ... | deadline: ... | avoid: ...
- assumptions: [flagged]

Estimated paper level (estimate):
- <band> — basis: <one line>

Field-top reference candidates (outside the four tiers; optional):
- <Journal> — indexing <...> · OA/APC <...> · speed <band + LetPub figure>
  Official site: <URL, or "not found">
  LetPub: <URL, or "not found">
  Recent related papers: <1-3 representative papers with year + DOI/URL, or "no close recent match found">
  Why top for this direction: <field-specific reason, not generic prestige>
  Current realism: <realistic stretch / long-shot / unrealistic> because <specific gap>
  What to strengthen before attempting: <concrete evidence, experiment, validation, theory, dataset, or framing>

Each tier: aim for about 10 entries; if fewer genuine verified fits exist, state why the tier is thin.

Reach (可冲):
- <Journal> — indexing <SCIE?> · OA/APC <...> · speed <band + LetPub figure>
  Official site: <URL, or "not found">
  LetPub: <URL, or "not found">
  Recent related papers: <1-3 representative papers with year + DOI/URL, or "no close recent match found">
  Fit: <scope> / <recent-content evidence> / <level> / <constraint>
  Adjust if borderline: <concrete change>
- ...

Fast-review reach (审稿快的可冲):
- ...   [if thin: "few genuine fits here, because <reason>"]

Safe (稳的):
- ...

Fast-review safe (快速审稿稳的):
- ...   [surface APC; screen hardest for red flags]

Red flags / cautions:
- <any early-warning / predatory / hijacked concern, or "none found">

Sources checked:
- official site + LetPub opened for every journal listed
- recent related papers searched in each journal's archive/site and at least one scholarly index/search source
- indexing on Master Journal List / Scopus; OA on DOAJ; CAS early-warning list screened

Next step:
- choose a target, then use paper-cover-letter.
```

## Worked example

This shows the *shape* of the online output. URLs, metrics, and review times are written as placeholders here because they come from live search at run time — in a real run, replace each placeholder with the actual page you opened. It is illustrative, not a real recommendation.

Intake (as gathered):

- indexing: SCIE required; OA optional; budget "prefer free but can pay a moderate APC"; language English; deadline: submit within ~2 months (student graduation); avoid: nothing specified.
- subfield: LiDAR-based localization / SLAM in robotics; keywords: point-cloud registration, Monte Carlo localization, degeneracy, real-world deployment.
- inputs: full paper; solid real-world experiments, one moderate methodological novelty, beats two standard baselines; user's anchor: "we usually land around Q2."

Estimated level (estimate): mid-tier (≈ Q2), based on a moderate novelty plus strong deployment results, consistent with the user's anchor. Low-to-moderate confidence without the full manuscript.

Field-top reference candidates (outside the four tiers):

- <Field-native robotics flagship venue> — indexing <confirmed> · <subscription/OA status from site> · speed <band + LetPub-reported first-decision time>.
  Official site: <journal-site URL opened>
  LetPub: <LetPub page URL opened>
  Recent related papers: <1-3 recent articles in this venue on LiDAR localization / point-cloud registration / field robotics, with year + DOI/URL>.
  Why top for this direction: recognized high-visibility destination for robotics systems and autonomy work, with recent contents close to the manuscript's technical audience.
  Current realism: long-shot, because the described manuscript has solid deployment evidence but only moderate methodological novelty.
  What to strengthen before attempting: add a decisive benchmark against stronger current baselines, deeper failure-case analysis, and broader real-world deployment evidence before treating this as a main target.

Reach (可冲):

- <Robotics/automation journal one tier above the anchor> — indexing <SCIE, confirmed on Master Journal List> · <subscription, optional OA, APC from site> · speed <band + LetPub-reported first-decision time>.
  Official site: <journal-site URL opened>
  LetPub: <LetPub page URL opened>
  Recent related papers: <1-3 recent articles in this journal on LiDAR localization / point-cloud registration, with year + DOI/URL>.
  Fit: scope squarely in robotic perception/localization and recent contents show adjacent work; level slightly above the anchor, so a strong submission is plausible but not likely; satisfies SCIE.
  Adjust if borderline: strengthen the deployment claim with a quantitative degeneracy-handling comparison the venue's reviewers tend to expect.

Fast-review reach (审稿快的可冲):

- Often thin here. More selective robotics venues in this scope tend to review slowly (check the LetPub-reported times), so a robotics *letters* venue is usually the way to keep reach-level visibility with faster turnaround — consider submitting as a letter.
  Official site: <letters-venue URL> · LetPub: <URL>
  Recent related papers: <1-3 recent letter-format or short-communication articles in this topic area, with year + DOI/URL, or "no close recent match found">.

Safe (稳的):

- <Broad-scope indexed venue in sensors/measurement or applied robotics at the anchor level> — indexing <SCIE, confirmed> · <OA optional, APC from site> · speed <band + LetPub figure>.
  Official site: <URL> · LetPub: <URL>
  Recent related papers: <1-3 recent articles in this journal on sensor-based localization / mapping / registration, with year + DOI/URL>.
  Fit: scope covers sensor-based localization and recent contents show a recurring applied-sensing audience; level matches the anchor, so acceptance is more likely; satisfies SCIE.
  Adjust if borderline: foreground the sensing/measurement angle in the framing to match the venue's readership.

Fast-review safe (快速审稿稳的):

- <Large legitimate open-access venue in scope, DOAJ-listed> — indexing <confirm SCIE vs ESCI/Scopus-only> · <OA, APC from site — the main cost> · speed <band + LetPub figure, usually faster>.
  Official site: <URL> · LetPub: <URL>
  Recent related papers: <1-3 recent broad-scope articles close to the manuscript topic, with year + DOI/URL>.
  Fit: broad scope accepts sound, well-evaluated engineering work and recent contents include adjacent work; level at or below the anchor; fast turnaround suits the 2-month deadline.
  Caution: verified DOAJ listing and not on the CAS early-warning list; the APC can be substantial.

Red flags / cautions: none found during verification; the fast-review-safe candidate was checked against DOAJ and the CAS early-warning list.

Sources checked: official site + LetPub + recent related-paper evidence for every journal above; SCIE status on the Master Journal List; DOAJ for the OA candidate; CAS early-warning list screened.

Next step: pick one, then use paper-cover-letter.
