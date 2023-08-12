# Проект: recipe_savor

---
- domain - https://recipesavor.ddns.net/
- admin name - admin
- admin password - recipesavor
- admin email - admin@admin.ru


### Стек:
Python, Django, Django REST Framework, Djoser, Node.js, React, Gunicorn, Nginx, Docker, GitHub Actions

---

### Описание:

**recipe_savor** — это платформа, которая соединяет любителей кулинарии. Здесь пользователи могут делиться своими уникальными рецептами, находить вдохновение в блюдах других пользователей, а также скачивать игредиенты понравившихся рецептов. Удобный функционал подписок позволяет быть в курсе последних кулинарных тенденций и не упустить ни одного интересного рецепта..

---

### Как развернуть проект локально:

1. Клонировать репозиторий:
```bash
	git@github.com:CHEDEIV8/recipe_savor.git
	cd infra/
```
2. Создать в папке infra/ файл **.env** с переменными окружения (см. [.env.example](.env.example)).

3. Собрать и запустить докер-контейнеры через Docker Compose:
```bash
	docker compose up --build
```
4. После окончания сборки контейнеров перейдите в папку infra выполнить следующие команды:
```
docker-compose exec python manage.py migrate # Выполнить миграции
docker-compose exec python manage.py createsuperuser # Создать суперпользователя
```
---
### Как развернуть проект на серверe:
1. Создать папку recipesavor/ с файлом .env в домашней директории сервера и заполнить его по образцу (см. [.env.example](.env.example)). 
```bash
	cd ~
	mkdir recipesavor
	nano recipesavor/.env
```

2. Cкопировать папку dosc и data в домашную директорию сервера
```bash
rsync -avz -e ssh /путь/к/локальной/папке/data user@удаленный_сервер:/путь/на/удаленном/сервере/
rsync -avz -e ssh /путь/к/локальной/папке/docs user@удаленный_сервер:/путь/на/удаленном/сервере/
```

3. Установить на сервере Docker, Docker Compose:
```bash
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```
4. Настроить в nginx перенаправление запросов на порт 7000:
```nginx
    server { 
    	server_name <...>; 
    	server_tokens off;
    	location / { 
    		proxy_pass http://127.0.0.1:7000; 
    	}
    }
```
5. Запустить certbot для получения SSL-сертификата и перезапустить nginx :
```bash
sudo certbot --nginx
sudo systemctl reload nginx 
```

 
6. Добавить в GitHub Actions следующие секреты:
```
DOCKER\_USERNAME - логин от Docker Hub
DOCKER\_PASSWORD - пароль от Docker Hub
SSH\_KEY - закрытый ssh-ключ для подключения к серверу
SSH\_PASSPHRASE - passphrase от этого ключа
USER - имя пользователя на сервере
HOST - IP-адрес сервера
TELEGRAM\_TO - ID телеграм-аккаунта для оповещения об успешном деплое
TELEGRAM\_TOKEN - токен телеграм-бота
```
---

### Об авторе

Автор проекта: **Денис Чередниченко**
