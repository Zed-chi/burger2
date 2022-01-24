# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.
Состоит из:
* Первый — публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.
* Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. 
* Третий интерфейс — это админка.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Требования:
* python >= 3.7
* node.js >= 12
* Cоздать файл `.env` в корне проекта со следующими настройками:

- `DEBUG` — дебаг-режим. Поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте. Не стоит использовать значение по-умолчанию, **замените на своё**.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `rollbar_token` - ключ для rollbar сервиса
- `rollbar_env` - название окружения для удобства просмотра в rollbar
- `psql_login` - логин юзера базы данных
- `psql_pass` - пароль юзера базы данных
- `psql_db` - навание базы данных 

Запуск:

* pip install -r requirements.txt
* npm install --dev

Собрать фронтенд parcel-ом:
* npm install -g parcel@latest  # установка
* parcel build bundles-src/index.js --dist-dir bundles --public-url="./" # сборка

Если проблема с parcel то можно установить esbuild и собрать командой:
* npm install -g esbuild # установка
* esbuild ./bundles-src/index.js --bundle --loader:.png=file --loader:.js=jsx --outdir=bundles # сборка

* python manage.py migrate
* python manage.py runserver


## Информация по уже развернутому проекту:

В корне проекта находится файлик deploy.sh который:
* Обновит код репозитория
* Установит библиотеки для Python и Node.js
* Пересоберёт JS-код
* Пересоберёт статику Django
* Накатит миграции
* Перезапустит сервисы Systemd
* Сообщит об успешном завершении деплоя

Сервер расположен по адресу [color-burgers.ru](https://color-burgers.ru)
Для входа по ssh:
    ip: 5.101.51.211
    


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного модуля Django](https://dvmn.org/modules/django/)
