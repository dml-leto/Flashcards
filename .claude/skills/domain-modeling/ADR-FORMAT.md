# ADR Format

Decisions live in `docs/decisions/`. The rules, the index and the template are in `docs/decisions/README.md`: read it before writing and follow it exactly. In short:

- One decision = one file `fc-<N>-adr-<slug>.md`, where `FC-<N>` is the GitHub issue the decision was made in. Non-architecture decisions drop `adr-`.
- The title starts with the ID: `# FC-<N> · ADR: Title`.
- The document is written in Russian; the slug is English kebab-case.
- An accepted decision is never rewritten. A change is a new document with `Supersedes FC-<N>`, and the old one gets `Superseded by FC-<M>`.
- Adding the row to the index in `docs/decisions/README.md` is part of the same change.

If there is no `type:decision` issue for this decision yet, propose creating one instead of writing the document straight away.

Keep the document as short as the decision allows. The value is in recording *that* a decision was made and *why*, not in filling out sections. "Considered alternatives" is worth writing only when the rejected options are worth remembering.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it: you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "Learning Engine lives in `card-core` and is `internal`."
- **Integration patterns between modules.** "Background work goes through a transactional outbox with `SKIP LOCKED`, not Kafka."
- **Technology choices that carry lock-in.** Database, message bus, auth approach, deployment target. Not every library: just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "A deck belongs to exactly one folder." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "Accounts are created by a migration; there is no sign-up."
- **Rejected alternatives when the rejection is non-obvious.** If you considered JWT and picked server sessions for subtle reasons, record it; otherwise someone will suggest JWT again in six months.
