# Наставнику
- Логин админки: boss_of_this_gym
- Пароль админки: VanDarkholm
- Email админки (для взаимодействия с api): darkh0lm@lalamail.com


# Foodgram
Данный проект является продуктовым помощником. Сайт предназначен для публикации рецептов и помощи пользователю с формированием и обработкой списков покупок на основе рецептов.

## Запуск проекта
1. В домашнюю папку проекта на сервере скопируйте папку frontend из репозитория, а также файл docker-compose.yml. Создайте папку nginx.conf и поместите туда файл nginx.conf, после чего переименуйте в default.conf
2. [Установите](https://docs.docker.com/engine/install/ubuntu/) на сервере Docker
3. Запустите сборку контейнеров командой `sudo docker-compose build`
4. Сделайте пуш репозитория на сервер с заполненными секретами в репозитории на Github или самостоятельно заполните ENV-файл со следующими переменными: DB_ENGINE, POSTGRES_DB DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT, DJ_SECRET_KEY
5. После сборки контейнеров с проектом перейдите в контейнер с бекендом `sudo docker-compose exec 
6. Проведите миграции в проекте, соберите статики и создайте суперпользователя следующим набором команд:

   - python manage.py migrate
   - python manage.py makemigrations api
   - python manage.py migrate api
   - python manage.py makemigrations users
   - python manage.py migrate users
   - python manage.py add_ingredients
   - python manage.py collectstatic
   - python manage.py createsuperuser

7. Перейдите в джанго-админку по эндпоинту /admin/ и создайте тэги для рецептов
8. Проект готов!

## Техническое описание проекта

### Сервисы проекта

 - **Главная страница** — содержит список первых шести рецептов, сортируемых по дате публикации от новых к старым. Страница имеет пагинацию в нижней части.
- **Страница рецепта** — содержит полное описание рецепта согласно модели. Авторизованные пользователи могут добавить рецепт в избранное и в список покупок, а также могут подписаться на автора рецепта.
- **Страница пользователя ** — содержит информацию о пользователе: имя, опубликованные рецепты, а также кнопку подписки (для авторизованных пользователей)
- **Подписка на авторов ** — подписка доступна лишь авторизованным пользователям с помощью кнопка «Подписаться на автора», притом только от себя и для себя. Авторизованным посетителям на странице подписок доступны рецепты, опубликованные авторами, на которых подписан пользователь, отсортированные по дате публикации (от новых к старым). В случае необходимости пользователи могут отказаться от подписки с помощью кнопки «Отписаться от автора».
- **Список избранного** — избранное доступно лишь авторизованным пользователям, работа со списком доступна лишь владельцу. Сценарии поведения пользователя:
а) Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
б) Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
в) При необходимости пользователь может удалить рецепт из избранного.
- **Список покупок** — покупки доступны только авторизованному пользователю, взаимодействие со списком доступно только владельцу.
Сценарии поведения пользователя:
а) Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
б) Пользователь переходит на страницу  **Список покупок**, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку  **Скачать список**  и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
в) При необходимости пользователь может удалить рецепт из списка покупок.

Список покупок скачивается в формате  _.txt.
При скачивании списка покупок ингредиенты в результирующем списке суммируются.

- **Фильтрация по тегам** — нажатие на тег выводит список рецептов, которые отмечены данным тегом. При активации нескольких тегов выводится список рецептов, содержащих хотя бы один тег.
Фильтрация по тегам на странице пользователя затрагивает лишь опубликованные этим пользователем рецепты. Фильтрация в избранном действует аналогично - только на избранное.
- **Регистрация пользователей** — реализована система создания и авторизации учетных записей для пользования проектом.
Для пользователей обязательны следующие поля:
а) Логин
б) Пароль
в) Email
г) Имя
д) Фамилия

Пользователи имеют три уровня доступа:
а) Анонимы (неавторизованные пользователи):
— Создание аккаунта
— Просмотр рецептов на главной странице
— Просмотр страниц рецептов
— Просмотр страниц пользователей
— Фильтрация рецептов по тегам
б) Авторизованные пользователи:
— Авторизация (вход под логином и паролем)
— Выход из системы (разлогин)
— Изменение пароля
— Создание, редактирование, изменение собственных рецептов
— Просмотр рецептов на главной странице
— Просмотр страниц рецептов
— Просмотр страниц пользователей
— Фильтрация рецептов по тегам
— Работа со списком избранного: добавление и удаление рецептов, просмотр страницы избранных рецептов
— Работа со списком покупок: добавление и удаление любых рецептов из базы, выгрузка файла в формате .txt для рецептов из списка покупок
— Подписка на авторов, просмотр страницы подписок и отмена подписок
в) Администраторы — обладают всеми правами авторизованного пользователя, а также:
— Изменение паролей любых аккаунтов
— Создание, удаление и бан любых аккаунтов
— Редактирование и удаление любых рецептов
— Добавление, удаление и редактирование ингредиентов
— Добавление, удаление и редактирование тегов

- **Админка**
Модели — выведены все модели с возможностью редактирования и удаления записей
— Пользователи: реализован фильтр списка по email и юзернейму
— Рецепты: выведены название и автор рецепта, реализован фильтр по автору. названию рецепта и тегам, на странице рецепта выведено общее количество отметок «В избранное» для рецепта
— Ингредиенты: выведены название ингредиента и единицы измерения, реализован фильтр по названию

### Инфраструктура проекта
Проект находится в репозитории foodgram-project-react
Foodgram использует базу данных PostgreSQL ( на момент разработки заменена SQLite)
Запускается в трех контейнерах через docker-compose на учебном сервере в Яндекс.Облаке.
Проект запушен на Docker Hub.
Список контейнеров:
- nginx
- PostgreSQL
- Django
Контейнер frontend используется только для подготовки файлов.

## Архитектура проекта

### backend
Содержит бэкенд проекта. Состоит из трех основных частей:
- **api**
Реализован API для всех моделей проекта, за исключением User и Follow, предназначенных для работы с аккаунтами и взаимодействий между ними по подпискам
- **foodgram**
Основная папка бэкенда. Здесь лежит корневой конфиг url-ов, настройки проекта, wsgi-файл
- **users**
Приложение, содержащее часть бэкенда, отвечающую за регистрацию и авторизацию пользователей, а также подписки.
### infra
Модуль, содержащий данные по корректному развертыванию проекта в Docker-контейнерах
### frontend
Содержит файлы фронтенда, необходимые для корректного отображения сервисов сайта на стороне клиента. Разработан отдельно, подключается с помощью nginx.
