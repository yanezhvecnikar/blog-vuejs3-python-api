---

## 🏗 Архитектура проекта

                  ┌────────────────────────────────────┐
                  │            Пользователь            │
                  └────────────────────────────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │                               │
       ┌─────────▼─────────┐           ┌─────────▼─────────┐
       │  Веб‑сайт (dist)  │           │   Telegram‑бот    │
       │   (Nginx static)  │           │    (Aiogram 3)    │
       └─────────┬─────────┘           └─────────┬─────────┘
                 │                               │
                 └──────────────┬────────────────┘
                                ▼
                   ┌────────────────────────┐
                   │   FastAPI REST API     │
                   │  /api/projects         │
                   └───────────┬────────────┘
                               │
                     ┌─────────▼──────────┐
                     │   PostgreSQL DB    │
                     │  (projects table)  │
                     └────────────────────┘

- **Веб‑сайт** (dist) — отображает портфолио, статично отдаётся Nginx
- **Telegram‑бот** — показывает проекты, берёт их из PostgreSQL
- **FastAPI API** — CRUD‑доступ к проектам, единый источник данных
- **PostgreSQL** — хранит список проектов и их данные


---

## 🌐 Веб-сайт (dist)

Проект включает **фронтенд-сайт**, собранный в виде папки `dist`.  
Он может быть создан на **Vue.js**, **React** или любой другой фронтенд-технологии.

### 📦 Что внутри `dist`
- **index.html** — главная страница
- **assets/** — сжатые JS/CSS файлы
- **favicon.ico** — иконка сайта
- Медиа-файлы, используемые в проекте

### 🚀 Развёртывание сайта через Nginx
Чтобы сайт открывался по адресу `http://myserver.lock/`:

1. Скопируйте содержимое `dist` на сервер:
```bash
scp -r dist/* user@myserver:/var/www/html/

# 🚀 Telegram Portfolio Bot + FastAPI API

Этот проект — это **Telegram-бот портфолио** с административной панелью и REST API на **FastAPI**, с хранением данных в **PostgreSQL**.  
Он позволяет:
- Просматривать список проектов прямо в Telegram
- Сохранять проекты в базе данных
- Добавлять/удалять проекты через **админку бота**
- Добавлять проекты через **FastAPI** (удобно для веб-админки или интеграций)
- Разворачивать на сервере с помощью **Nginx** и **systemd**

---

## 📦 Стек технологий
- **Python 3.12**
- **Aiogram 3** — Telegram-бот
- **FastAPI** — REST API
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Pydantic v2** — схемы данных
- **Nginx** — обратный прокси
- **Systemd** — автозапуск бота и API

---

[Unit]
Description=FastAPI app
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/blog-vuejs3-python-api/app
ExecStart=/root/blog-vuejs3-python-api/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

[Unit]
Description=Telegram Bot
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/blog-vuejs3-python-api/bot
ExecStart=/root/blog-vuejs3-python-api/.venv/bin/python bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target

server {
    listen 80;
    server_name euorik.com www.euorik.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name euorik.com www.euorik.com;

    ssl_certificate /etc/letsencrypt/live/euorik.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/euorik.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    root /var/www/euorik.com/html;
    index index.html;

    # Vue SPA поддержка
    location / {
        try_files $uri /index.html;
    }

    # Проксирование API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}