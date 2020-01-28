# DreamTeam-Test-Assignment

Я срезал несколько углов, потому что понимаю, что уже затратил много времени на это задание, но при этом я поработал над новыми для себя вещами, и это круто.

## Пререквизиты

В первую очередь, Python 3.7+. Список использованных модулей я заморозил в requirements.txt.

Я использовал установленную системно базу данных PostgreSQL. При помощи PGAdmin была создана база данных "sn_server_db" и роль "sn_server_user" с паролем "123" (задание ведь тестовое). Роли даны все права по изменению этой базы данных.

Для проверки работы API я использовал [Postman](https://www.getpostman.com/).

## Структура проекта

Структура типична для Django в целом и Django REST framework в частности.

### Эндпоинты API

Всё взаимодействие с сервером происходит посредством передачи данных в формате JSON через API. Базовый адрес каждого эндпоинта - "http://localhost:8000/api/".

#### /allusers/

При помощи GET мы получим список всех существующих пользователей, на случай, если нам нужно что-то проверить.

#### /allgroups/

При помощи GET мы получим список всех существующих групп, на случай, если нам нужно что-то проверить.

#### /auth/registration/

##### POST

Создание нового пользователя. Нужно отправить POST-запрос с данными, например:

```
{
    "email":"test@test.test"
    "username":"Suncake",
    "password":"qwerty"
}
```

Запрос возвращает "token", который затем следует использовать для любых требующих авторизации запросов.

#### /auth/login/

##### POST

Здесь мы логинимся в существующего пользователя. Передаём либо username и password, либо email и password:

```
{
    "username":"Suncake",
    "password":"qwerty"
}
```

Запрос возвращает "token", который затем следует использовать для любых требующих авторизации запросов.

#### /user/<id>

Работа с профилями пользователей.

##### GET

Подставляем нужный id и получаем данные о пользователе, за исключением пароля и имейла.

##### PATCH

Редактируем профиль пользователя, передавая JSON, но только если запрос прислан самим пользователем. Также можно передать изображение под ключом "avatar". Все поля опциональны.

```
{
    "first_name":"Никита",
    "second_name":"Зотов",
    "nickname":"Suncake",
    "birth_date":"02/06/1994"
    "info":"Вставить глубокую мысль с многоточием в конце...",
    "avatar":"Какое-то изображение, загруженное через форму"
}
```
#### /user/<id>/friendship/
  
##### POST

Здесь мы создаём дружбу и добавляем пользователей в друзья друг другу. Согласие получателя при этом не требуется.

##### DELETE

А здесь дружба рушится. Тоже в одностороннем порядке.

#### /group/<id>
  
##### POST

Здесь не нужно никаких id - создаётся новая группа, айди присваивается автоматически. Отправляем JSON с данными, также можно передать изображение под ключом "avatar". Администратор - пользователь, от имени которого подан запрос.

```
{
    "name":"A Piece of Cake",
    "description":"A Warframe clan and Discord community",
    "avatar":"Какое-то изображение, загруженное через форму"
}
```

##### PATCH

Редактируем данные группы. Сработает, только если запрос идёт от админа группы. Передаём JSON с обновлённой информацией. Все поля опциональны.


```
{
    "name":"A Piece of Cake",
    "description":"A Warframe clan and Discord community",
    "administrator":321 # id нового админа
    "avatar"="Какое-то изображение, загруженное через форму"
}
```

##### DELETE

Группа удаляется. У всех пользователей она удаляется каскадом.

#### /group/<id>/membership/
  
##### POST

Тот же принцип, что и с дружбой - создаётся членство в группе.

##### DELETE

Пользователь выходит из группы.

