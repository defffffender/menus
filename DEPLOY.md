# Деплой Menus на VPS (Ubuntu 22.04/24.04)

Схема: **nginx** (HTTPS, отдаёт static/media) → **daphne** (ASGI: HTTP + WebSocket)
под **systemd**. БД — SQLite по умолчанию или PostgreSQL. Пути в примерах: код в
`/opt/menus`, системный пользователь `menus`.

> Секреты (SECRET_KEY, пароли, Eskiz, БД) задаются только в `/opt/menus/.env` на
> сервере. В git и в переписку их не вносим.

---

## 1. Подготовка сервера

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip git nginx
# по желанию: PostgreSQL и Redis
# sudo apt install -y postgresql redis-server
```

Создать пользователя и каталог:

```bash
sudo adduser --system --group --home /opt/menus menus
sudo mkdir -p /opt/menus && sudo chown menus:menus /opt/menus
```

## 2. Код и зависимости

```bash
sudo -u menus git clone https://github.com/defffffender/menus.git /opt/menus
cd /opt/menus
sudo -u menus python3 -m venv venv
sudo -u menus venv/bin/pip install -r requirements.txt
```

## 3. Конфигурация (.env)

```bash
sudo -u menus cp .env.example .env
sudo -u menus python venv/bin/python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
sudo -u menus nano /opt/menus/.env
```

Минимум для прода:

```ini
DEBUG=False
SECRET_KEY=<сгенерированный выше>
ALLOWED_HOSTS=menu.example.uz,www.menu.example.uz
CSRF_TRUSTED_ORIGINS=https://menu.example.uz,https://www.menu.example.uz
# пока нет HTTPS (до certbot) — иначе будет редирект-петля:
SECURE_SSL_REDIRECT=False
# SMS
ESKIZ_ENABLED=True
ESKIZ_EMAIL=...
ESKIZ_PASSWORD=...
# PostgreSQL (опционально):
# DATABASE_URL=postgres://menus:ПАРОЛЬ@127.0.0.1:5432/menus
# Redis для realtime между воркерами (опционально):
# REDIS_URL=redis://127.0.0.1:6379/0
```

(Если PostgreSQL) создать БД:

```bash
sudo -u postgres psql -c "CREATE USER menus WITH PASSWORD 'ПАРОЛЬ';"
sudo -u postgres psql -c "CREATE DATABASE menus OWNER menus;"
```

## 4. Миграции, суперюзер, статика

```bash
cd /opt/menus
sudo -u menus venv/bin/python manage.py migrate
sudo -u menus venv/bin/python manage.py createsuperuser
sudo -u menus venv/bin/python manage.py collectstatic --noinput
```

## 5. systemd (daphne)

```bash
sudo cp /opt/menus/deploy/menus.service /etc/systemd/system/menus.service
sudo systemctl daemon-reload
sudo systemctl enable --now menus
sudo systemctl status menus      # должен быть active (running)
```

## 6. nginx

```bash
sudo cp /opt/menus/deploy/nginx-menus.conf /etc/nginx/sites-available/menus
# в файле заменить menu.example.uz на ваш домен:
sudo nano /etc/nginx/sites-available/menus
sudo ln -s /etc/nginx/sites-available/menus /etc/nginx/sites-enabled/menus
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

## 7. Домен и HTTPS

1. В DNS-панели домена добавить **A-запись** на IP сервера (для `@` и `www`).
2. Дождаться распространения DNS, затем выпустить сертификат:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d menu.example.uz -d www.menu.example.uz
```

3. После выпуска TLS включить редирект на HTTPS:

```bash
sudo -u menus sed -i 's/^SECURE_SSL_REDIRECT=False/SECURE_SSL_REDIRECT=True/' /opt/menus/.env
sudo systemctl restart menus
```

Готово — сайт работает по `https://menu.example.uz`.

## 8. Проверка SMS

```bash
cd /opt/menus
sudo -u menus venv/bin/python manage.py eskiz_test +998901234567
```

(Сработает только после одобрения текстов на модерации Eskiz.)

---

## Обновление после изменений в коде

```bash
cd /opt/menus
sudo -u menus git pull
sudo -u menus venv/bin/pip install -r requirements.txt
sudo -u menus venv/bin/python manage.py migrate
sudo -u menus venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart menus
```

## Полезные команды

```bash
sudo journalctl -u menus -f         # логи приложения (в т.ч. SMS)
sudo systemctl restart menus        # перезапуск
sudo nginx -t && sudo systemctl reload nginx
```
