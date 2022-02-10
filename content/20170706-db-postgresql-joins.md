Title: Выборка данных из нескольких таблиц (JOIN)
Category: Blog
Tags: SQL, Postgresql, DB, database, INNER JOIN

Задача: получить полный адрес покупателя.

Вспомним, что информация о покупателяx после нормализации находится теперь в 
5 -ти разных таблицах.

![db_person.png]({static}/images/db_person.png)

Содержимое таблиц выглядит так:

```
haircolors=# select * from person ;
 person_id | firstname | lastname | phonenumber  | address_id 
-----------+-----------+----------+--------------+------------
         1 | Денис     | Петров   | +79784567897 |          1
         2 | Юлия      | Бабкина  | +79784168585 |          2
(2 rows)

haircolors=# select * from address ;
 id | building | flat_no |         street          | city_id 
----+----------+---------+-------------------------+---------
  1 |       77 |      54 | ул. Александра Косарева |       1
  2 |        1 |      55 | ул. Кесаева             |       1
(2 rows)
```
```
haircolors=# select * from city;
 city_id |  city_name  
---------+-------------
       1 | Севастополь
(1 row)
```
```
haircolors=# select * from zip_code_catalog ;
         street          | zip_code 
-------------------------+----------
 ул. Александра Косарева |   299006
 ул. Кесаева             |   299003
(2 rows)
```
```
haircolors=# select * from zip_code;
 zip_code 
----------
   299006
   299003
(2 rows)
```

Для того чтоб получить информацию воспользуемся INNER JOIN:

```postgresql
SELECT person_id, 
       firstname,
       lastname,
       phonenumber,
       a.street,
       building, 
       a.flat_no, 
       zip_code, 
       city_name FROM person AS p 
       INNER JOIN address AS a ON p.address_id = a.id 
        INNER JOIN city AS c ON a.city_id = c.city_id 
         INNER JOIN zip_code_catalog AS z ON a.street = z.street;
```

В результате получим таблицу с необходимой информацией о покупателях:

```
haircolors=# SELECT person_id, firstname, lastname, phonenumber, a.street, building, a.flat_no, zip_code, city_name FROM person AS p INNER JOIN address AS a ON p.address_id = a.id INNER JOIN city AS c ON a.city_id = c.city_id INNER JOIN zip_code_catalog AS z ON a.street = z.street;
 person_id | firstname | lastname | phonenumber  |         street          | building | flat_no | zip_code |  city_name  
-----------+-----------+----------+--------------+-------------------------+----------+---------+----------+-------------
         1 | Денис     | Петров   | +79784567897 | ул. Александра Косарева |       77 |      54 |   299006 | Севастополь
         2 | Юлия      | Бабкина  | +79784168585 | ул. Кесаева             |        1 |      55 |   299003 | Севастополь
(2 rows)

```

### Вывод

Наглядно видно, что запросы для получения выборок данных которые находятся в 
разных таблицах иногда могут быть скажем так не такими уж краткими. В некоторых 
случаях я думаю уместно будет произвести денормализацию, т.е. выполнить 
процесс, обратный нормализации, теряя несколько в независимости данных, но 
приобретая удобство и, возможно, в некоторых случаях улучшая 
производительность. 

### Ресурсы

[http://www.postgresqltutorial.com](http://www.postgresqltutorial.com/postgresql-inner-join/)

[https://www.tutorialspoint.com/postgresql](https://www.tutorialspoint.com/postgresql/postgresql_using_joins.htm)
