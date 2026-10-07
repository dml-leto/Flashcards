---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing domain terminology, writing or editing the glossary <internal docs repo>/product/glossary.md (location: CLAUDE.md), or recording or editing a decision in docs/decisions/.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `<internal docs repo>/product/glossary.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

This project has a single context, split between this public repo and the private internal docs repo (location: CLAUDE.md):

```
public repo /
├── CLAUDE.md                ← roles and process; overrides this skill on conflict
└── docs/decisions/
    ├── README.md            ← rules, index and template for decisions
    └── fc-<N>-[adr-]<slug>.md

<internal docs repo>/
└── product/
    ├── README.md            ← table of contents for product/
    ├── glossary.md          ← ubiquitous language (Russian, with English code names)
    └── *.md                 ← primary sources: product overview, feature spec
```

Create `<internal docs repo>/product/glossary.md` (location: CLAUDE.md) lazily: only when the first term is resolved. When you create it, update `<internal docs repo>/product/README.md`.

The terms in the spec files in `<internal docs repo>/product/` are the starting point. If the glossary and the spec disagree, surface it and ask which one is right.

## Who decides

The user makes every domain and architecture decision (see `CLAUDE.md`, section 0). You challenge, propose and recommend. Write the glossary or a decision only after the user's explicit "yes" to the exact entry.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `<internal docs repo>/product/glossary.md`, call it out immediately. "The glossary defines 'Round' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'set': do you mean the Deck or the Batch? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code moves only wrong cards to the next batch, but you just said skipped cards move too. Which is right?"

### Update the glossary as terms resolve

When a term is resolved, show the proposed entry and write it to `<internal docs repo>/product/glossary.md` right after the user confirms. Don't batch these up until the end of the session: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`<internal docs repo>/product/glossary.md` should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer decision records sparingly

Only offer to record an architecture decision (ADR) when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
