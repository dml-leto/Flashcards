Closes #

<!-- Issue number above. Auto-close on merge is disabled: "Closes" only links the PR to the issue and moves the card to In Review.
     PR title = squash commit title: `type: summary (FC-N)`, English, no scope. Types: CLAUDE.md, section 2. -->

## Что сделано

## Как проверить

## Чек-лист
<!-- Delete items that don't apply, or mark them N/A. -->
- [ ] Тесты добавлены или обновлены, сборка зелёная локально
- [ ] Изоляция по `owner_id` на каждом запросе и тест, что чужие данные недоступны (404)
- [ ] Миграции Flyway только новые, применённые не правились
- [ ] Ошибки API в формате Problem Details (RFC 9457)
- [ ] Нет секретов и паролей в коде, конфигах и истории коммитов
- [ ] Если изменилось правило — обновлён `CLAUDE.md`; если принято решение — документ в `docs/decisions/` и строка в индексе
