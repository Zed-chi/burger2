# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.
Состоит из:

- Первый — публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.
- Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов.
- Третий интерфейс — это админка.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)

Требования:

- python >= 3.7
- node.js >= 12
- Cоздать файл `.env` в корне проекта со следующими настройками:

* `DJANGO_CONFIGURATION` - ["Dev"/"Prod"/"ProdPostgres"]
* `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте. Не стоит использовать значение по-умолчанию, **замените на своё**.
* `ROLLBAR_TOKEN` - ключ для rollbar сервиса
* `ROLLBAR_ENV` - название окружения для удобства просмотра в rollbar
* `PG_DB_NAME` - логин юзера базы данных (в случае конфигурации ProdPostgres)
* `PG_USER` - пароль юзера базы данных (в случае конфигурации ProdPostgres)
* `PG_PASS` - навание базы данных (в случае конфигурации ProdPostgres)
* `MY_HOST` - доменное имя

# Запуск:

- pip install -r requirements.txt
- npm install --dev

### Собрать фронтенд parcel-ом:

- npm install -g parcel@latest # установка
- parcel build bundles-src/index.js --dist-dir bundles --public-url="./" # сборка

Если проблема с parcel то можно установить esbuild и собрать командой:

- npm install -g esbuild # установка
- esbuild ./bundles-src/index.js --bundle --loader:.png=file --loader:.js=jsx --outdir=bundles # сборка

###

- python manage.py migrate
- python manage.py runserver

### Для Работы Postgres

Установить:
`sudo apt-get update`
`sudo apt-get install libpq-dev postgresql postgresql-contrib`

#### Создать базу и пользователя:

`sudo su - postgres`
Войти в оболочку дб
`>>psql`

```
    CREATE DATABASE <имя базы>;
    CREATE USER <имя пользователя> WITH PASSWORD 'пароль';
    GRANT ALL PRIVILEGES ON DATABASE <имя базы> TO <имя пользователя>;
    \q
    exit
```

Найти файл pg_hba.conf:
`find / -name pg_hba.conf 2>/dev/null`
Заменить:
`host    all     postgres   peer` На `host    all     postgres      md5`
Перезагрузить:
`sudo service postgresql reload`

## Информация по уже развернутому проекту:

#### SSL

Certbot не работает, поэтому был выбран [acme-nginx](https://github.com/kshcherban/acme-nginx#usage), с ним проблем нет.
Обновление определено в `cert_renewal.service` и `cert_renewal.timer`

В корне проекта находится файлик deploy.sh который:

- Обновит код репозитория
- Установит библиотеки для Python и Node.js
- Пересоберёт JS-код
- Пересоберёт статику Django
- Накатит миграции
- Перезапустит сервисы Systemd
- Сообщит об успешном завершении деплоя

Сервер расположен по адресу [color-burgers.ru](https://color-burgers.ru)
Для входа по ssh:
ip: 5.101.51.211

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного модуля Django](https://dvmn.org/modules/django/)
