# Django Posts

Учебный проект, демонстрирующий :

* парсинг внешнего JSON‐API;
* хранение данных в PostgreSQL через Django ORM;
* собственные алгоритмы bubble‑sort и binary search;
* минимальный пользовательский интерфейс;
* раздел администрирования, разграничение доступа через пользователей и группы;
* контейнеризацию Docker.

---

## Содержание

1. [Быстрый старт](#быстрый-старт)
2. [Архитектура и структура каталогов](#архитектура-и-структура-каталогов)
3. [Работа с Docker](#работа-с-docker)
4. [Локальный запуск без Docker](#локальный-запуск-без-docker)
5. [Команда парсинга JSON](#команда-парсинга-json)
6. [Сортировка и поиск](#сортировка-и-поиск)
7. [Тестирование](#тестирование)
8. [Django‑admin и роли](#django-admin-и-роли)
9. [Переменные окружения](#переменные-окружения)
10. [Полезные шпаргалки](#полезные-шпаргалки)

---

## Быстрый старт

```bash
# 1. клонируем репозиторий
$ git clone https://github.com/<you>/django-posts.git
$ cd django-posts

# 2. запускаем docker‑compose
$ docker-compose up --build -d   # Windows

# 3. применяем миграции и загружаем демо‑данные
$ docker compose exec web python manage.py migrate
$ docker compose exec web python manage.py parse_data

# 4. создаём суперпользователя (для /admin/)
$ docker compose exec web python manage.py createsuperuser

# 5. откройте в браузере
http://localhost:8000/        # список постов
http://localhost:8000/admin/  # админ‑панель
```

⚙️ **По умолчанию** веб‑контейнер доступен на `:8000`, база — на `:5432`. Меняется в `docker-compose.yml`.

---

## Архитектура и структура каталогов

```text
django-posts/
├── Dockerfile              # образ «web» 
├── docker-compose.yml      # web + db(postgres)
├── .dockerignore           # игноры для сборки
├── manage.py
├── requirements.txt
├── django_posts/           # проект‑ядро
│   ├── __init__.py
│   ├── settings.py         # база, приложения
│   ├── urls.py             # корневые URL
│   └── wsgi.py
└── posts/                  # наше приложение
    ├── __init__.py
    ├── admin.py            # регистрация Post в админке
    ├── apps.py
    ├── models.py           # модель Post
    ├── utils.py            # bubble_sort, binary_search
    ├── views.py            # list & detail
    ├── urls.py             # /  и  /<pk>/
    ├── management/         # кастомные команды
    │   └── commands/
    │       └── parse_data.py
    ├── templates/
    │   └── posts/
    │       ├── list.html
    │       └── detail.html
    └── tests.py            # pytest‑тесты алгоритмов и view
```

---

## Работа с Docker

| Команда                        | Что делает                                                  |
| ------------------------------ | ----------------------------------------------------------- |
| `docker compose up -d`         | Собирает образы, поднимает контейнеры `web` и `db` в фоне.  |
| `docker compose logs -f web`   | Смотрит логи сервера Django.                                |
| `docker compose exec web bash` | Открывает shell внутри контейнера.                          |
| `docker compose down -v`       | Останавливает проект **и** удаляет том с БД (чистый старт). |

> На Windows с Docker Desktop ≤ 4.14 вместо `docker compose` используйте `docker-compose`.

---

## Локальный запуск без Docker

```bash
python -m venv .venv
. .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# SQLite по умолчанию
python manage.py migrate
python manage.py parse_data
python manage.py runserver
```

---

## Команда парсинга JSON

```bash
python manage.py parse_data [--url https://...] [--limit 100]
```

* по умолчанию скачивает `https://jsonplaceholder.typicode.com/posts` и сохраняет **100** записей;
* параметры `--url` и `--limit` позволяют загрузить другой источник или сократить объём.

Логика в `posts/management/commands/parse_data.py`.

---

## Сортировка и поиск

* **Поиск** — строка `q` в заголовке (`icontains`).
* **Сортировка** — query‑param `sort=id|title`.
* Алгоритмы из `posts/utils.py`:

  * `bubble_sort(sequence, key)` — классический пузырёк O(n²);
  * `binary_search(seq, target, key)` — показан в тестах.

Django‑QuerySet конвертируется в list, затем сортируется **в памяти**, удовлетворяя требование «свой алгоритм, не `order_by()`».

---

## Тестирование

```bash
docker compose exec web pytest -q
```

Покрытие:

* корректность `bubble_sort` и `binary_search`;
* HTTP‑ответы view‑функций (list/detail) с различными query‑параметрами.

---

## Django‑admin и роли

* Раздел **Posts**.
* Системные разделы **Users / Groups** позволяют:

  * создать группу `Editors` и назначить права `add/change/view_post`;
  * добавить пользователя `editor1` и включить его в группу;
  * входить под `editor1` (нужен `is_staff=True`).

> Права создаются автоматически миграциями (`add`, `change`, `delete`, `view`). При желании расширьте их в `Meta.permissions`.

---

## Переменные окружения

| Переменная          | По умолчанию      | Описание                                                                                                                 |
| ------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `DJANGO_SECRET_KEY` | `insecure-key`    | Секрет для сессий.                                                                              |
| `DEBUG`             | `1`               | Выключите (`0`) на боевом сервере.                                                                                       |
| `DATABASE_URL`      | см. `compose.yml` | Строка подключения; если указана, переопределяет настройки `DATABASES` в `settings.py` (используется `dj_database_url`). |

Отредактируйте `.env` (пример рядом) или прокиньте `-e` при запуске контейнера.


