# product/glossary.md Format (internal docs repo)

## Structure

The glossary is written in Russian. Each term carries its English name, which is the name used in code, API and database.

```md
# Глоссарий

Единый язык проекта: термины домена и их имена в коде. Подробности о поведении — в спецификации (`product/`).

## Контент

**Набор** (`Deck`):
Группа карточек для изучения, принадлежит ровно одной папке.
_Не говорим_: колода, сет, список

**Карточка** (`Flashcard`):
Пара «слово — перевод» с необязательными грамматическими атрибутами и примерами.
_Не говорим_: слово, запись

## Обучение

**Батч** (`Batch`):
Порция из 10 карточек, которую пользователь проходит за один подход внутри раунда.
_Не говорим_: страница, пачка
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Не говорим_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's domain.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this domain, or a general programming concept? Only the former belongs.
- **The English name is the code name.** If code uses a different identifier, that is a finding: surface it and ask which one should change.
- **Group terms under subheadings** when natural clusters emerge (content, learning, users and access).
