---
name: problem-driven-literature-review
description: Write, diagnose, revise, or audit literature review, related work, introduction background, research-gap, and reference-selection sections using a problem-driven S-R-L-H-G-M-C-V protocol. Use for claim-first citation selection, literature-route organization, hidden-assumption analysis, direct competitor coverage, structural gap synthesis, review-baseline alignment, contribution mapping, and citation integrity in technical research papers.
---

# Problem-Driven Literature Review

## Scope

Use this skill for literature review, related work, introduction background, research-gap synthesis, reference selection, and citation-role assignment in technical research papers, organized by a problem-driven protocol rather than a method-name list.

Read `references/literature_review_protocol.md` for the full protocol, worksheet, paragraph templates, reference-role table, reference metadata check, quality gates, and per-contribution-type examples before drafting or auditing a full review. For a short background paragraph, the principle and protocol summary below are enough.

Use another skill when the task is primarily:

- novelty risk, dangerous baselines, or whether the idea is defensible before writing: use `idea-novelty-auditor` (if available);
- manuscript storyline, section structure, contribution framing, or experiment-to-claim redesign: use `paper-argument-reconstructor` (if available);
- TeX-safe language polishing of the review text: use `paper-polisher` (if available).

## Verification Mode

This skill has two modes. By default it writes or revises the review as described above. When the input is a related-work or background section another tool or skill has already drafted, switch to verification mode instead of regenerating:

- do not overwrite the other tool's wording;
- check it against this skill's rules: citation integrity, reference metadata quality, direct-competitor coverage, negative-claim hygiene, and whether the named structural gap is actually supported;
- report only the deviations and their locations; fix one in place only if it breaks a hard rule.

The suite's value is faithful, bounded output, not a competing rewrite. Verify rather than replace what a stronger generator already produced.

## One-Sentence Principle

A literature review is not a list of what other people did. It should prove why the target paper is necessary:

```text
S requires R.
Literature L solves parts of R under H.
H breaks under S, producing gap G.
We propose C to close G and validate it by V.
```

## Core Protocol: S-R-L-H-G-M-C-V

| Step | Meaning | Question to answer |
|---|---|---|
| S | Scenario | What target task, environment, and constraints define the paper? |
| R | Requirements | What must a credible solution satisfy? |
| L | Literature lines | Which functional routes does prior work follow? |
| H | Hidden assumptions | What must be true for each route to work well? |
| G | Structural gap | Why do existing routes fail to jointly satisfy R? |
| M | Missing object | What concrete object (representation, mechanism, interface, theory, metric, benchmark, framework) is missing? |
| C | Contributions | Which gap component does each contribution address? |
| V | Validation | Which experiment, theorem, ablation, or benchmark validates each claim? |

G and M are distinct: **G is the capability that is jointly missing; M is the concrete object that supplies it.** Name M explicitly; an unnamed M is the most common review failure.

## Workflow

1. Infer the venue, paper type, contribution type, audience, review length, and available validation; ask at most one clarifying question, and only if it would change the structure.
2. Fill the minimum worksheet (S-R-L-H-G-M-C-V) before writing prose.
3. Organize literature by function and hidden assumptions, not by method name.
4. Compress limitations into one structural gap G, and name the missing object M.
5. Map each contribution C to a gap component, and each claim to a validation V.
6. Select references claim-first: write the claim, then find the reference, and give every reference a role.
7. If BibTeX entries are created, pasted from Google Scholar, or copied from another tool, run `scripts/check_references.py` on the `.bib` content before treating the entries as manuscript-ready. Use `--online` when DOI/Crossref verification is possible, and `--strict` when warnings should block final use.
8. Run the quality gates: direct-competitor coverage, negative-claim hygiene, review-experiment alignment, citation integrity, and reference metadata integrity.

Full tables, paragraph templates, the reference-role taxonomy, retrieval flow, reference metadata check, and per-contribution-type examples are in `references/literature_review_protocol.md`.

## Output

- For a full Related Work section: the review prose, plus the filled S-R-L-H-G-M-C-V worksheet and the reference-role list.
- For a diagnosis: the structural-gap sentence, the named missing object M, any uncovered direct competitors, and citation-integrity issues, then a revised structure.

Keep claims bounded: do not invent references, and do not use `nobody has done this` phrasing. Do not trust Google Scholar BibTeX as authoritative metadata; treat it as a draft export that must be checked against DOI, publisher, Crossref, DBLP, PubMed, arXiv, or the target journal style as appropriate. If recent-literature accuracy matters, verify with a search (e.g. WebSearch) or ask the user for the relevant reference set instead of asserting priority.
