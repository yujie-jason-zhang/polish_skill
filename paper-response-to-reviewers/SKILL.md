---
name: paper-response-to-reviewers
description: Draft, plan, or diagnose a point-by-point response to reviewers (response letter / rebuttal) for a journal or conference revision, especially IEEE Transactions and control, robotics, automation, aerospace, and intelligent-systems venues. Use to audit the manuscript's claims, decode each comment's hidden concern, grade severity and required evidence, produce a revision plan before claiming any edit, revise and mark the manuscript, reconcile conflicting reviewers, handle multi-round revisions, and write the response letter with exact locations. Reuses the real revisions the authors made; defers final language polishing to paper-polisher.
---

# Paper Response to Reviewers

## Scope

For handling journal or conference reviewer comments, especially IEEE Transactions and control, robotics, automation, aerospace, and intelligent-systems venues.

This is not a "generate the reply letter directly" template. It is a full revision loop:

> understand the paper and the comments -> design the reply strategy -> revise the manuscript -> assess whether the revision suffices -> write the formal response letter -> verify locations and marked text

This skill produces the **revision plan and the response letter**. Editing the manuscript itself is higher-risk: have the user confirm manuscript edits, route structural rewrites to `paper-argument-reconstructor`, and final language to `paper-polisher`.

See `references/response_letter_guide.md` for the full severity/evidence grading, decision gates, conflicting-reviewer and multi-round handling, reply templates, and checklist. For a short reply, the core principles and rules below are enough.

Use another skill when the task is primarily:

- the short cover letter accompanying the submission (not the detailed replies): use `paper-cover-letter` (if available);
- restructuring an argument or section a reviewer attacked: use `paper-argument-reconstructor` (if available), then report the change here;
- final TeX-safe polishing of the reply text: use `paper-polisher` (if available).

## Verification Mode

This skill has two modes. By default it plans and writes the response as described above. When the input is a response letter another tool or skill has already drafted, switch to verification mode instead of regenerating:

- do not overwrite the other tool's wording;
- check it against this skill's rules: promised-change-to-manuscript consistency, evidence-based (not bluffed) rebuttals, softened overstatements, no S3/S4 concern answered with future work alone, and mutually consistent replies across reviewers;
- report only the deviations and their locations; fix one in place only if it breaks a hard rule.

The suite's value is faithful, bounded output, not a competing rewrite. Verify rather than replace what a stronger generator already produced.

## Core Principles

1. **Understand the paper before handling comments.** Identify its problem, method, theoretical assumptions, experimental support, core claims, and limitations.
2. **Design the reply strategy before revising.** Do not rewrite a comment directly into a reply.
3. **Every reply must correspond to a real manuscript change.** Do not fabricate experiments, proofs, figures, page numbers, sections, or marked edits.
4. **Close the loop on every substantive comment.**

Loop format:

> reviewer concern -> hidden concern -> revision strategy -> manuscript modification -> evidence check -> response letter -> exact location

Write each formal reply in five moves:

> quote the comment -> thank and state the position -> describe the concrete change -> give the reason it suffices -> point to the exact location (Section / Page / Eq / Fig / Table)

The position falls into one of five strategies (templates in the guide): accept-and-revise / partial accept (scope concession) / clarify or evidence-based rebuttal / added proof / added experiment.

## Non-Negotiable Rules

- **If the manuscript is not yet revised, output only a revision plan; never write "We have revised".**
- Do not fabricate experiments, proofs, figures, page numbers, sections, or marked edits; pointers must be real, or left as `[Section X, Page Y]` placeholders.
- Every "we have added/revised" in the letter must correspond to a real edit findable in the manuscript (reply-manuscript consistency).
- Rebut only with a technical reason or manuscript evidence; never bluff. A rebuttal that cannot give a reason becomes a clarification or a concession.
- When a reviewer flags an overstatement, soften the claim to what the evidence supports (a conditional certificate) rather than defending the stronger wording.
- Do not answer an S3/S4 substantive concern with future work alone; future work must pass the decision gate (see the guide).
- When reviewers conflict, never promise one reviewer a change and the other the opposite; the editor reads all replies together.
- Stay respectful and specific. Never write "the reviewer misunderstood"; write "our original presentation was not sufficiently clear".

## Rule-Conflict Escalation

If the user asks the reply to claim a change, a result, or a rebuttal the manuscript does not support, stop and ask before writing it. If your own draft drifts into an unsupported claim, an evidence-free rebuttal, a fabricated pointer, mutually inconsistent replies to different reviewers, or future work used to dodge an S3/S4 concern, revise it back without asking.

## Workflow (7 stages)

See `references/response_letter_guide.md` for the tables and examples.

1. **Understand the paper + claim audit.** Check contributions, assumptions, and evidence; flag overstatements in the abstract/introduction/conclusion; tone down high-risk words.
2. **Split and decompose the comments.** First separate the raw review material by editor / associate editor / reviewer and give every comment a stable ID (R1-C1, R1-C2, ...); then break each long comment into minimal units and identify the explicit request plus the hidden concern.
3. **Grade severity and required evidence.** Assign S0-S4 to each comment and match the required evidence strength E0-E5.
4. **Output the revision plan first.** Before the manuscript is edited, output only a revision plan (a planned-action table); do not write "revised".
5. **Revise the manuscript and mark the changes.** Each substantive comment maps to at least one manuscript action; mark per journal policy (blue / latexdiff / tracked changes / none).
6. **Assess sufficiency, and reconcile conflicts.** Check each change reaches the required evidence strength; where reviewers conflict, resolve the trade-off and keep the replies mutually consistent.
7. **Write the formal response letter.** Only after the edits are done, the locations confirmed, and the evidence sufficient; reply per comment in the five moves.

## Output Modes

- **Manuscript not finished** -> a revision plan (per comment: core concern / severity / required evidence / proposed action / needs user decision?); no final letter.
- **Manuscript finished** -> the final response letter (five moves per comment) plus a "promised change <-> manuscript location" check table, with `[confirm]` on anything unverified.
- **Diagnosing an existing draft** -> flag vague replies, evidence-free rebuttals, S3/S4 answered only with future work, reply-manuscript mismatches, conflicting replies, unsoftened claims, and disrespectful tone; then give a revised version.

For a long revision (several reviewers or many comments), output the response per reviewer rather than all at once, so each thread stays reviewable. For a second or later round, see the multi-round guidance in the guide.
