# Cover Letter Guide

## Goal

Produce the letter that accompanies a journal submission: a short, factual, non-promotional message to the editor that states what is being submitted, why it fits the journal, and that the work meets originality and ethics expectations.

A cover letter is not a second abstract and not a sales pitch. It sells *fit and integrity*, not hype. It reuses contributions the manuscript already supports.

## Core Principle

```text
State the submission -> summarize the contribution honestly -> argue scope fit -> declare originality and ethics -> give contact details.
```

Two failure modes to avoid:

- inflation: the letter claims more novelty or superiority than the manuscript proves;
- fabrication: the letter asserts ethics facts, journal-scope details, or specifics (names, IDs, dates) that have not been confirmed.

## The Moves

Each move below gives its function, a concise form, a detailed form when relevant, and the placeholders to keep. All bracketed text is a placeholder to be filled by the user; never invent its content.

### Move 1 — Salutation and submission statement

Function: address the editor (or use a neutral salutation), then state the title, article type, and target journal.

Concise:

```text
Dear [Editor],

We would like to submit our manuscript titled "[Manuscript title]" to [Journal] for consideration as a [article type].
```

Notes:

- If the handling editor's name is unknown, "Dear Editor" or "Dear Editor-in-Chief" is acceptable; do not guess a name.
- The article type must match the journal's categories (for example, regular paper, brief, technical note). Leave `[article type]` if unsure.

### Move 2 — Core contribution

Function: state the problem, the approach, and the main result, at the manuscript's own claim strength.

Concise (single sentence):

```text
This paper presents [a method/framework] for [problem], which [main benefit] while [preserved property].
```

Detailed (mechanism and effect):

```text
This paper proposes [framework] for [target setting]. The approach [primary effect] while [guaranteed property]. By combining [mechanism 1] and [mechanism 2], it [improvement] relative to conventional approaches.
```

Hedging rule:

- For any novelty assertion, keep a qualifier such as "to the best of our knowledge".
- Tie comparative claims to the evaluated setting; do not generalize a tested result into unconditional superiority.

### Move 3 — Scope fit

Function: connect the work to the journal's aims and readership, naming the actual journal.

```text
We believe this work aligns well with the aims and scope of [Journal] and will be of interest to its readership.
```

Notes:

- Reference the real scope of the target journal. Do not assert a fit you cannot justify.
- If the user has not named the journal, leave `[Journal]` and flag that scope-fit cannot be specific yet.

### Move 4 — Originality and ethics declarations

Function: state the standard submission guarantees. These are factual claims; confirm with the user or leave placeholders.

```text
This manuscript has not been published previously and is not under consideration for publication elsewhere. All authors have approved the submission, and there are no conflicts of interest to declare.
```

Add when the journal requires them:

- funding or acknowledgement of support;
- data availability;
- ethics approval or consent (for human or animal studies);
- author-contribution or authorship-agreement statements.

Integrity rule:

- Do not assert any of these on the user's behalf. If unconfirmed, write a flagged placeholder such as `[Confirm: no competing interests]` and list it for the user.

### Move 5 — Optional statements

Use only if relevant:

- suggested reviewers: name, affiliation, email, and one line on relevance; avoid anyone with a conflict of interest;
- opposed reviewers: name and a brief, professional reason;
- related submissions: any concurrent or prior related work under review elsewhere;
- prior contact: a presubmission inquiry the editor already responded to.

### Move 6 — Corresponding-author details

```text
Please direct all correspondence regarding this manuscript to the corresponding author at [email].
```

### Move 7 — Closing

```text
Thank you for your time and consideration.

Best regards,
[Name], on behalf of all authors
```

## Length Registers

- Concise: salutation, one-sentence contribution, one-line scope fit, one-line declarations, contact, closing. Use for journals that prefer a short letter, or when the abstract already carries the detail.
- Detailed: expand the contribution into mechanism and effect, separate originality from ethics, and add a readership sentence. Use when the journal expects a fuller letter, or the contribution needs context to read as a fit.

Both registers keep the same claim strength. Length changes the detail, not the certainty.

## Placeholder Discipline

Always leave a placeholder, never a guess, for:

- editor name;
- journal name and article type;
- manuscript title and manuscript ID (for revisions);
- author names and corresponding-author email;
- dates;
- any ethics fact (competing interests, prior publication, concurrent submission, funding, data, approvals).

Collect every placeholder into a short list at the end of the draft so the user can fill them in one pass. Mark ethics-fact placeholders separately: only the authors can confirm them.

## Revision and Resubmission Letters

The cover note for a *revised* manuscript differs from a new-submission letter:

- it cites the manuscript ID and thanks the editor and reviewers;
- it states that a point-by-point response accompanies the revision;
- it does not reproduce the detailed responses themselves.

The detailed point-by-point reply to reviewer comments is handled by `paper-response-to-reviewers` (if available) and is out of scope for this skill.

## Tone

- Formal, concise, and restrained: the same objective register as the manuscript.
- No marketing language ("groundbreaking", "the first ever", "tremendous").
- Keep novelty hedged and comparisons bounded.
- For a final-language pass, hand the assembled letter to `paper-polisher`.

## Pre-Send Checklist

- Title, journal, and article type are correct or placeheld.
- The contribution summary does not exceed the manuscript's claims.
- Every novelty claim is hedged; every comparison is bounded.
- Scope-fit names the real target journal.
- Originality and ethics statements are confirmed by the user or left as flagged placeholders.
- No invented names, emails, IDs, or dates remain as if they were real.
- Optional reviewer suggestions carry no conflict of interest.
- Corresponding-author contact is present.
