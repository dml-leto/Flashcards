# Architecture Decision Records

Здесь фиксируются значимые архитектурные и продуктовые решения: что решили, почему и чем за это платим.
Формат — облегчённый [MADR](https://adr.github.io/madr/) (Michael Nygard).

## Правила
- Один файл = одно решение: `NNNN-kebab-case-title.md`, номера не переиспользуются.
- Принятый ADR не переписывается. Если решение меняется, пишется новый ADR со статусом `Supersedes NNNN`,
  а старому ставится `Superseded by NNNN`.
- Каждому ADR соответствует issue с меткой `type:decision` на GitHub.

## Реестр

| № | Решение | Статус | Issue |
|---|---|---|---|
| [0001](0001-frontend-framework.md) | Фронтенд: Vue 3 + TypeScript + Vite + PrimeVue, SPA на том же origin | Accepted | [#2](https://github.com/dml-leto/Flashcards/issues/2) |
| [0002](0002-authentication.md) | Аутентификация: серверная сессия (Spring Session JDBC) + HttpOnly cookie | Accepted | [#3](https://github.com/dml-leto/Flashcards/issues/3) |

## Шаблон

```markdown
# NNNN. Заголовок

- **Статус:** Proposed | Accepted | Superseded by NNNN
- **Дата:** YYYY-MM-DD
- **Issue:** #N

## Контекст
Какую проблему решаем, какие есть ограничения.

## Решение
Что выбрали, конкретно.

## Рассмотренные альтернативы
Вариант: почему не он.

## Последствия
Что станет проще, что сложнее, какие новые обязательства появляются.
```
