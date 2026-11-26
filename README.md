# РИТМ — курьерский парк

Независимый курьерский парк для пеших курьеров в Самаре.  
**Твой город. Твой маршрут. Твой доход.**

Сайт + админ-панель + Telegram-бот с deep-linking образуют единую систему привлечения и сопровождения курьеров.

## Возможности

- Заявка с сайта (имя, телефон, 18+, город, способ связи, согласие ПДн)
- Персональная ссылка Telegram (deep linking) после заявки
- Привязка Telegram ID к заявке (одноразовый токен, только хеш в БД)
- Меню бота: Моя заявка, Обучение, Яндекс Про, Связь с менеджером
- 10 статусов кандидата с уведомлениями в Telegram
- Админка: фильтры, поиск, история статусов, заметки, статистика
- Напоминания (endpoint для cron)
- Форма заявок по умолчанию **выключена** до заполнения реквизитов оператора

## Быстрый старт

```bash
git clone https://github.com/chernomorets2017-ops/ritm.git
cd ritm
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Админка: `/admin` (логин `admin`)

### Telegram-бот

1. @BotFather → токен
2. `.env`: TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_CHAT_ID, TELEGRAM_BOT_USERNAME, SITE_URL, SECRET_KEY
3. Админка → username бота
4. `python bot.py`

Полная документация в репозитории.
