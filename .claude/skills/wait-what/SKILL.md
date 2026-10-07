---
name: wait-what
description: "Stop. That last message did not land: re-pitch it."
disable-model-invocation: true
---

Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, answer in plain Russian with short sentences (one idea per sentence, no unexplained jargon), and use the ubiquitous language from the glossary `<internal docs repo>/product/glossary.md` (location: CLAUDE.md) if it exists.

Established industry terms stay in English: never transliterate or translate them away. Write `API`, `endpoint`, `outbox`, `idempotency`, not «АПИ», «эндпоинт», «аутбокс». If a Russian word helps understanding, add it next to the English term, e.g. «idempotency (идемпотентность)», never instead of it.
