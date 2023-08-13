# Сервис укорачивания ссылок YaCut

На большинстве сайтов адреса страниц довольно длинные. Делиться такими длинными ссылками не всегда удобно, 
а иногда и вовсе невозможно. Удобнее использовать короткие ссылки. Проект YaCut - это сервис укорачивания 
ссылок. Его назначение - ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам 
пользователь или предоставляет сервис.

### Технологии
* Python 
* Flask
* SQLAlchemy

### Как запустить проект:

+ Клонировать репозиторий и перейти в него в командной строке:

  ```
  git clone git@github.com:shusharkin/yacut.git
  ```

  ```
  cd yacut
  ```

+ Cоздать и активировать виртуальное окружение:

  ```
  python -m venv venv
  ```
  ```
  source venv/scripts/activate
  ```

* Установить зависимости из файла requirements.txt:

  ```
  python -m pip install --upgrade pip
  ```

  ```
  pip install -r requirements.txt
  ```

* Создать переменные окружения (файл yacut/.env). Пример заполнения файла:
  ```
  FLASK_DEBUG=True
  FLASK_APP=yacut
  FLASK_ENV=development
  DATABASE_URI=sqlite:///db.sqlite3
  SECRET_KEY=SECRET_KEY
  ```
* Применить миграции:

  ```
  flask db upgrade
    ```

* Запуск проекта:

  ```
  flask run
  ```

---


### Автор: [Шушаркин Герман](https://github.com/shusharkin)
