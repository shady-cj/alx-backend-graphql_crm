# CRM Celery + Celery Beat Setup Guide

This document explains how to set up and run **Celery** and **Celery Beat** in the Django CRM project.

---

## 1️⃣ Install Redis and Dependencies

### 🧱 Option A — Using Redis on Local Machine
- **Windows (via WSL or Docker):**
  ```bash
  wsl
  sudo apt update
  sudo apt install redis-server
  sudo service redis-server start
  ```

- **macOS (Homebrew):**
  ```bash
  brew install redis
  brew services start redis
  ```

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update
  sudo apt install redis-server
  sudo systemctl enable redis-server
  sudo systemctl start redis-server
  ```

Confirm Redis is running:
```bash
redis-cli ping
# → PONG
```

### 🧩 Install Python Dependencies
Inside your virtual environment:

```bash
pip install "celery[redis]" django-celery-beat
```

---

## 2️⃣ Run Django Migrations

Make sure your database is ready and apply migrations:

```bash
python manage.py migrate
```

For `django-celery-beat` (stores periodic tasks in DB):

```bash
python manage.py migrate django_celery_beat
```

---

## 3️⃣ Start Celery Worker

Run the Celery worker to process background jobs:

```bash
celery -A crm worker -l info
```

### Optional (Advanced)
- You can adjust concurrency:
  ```bash
  celery -A crm worker -l info --concurrency=4
  ```
- To write logs to a file:
  ```bash
  celery -A crm worker -l info --logfile=/tmp/crm_report_log.txt
  ```

---

## 4️⃣ Start Celery Beat (Scheduler)

Start Celery Beat to manage periodic tasks:

```bash
celery -A crm beat -l info
```

Or log output to file:

```bash
celery -A crm beat -l info --logfile=/tmp/crm_report_log.txt
```

---

## 5️⃣ Verify Logs and Task Execution

Monitor task execution by tailing the log file:

```bash
tail -f /tmp/crm_report_log.txt
```

You should see messages like:
```
[2025-10-30 21:10:34,123: INFO/MainProcess] Received task: crm.tasks.generate_report[abcd1234]
[2025-10-30 21:10:35,456: INFO/ForkPoolWorker-1] Task crm.tasks.generate_report[abcd1234] succeeded in 1.23s
```

---

## 6️⃣ Common Commands

| Purpose | Command |
|----------|----------|
| Run worker | `celery -A crm worker -l info` |
| Run beat scheduler | `celery -A crm beat -l info` |
| Run both (dev only) | `celery -A crm worker -B -l info` |
| Clear all Celery tasks | `celery -A crm purge` |
| Check Redis connection | `redis-cli ping` |

---

## 7️⃣ Notes & Best Practices

- Always run **worker** and **beat** as separate processes in production.
- Ensure `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` in `.env` point to Redis.
- Logs are stored in `/tmp/crm_report_log.txt` by default (adjust as needed).
- You can monitor tasks via **Flower** (`pip install flower`):
  ```bash
  celery -A crm flower
  ```

---

**✅ Your Celery setup is now complete!**

```
🚀 Worker running: celery -A crm worker -l info  
🕒 Scheduler running: celery -A crm beat -l info  
🧠 Logs available at: /tmp/crm_report_log.txt
```
