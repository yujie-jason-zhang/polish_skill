---
name: paper-cover-letter
description: Draft, revise, or diagnose an academic journal cover letter (submission letter to the editor) once the manuscript is essentially complete. Use for the submission statement, a non-overclaiming contribution summary, scope-fit argument for the target journal, originality and ethics declarations, suggested or opposed reviewers, and corresponding-author details. Reuse the manuscript's established problem and contributions instead of inventing them; defer final language polishing to paper-polisher.
---

# Paper Cover Letter

## Scope

Use this skill when the manuscript is essentially complete and the user needs the letter that accompanies a journal submission: a new submission, a resubmission, or the cover note for a revised manuscript.

Read `references/cover_letter_guide.md` for move-by-move templates, length registers, placeholder rules, and the declaration block before drafting a full letter. For a one-line tweak, the core rules below are enough.

Use another skill when the task is primarily:

- a point-by-point response to reviewer comments or a rebuttal: use `paper-response-to-reviewers` (if available); that is a separate task, not a cover letter;
- manuscript storyline, contribution framing, or section structure: use `paper-argument-reconstructor` (if available) to settle the contributions first;
- TeX-safe or final-language polishing of the letter text: use `paper-polisher` (if available) for the closing pass;
- novelty-risk auditing of the underlying idea: use `idea-novelty-auditor` (if available).

A cover letter reuses contributions that the manuscript already supports. It does not establish new ones.

## Verification Mode

This skill has two modes. By default it drafts the letter as described above. When the input is a cover letter another tool or skill has already drafted, switch to verification mode instead of regenerating:

- do not overwrite the other tool's wording;
- check it against this skill's rules: no overclaiming, novelty kept hedged, ethics statements treated as facts to confirm rather than assumed, and placeholders for every unconfirmed specific;
- report only the deviations; fix one in place only if it breaks a hard rule.

The suite's value is faithful, bounded output, not a competing rewrite. Verify rather than replace what a stronger generator already produced.

## Non-Negotiable Rules

- Do not invent contributions, results, novelty, or journal-scope claims that the manuscript or the user does not support.
- Treat every originality and ethics statement as a factual claim: no prior publication, no concurrent submission, all-author approval, conflict-of-interest status, funding, and data availability. Do not assert these on the user's behalf. Insert them only when the user confirms them; otherwise leave an explicit `[...]` placeholder and flag it.
- Do not overclaim. Keep novelty hedged (for example, "to the best of our knowledge") and tie any superiority to the evaluated conditions, mirroring the manuscript's own claim boundaries.
- Leave every unconfirmed specific as a `[...]` placeholder: editor name, journal name, manuscript ID, article type, author names, emails, and dates. Do not fabricate them.
- Preserve the manuscript's terminology and claim strength. The letter must not promise more than the paper delivers.

## Rule-Conflict Escalation

If the user asks the letter to assert an ethics fact, a novelty claim, or a scope-fit statement that the source does not support, stop and ask before writing it. If your own draft drifts into overclaiming, revise it back into bounded language without asking.

## Workflow

1. Confirm the target journal, manuscript title, article type, and submission stage (new, resubmission, or revision).
2. Pull the core problem and contributions from the manuscript or from `paper-argument-reconstructor` output. Do not re-derive or inflate them.
3. Choose a length register: concise (a few sentences) or detailed (mechanism, effect, and readership). Default to the journal's norm or the user's preference.
4. Assemble the moves in order, inserting a placeholder for every unconfirmed fact.
5. Run the pre-send check: no overclaim, ethics statements confirmed or placeheld, scope-fit naming the actual journal, no fabricated specifics.
6. If the user wants a final language pass, hand the assembled letter to `paper-polisher`.

## Cover Letter Moves

Summary only; see `references/cover_letter_guide.md` for templates.

1. Salutation and submission statement: title, article type, target journal.
2. Core contribution: problem, approach, and main result, hedged.
3. Scope fit with the target journal and its readership.
4. Originality and ethics declarations: confirmed or placeheld.
5. Optional: suggested or opposed reviewers, related or concurrent submissions, prior editorial contact.
6. Corresponding-author correspondence details.
7. Closing.

Moves 3 and 4 may swap order. Keep whichever order the target journal expects.

## Output Modes

For a new draft, return:

1. The letter, with an explicit `[...]` placeholder for every unconfirmed fact.
2. A short list of the placeholders the user must fill, marking which are ethics facts that only the authors can confirm.

For diagnosis of an existing letter, return:

1. Overclaims and unsupported novelty or scope assertions.
2. Missing or unconfirmed ethics declarations.
3. Structural gaps against the standard moves.
4. A revised version that keeps claims bounded.

For a letter that must be returned paste-ready, run a final `paper-polisher` pass if available.
