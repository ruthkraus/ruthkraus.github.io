Title: Процедура нормализации данных и нормальные формы данных (2НФ).
Category: Blog
Tags: SQL, theory, DB, database, 1NF, 2NF

Итак пришло время привести данные, которые мы привели к 1НФ, ко 2НФ.
Само понятие 2НФ можно процитировать из книги Дж. Дейта, как:

> **2НФ** - переменная отношения находится во 2нф тогда и только тогда, когда она 
находится в первой нф и каждый неключевой атрибут неприводимо зависит от 
ее первичного ключа.(предполагается наличие 1 потенциального ключа который 
является первичным ключом) 

##### Первый этап нормализации (подразумевается что отношения уже в 1НФ)
> Всякую переменную отношения которая находится в 1НФ, но не находится во 2НФ 
всегда можно свести к эквивалентному множеству отношений находящихся во 2НФ.

Этот процесс заключается в замене переменной отношения 1НФ подходящим набором
проекций, эквивалентных исходной переменной отношения , в том смысле что ее 
всегда можно будет восстановить путем соединения данных проекций.

> Если есть R {A,B,C,D} PRIMARY KEY {A,B} (предположим что А зависит от D A -> D),

>тогда процедура нормализации состоит в замене этой R двумя проекциями
R1 {A, D} PRIMARY KEY {A}
R2 {A, B, C} PRIMARY KEY {A,B} FOREIGN KEY {A} REFERENCES R1

получается R2 будет иметь атрибут А как внешний ключ ссылаясь на первичный ключ 
A таблицы R1 и переменная отношения R может быть восстановлена посредством 
соединения переменных отношения R1 R2 по внешнему ключу и соответствующему ему 
первичному ключу этих переменных отношения.

Своими словами, если у нас в таблице есть столбец который явно зависит от 
первичного ключа, его следует выделить в отдельную таблицу, где будет 
первичный ключ и этот столбец, а в исходной таблице бывший первичный ключ 
станет внешним.

(фактически это приводит к удалению дубликатов в строках и 
разделению данных которые зависят от одной из частей составного первичного ключа,
фактически разделяется на отдельные отношения в которых отдельная часть 
составного первичного ключа будет являться первичным ключом а, второе отношение 
будет иметь составной первичный ключ, в котором выделенная часть 
предыдущего составного первичного ключа будет внешним ключом по отношению к 
первичному ключу отделенного отношения)

Напомним к чему мы пришли приведя данные в 1НФ:

```
haircolors=# ALTER TABLE customers DROP COLUMN address_old ;
ALTER TABLE
haircolors=# select * from customers ;
 id | firstname | lastname | phonenumber  | manufacturer |     product_name      |      dateorder      |   price    | qty | salon_name | address 
----+-----------+----------+--------------+--------------+-----------------------+---------------------+------------+-----+------------+---------
  5 | Денис     | Петров   | +79784567897 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          1 |       1
  6 | Денис     | Петров   | +79784567897 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          2 |       1
  7 | Денис     | Петров   | +79784567897 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          4 |       1
  8 | Денис     | Петров   | +79784567897 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          1 |       1
  9 | Денис     | Петров   | +79784567897 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          2 |       1
 10 | Денис     | Петров   | +79784567897 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          4 |       1
 11 | Юлия      | Бабкина  | +79784168585 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          3 |       2
 12 | Юлия      | Бабкина  | +79784168585 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          4 |       2
 13 | Юлия      | Бабкина  | +79784168585 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          5 |       2
 14 | Юлия      | Бабкина  | +79784168585 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          3 |       2
 15 | Юлия      | Бабкина  | +79784168585 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          4 |       2
 16 | Юлия      | Бабкина  | +79784168585 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          5 |       2
(12 rows)

haircolors=# select * from salon;
 salon_id | salon_name 
----------+------------
        1 | Е-Студия
        2 | Ле-туаль
        3 | UpDo
        4 | ViVa
        5 | Diana
(5 rows)

haircolors=# select * from address ;
 id |    city     | building | flat_no |         street          | zip_code 
----+-------------+----------+---------+-------------------------+----------
  1 | Севастополь |       77 |      54 | ул. Александра Косарева |   299006
  2 | Севастополь |        1 |      55 | ул. Кесаева             |   299003
(2 rows)

```

Явно видно, что имя-фамилия покупателей образуют уникальный ключ и существует связь
с полем **address**, создадим таблицу PERSON в ней создадим поле **address**,
которое является внешним ключом ссылающимся на первичный ключ таблицы ADDRESS (id)
и свяжет таким образом покупателя с адресом (person.address(FK)) -> address.id(PK).
Заполним таблицу данными:  

```postgresql
CREATE TABLE PERSON (
  PERSON_ID INT PRIMARY KEY,
  FIRSTNAME      VARCHAR(128) NOT NULL,
  LASTNAME       VARCHAR(128) NOT NULL,
  PHONENUMBER    VARCHAR(20) NOT NULL,
  ADDRESS INT,
  CONSTRAINT fk_address_id
     FOREIGN KEY (ADDRESS) 
     REFERENCES address (id)
);

INSERT INTO PERSON (PERSON_ID, FIRSTNAME, LASTNAME, PHONENUMBER, ADDRESS) VALUES (
1, 'Денис', 'Петров', '+79784567897', 1);

INSERT INTO PERSON (PERSON_ID, FIRSTNAME, LASTNAME, PHONENUMBER, ADDRESS) VALUES (
2, 'Юлия', 'Бабкина', '+79784168585', 2);

```
не забудем, для целостности данных добавим уникальность полю **address**
ведь у нас 1 покупатель может иметь только 1 уникальный адрес, мы условились что
разные покупатели не могут иметь один и тот же адрес:

```postgresql
ALTER TABLE person ADD UNIQUE (address);
```

```
haircolors=# \d person
              Table "public.person"
   Column    |          Type          | Modifiers 
-------------+------------------------+-----------
 person_id   | integer                | not null
 firstname   | character varying(128) | not null
 lastname    | character varying(128) | not null
 phonenumber | character varying(20)  | not null
 address     | integer                | 
Indexes:
    "person_pkey" PRIMARY KEY, btree (person_id)
    "person_address_key" UNIQUE CONSTRAINT, btree (address)
Foreign-key constraints:
    "fk_address_id" FOREIGN KEY (address) REFERENCES address(id)
Referenced by:
    TABLE "customers" CONSTRAINT "fk_person_id" FOREIGN KEY (person_id) REFERENCES person(person_id)

```

```
haircolors=# select * from person ;
 person_id | firstname | lastname | phonenumber  | address 
-----------+-----------+----------+--------------+---------
         1 | Денис     | Петров   | +79784567897 |       1
         2 | Юлия      | Бабкина  | +79784168585 |       2
(2 rows)

```

Теперь при попытке назначить один и тот же адрес 2м разным пользователям система
откажет в операции и вызовет исключение, попробуем установить Юлии Бабкиной такой 
же адрес как Денису Петрову:

```
haircolors=# UPDATE person SET address=1 WHERE person_id=2;
ERROR:  duplicate key value violates unique constraint "person_address_key"
DETAIL:  Key (address)=(1) already exists.
```

Единственое, ошибочка вышла, лучше переименум поле **address** в **address_id**
чтоб отражался смысл
```postgresql
 ALTER TABLE person RENAME COLUMN address TO address_id;
```
Таблица примет вид
```
haircolors=# \d person
              Table "public.person"
   Column    |          Type          | Modifiers 
-------------+------------------------+-----------
 person_id   | integer                | not null
 firstname   | character varying(128) | not null
 lastname    | character varying(128) | not null
 phonenumber | character varying(20)  | not null
 address_id  | integer                | 
Indexes:
    "person_pkey" PRIMARY KEY, btree (person_id)
    "person_address_key" UNIQUE CONSTRAINT, btree (address_id)
Foreign-key constraints:
    "fk_address_id" FOREIGN KEY (address_id) REFERENCES address(id)
Referenced by:
    TABLE "partner" CONSTRAINT "partner_person_id_fkey" FOREIGN KEY (person_id) REFERENCES person(person_id)
```
c данными:

```
haircolors=# select * from person ;
 person_id | firstname | lastname | phonenumber  | address_id 
-----------+-----------+----------+--------------+------------
         1 | Денис     | Петров   | +79784567897 |          1
         2 | Юлия      | Бабкина  | +79784168585 |          2
(2 rows)

```

Таким образом мы выразили связь ОДИН К ОДНОМУ (ONE TO ONE), используя внешний
ключ и уникальный индекс.
Можно было также в модели ADDRESS добавить поле person_id, сделать его внешним 
ключом и добавить уникальность. (т.е. фактически то же самое, но в обратную сторону)
Пока будем считать что мы сделали равнозначный вариант, но предполагаю что в 
будущем не исключено что можно сделать обратное, например для некоего удобства.


Теперь нашу исходную таблицу CUSTOMERS можно представить так, мы добавим столбец 
person_id и по нему все также мы можем узнать адрес покупателя, т.е. информацию 
мы не теряем, это самый главный принцип, мы не должны в результате нормализации
потерять часть информации. Т.е. можем убрать столбцы firstname, lastname, 
phonenumber, address и все равно можем узнать имя-фамилию, телефон, адрес покупателя.
 
```postgresql
ALTER TABLE CUSTOMERS DROP COLUMN firstname;
ALTER TABLE CUSTOMERS DROP COLUMN lastname;
ALTER TABLE CUSTOMERS DROP COLUMN phonenumber;
ALTER TABLE CUSTOMERS DROP COLUMN address;


ALTER TABLE customers ADD COLUMN person_id INT;

ALTER TABLE customers 
   ADD CONSTRAINT fk_person_id
   FOREIGN KEY (person_id) 
   REFERENCES person(person_id);

UPDATE customers SET person_id = 1 WHERE id IN (5,6,7,8,9,10);
UPDATE customers SET person_id = 2 WHERE id NOT IN (5,6,7,8,9,10);
```


```
haircolors=# select * from customers ;
 id | manufacturer |     product_name      |      dateorder      |   price    | qty | salon_name | person_id 
----+--------------+-----------------------+---------------------+------------+-----+------------+-----------
  5 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          1 |         1
  6 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          2 |         1
  7 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          4 |         1
  8 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          1 |         1
  9 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          2 |         1
 10 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          4 |         1
 11 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          3 |         2
 12 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          4 |         2
 13 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          5 |         2
 14 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          3 |         2
 15 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          4 |         2
 16 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          5 |         2
(12 rows)

```

Теперь наша таблица CUSTOMERS все больше напоминает список заказов которые делает
покупатель, который представлен внешним ключом person_id. 

Продолжим, явно у нас есть связь между производителем и продуктом, т.е. продукт явно
должен быть кем то произведен, причем продукт может производиться разными 
производителями.
  
Правило приведения ко 2НФ советует сделать таблицы для столбцов с повторяющимися
значениями.

Так и поступим, создадим таблицу MANUFACTURER:
```postgresql
CREATE TABLE MANUFACTURER (
  MANUFACTURER_ID INT PRIMARY KEY,
  NAME VARCHAR(256) NOT NULL
);

INSERT INTO MANUFACTURER (MANUFACTURER_ID, NAME) VALUES (1, 'Matrix');
INSERT INTO MANUFACTURER (MANUFACTURER_ID, NAME) VALUES (2, 'Loreal');
INSERT INTO MANUFACTURER (MANUFACTURER_ID, NAME) VALUES (3, 'Blond');
INSERT INTO MANUFACTURER (MANUFACTURER_ID, NAME) VALUES (4, 'Союз');
```


```
haircolors=# \d manufacturer
             Table "public.manufacturer"
     Column      |          Type          | Modifiers 
-----------------+------------------------+-----------
 manufacturer_id | integer                | not null
 name            | character varying(256) | not null
Indexes:
    "manufacturer_pkey" PRIMARY KEY, btree (manufacturer_id)

haircolors=# select * from manufacturer ;
 manufacturer_id |  name  
-----------------+--------
               1 | Matrix
               2 | Loreal
               3 | Blond
               4 | Союз
(4 rows)

```
А теперь создадим таблицу PRODUCT, здесь явно видна связь между названием продукта/товара,
производителем и ценой.
Фактически атрибуты NAME и MANUFACTURER_ID образуют первичный ключ, но я добавлю
отдельный первичный ключ для удобства - PRODUCT_ID. Это некоторая избыточность с теоретической 
точки зрения, но мне кажется что с таким подходом работать с данными удобнее.
Теоретически я не должен добавлять PRODUCT_ID, уникальность уже обеспечивает 
связка название товара - производитель, но в таком случае у нас будет сложный 
первичный ключ (первичный ключ образованный значениями 2х столбцов).

```postgresql
CREATE TABLE PRODUCT (
  PRODUCT_ID INT PRIMARY KEY,
  NAME VARCHAR(256),
  MANUFACTURER_ID INT REFERENCES manufacturer(manufacturer_id),
  PRICE MONEY
);

INSERT INTO PRODUCT (PRODUCT_ID, NAME, MANUFACTURER_ID, PRICE) VALUES (
1, 'Краска для волос', 1, 899.01);
INSERT INTO PRODUCT (PRODUCT_ID, NAME, MANUFACTURER_ID, PRICE) VALUES (
2, 'Краска для волос', 2, 599.12);
INSERT INTO PRODUCT (PRODUCT_ID, NAME, MANUFACTURER_ID, PRICE) VALUES (
3, 'Краска для волос', 3, 299.12);
INSERT INTO PRODUCT (PRODUCT_ID, NAME, MANUFACTURER_ID, PRICE) VALUES (
4, 'Полотенца одноразовые', 4, 199.12);

```

```
haircolors=# \d product
                Table "public.product"
     Column      |          Type          | Modifiers 
-----------------+------------------------+-----------
 product_id      | integer                | not null
 name            | character varying(256) | 
 manufacturer_id | integer                | 
 price           | money                  | 
Indexes:
    "product_pkey" PRIMARY KEY, btree (product_id)
Foreign-key constraints:
    "product_manufacturer_id_fkey" FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(manufacturer_id)

haircolors=# select * from product ;
 product_id |         name          | manufacturer_id |   price    
------------+-----------------------+-----------------+------------
          1 | Краска для волос      |               1 | 899.01 руб
          2 | Краска для волос      |               2 | 599.12 руб
          3 | Краска для волос      |               3 | 299.12 руб
          4 | Полотенца одноразовые |               4 | 199.12 руб
(4 rows)

```
Теперь мы можем сослаться на product_id таблицы PRODUCT в нашей изначальной 
таблице чтобы обозначить что покупают покупатели.
Добавим столбец product_id в таблицу CUSTOMERS, как внешний ключ ссылающийся на
значение поля таблицы PRODUCT.PRODUCT_ID

```postgresql
ALTER TABLE customers ADD COLUMN product_id INT REFERENCES product(product_id);
```
```
haircolors=# select * from customers ;
 id | manufacturer |     product_name      |      dateorder      |   price    | qty | salon_name | person_id | product_id 
----+--------------+-----------------------+---------------------+------------+-----+------------+-----------+------------
  5 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          1 |         1 |           
  6 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          2 |         1 |           
  7 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          4 |         1 |           
  8 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          1 |         1 |           
  9 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          2 |         1 |           
 10 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          4 |         1 |           
 11 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          3 |         2 |           
 12 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          4 |         2 |           
 13 | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          5 |         2 |           
 14 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          3 |         2 |           
 15 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          4 |         2 |           
 16 | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          5 |         2 |           
(12 rows)

```
Подставим значения соответствующих product.product_id и затем удалим столбцы
manufacturer, product_name, price

```postgresql
UPDATE customers SET product_id = 1 WHERE id in (5,6,7);
UPDATE customers SET product_id = 2 WHERE id in (8,9,10);
UPDATE customers SET product_id=3 WHERE id in (11,12,13);
UPDATE customers SET product_id=4 WHERE id in (14,15,16);

ALTER TABLE customers DROP COLUMN manufacturer;
ALTER TABLE customers DROP COLUMN product_name;
ALTER TABLE customers DROP COLUMN price;

```
Переименуем неудачно названный столбец salon_name, так как он означает суть 
salon_id, мы можем вычислить по нему salon_name, но в таблице мы указываем именно
salon_id:
```postgresql
ALTER TABLE customers RENAME COLUMN salon_name TO salon_id;
```
Можно переименовать ограничение 
```postgresql
ALTER TABLE customers RENAME CONSTRAINT fk_salon_name TO fk_salon_id;
```

```
haircolors=# select * from customers ;
 id |      dateorder      | qty | salon_id | person_id | product_id 
----+---------------------+-----+----------+-----------+------------
  5 | 2017-07-03 12:15:01 |   3 |        1 |         1 |          1
  6 | 2017-07-03 12:15:01 |   3 |        2 |         1 |          1
  7 | 2017-07-03 12:15:01 |   3 |        4 |         1 |          1
  8 | 2017-07-03 12:16:01 |   2 |        1 |         1 |          2
  9 | 2017-07-03 12:16:01 |   2 |        2 |         1 |          2
 10 | 2017-07-03 12:16:01 |   2 |        4 |         1 |          2
 11 | 2017-07-02 11:01:01 |  12 |        3 |         2 |          3
 12 | 2017-07-02 11:01:01 |  12 |        4 |         2 |          3
 13 | 2017-07-02 11:01:01 |  12 |        5 |         2 |          3
 14 | 2017-07-02 11:01:01 | 120 |        3 |         2 |          4
 15 | 2017-07-02 11:01:01 | 120 |        4 |         2 |          4
 16 | 2017-07-02 11:01:01 | 120 |        5 |         2 |          4
(12 rows)

```
Также я хотел бы переименовать таблицу СUSTOMERS потому что она отражает скорее
заказы чем покупателей, переименуем в ORDERS (я изначально неправильно назвал 
исходную таблицу и вот в результате приведения проблема обозначилась очень явно,
когда убрали лишние по смыслу данные которые сбили меня с толку вначале):
[link](http://www.postgresqltutorial.com/postgresql-rename-table/)

```postgresql
ALTER TABLE customers RENAME TO orders;
```

```
haircolors=# \d orders 
                Table "public.orders"
   Column   |            Type             | Modifiers 
------------+-----------------------------+-----------
 id         | integer                     | not null
 dateorder  | timestamp without time zone | not null
 qty        | integer                     | not null
 salon_id   | integer                     | 
 person_id  | integer                     | 
 product_id | integer                     | 
Indexes:
    "customers_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "customers_product_id_fkey" FOREIGN KEY (product_id) REFERENCES product(product_id)
    "fk_person_id" FOREIGN KEY (person_id) REFERENCES person(person_id)
    "fk_salon_id" FOREIGN KEY (salon_id) REFERENCES salon(salon_id)

```
Переименуем ограничения, так как после переименования у нас остались названия на 
более не существующее имя CUSTOMERS:
```postgresql
ALTER TABLE orders RENAME CONSTRAINT customers_pkey TO orders_pkey;
ALTER TABLE orders RENAME CONSTRAINT customers_product_id_fkey TO orders_product_id_fkey;
```

```
haircolors=# \d orders 
                Table "public.orders"
   Column   |            Type             | Modifiers 
------------+-----------------------------+-----------
 id         | integer                     | not null
 dateorder  | timestamp without time zone | not null
 qty        | integer                     | not null
 salon_id   | integer                     | 
 person_id  | integer                     | 
 product_id | integer                     | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_person_id" FOREIGN KEY (person_id) REFERENCES person(person_id)
    "fk_salon_id" FOREIGN KEY (salon_id) REFERENCES salon(salon_id)
    "orders_product_id_fkey" FOREIGN KEY (product_id) REFERENCES product(product_id)

```
В результате преобразований получилась таблица ORDER которая все так же отражает
покупки покупателей, и мы по прежнему можем узнать детали относящиеся к покупателю,
цену отдельного товара и название производителя.

```
haircolors=# select * from orders ;
 id |      dateorder      | qty | salon_id | person_id | product_id 
----+---------------------+-----+----------+-----------+------------
  5 | 2017-07-03 12:15:01 |   3 |        1 |         1 |          1
  6 | 2017-07-03 12:15:01 |   3 |        2 |         1 |          1
  7 | 2017-07-03 12:15:01 |   3 |        4 |         1 |          1
  8 | 2017-07-03 12:16:01 |   2 |        1 |         1 |          2
  9 | 2017-07-03 12:16:01 |   2 |        2 |         1 |          2
 10 | 2017-07-03 12:16:01 |   2 |        4 |         1 |          2
 11 | 2017-07-02 11:01:01 |  12 |        3 |         2 |          3
 12 | 2017-07-02 11:01:01 |  12 |        4 |         2 |          3
 13 | 2017-07-02 11:01:01 |  12 |        5 |         2 |          3
 14 | 2017-07-02 11:01:01 | 120 |        3 |         2 |          4
 15 | 2017-07-02 11:01:01 | 120 |        4 |         2 |          4
 16 | 2017-07-02 11:01:01 | 120 |        5 |         2 |          4
(12 rows)

```
Смотрим, у нас явно связь и повторы между person_id и salon_id, вынесем ее в таблицу 
которую назовем PARTNER и действительно, у нас покупатели являются партнерами-поставщиками
для салонов.

```postgresql
CREATE TABLE PARTNER (
  PARTNER_ID SERIAL PRIMARY KEY ,
  PERSON_ID INT REFERENCES PERSON(PERSON_ID),
  SALON_ID INT REFERENCES SALON(SALON_ID)
);

INSERT INTO PARTNER (PERSON_ID, SALON_ID) VALUES (1, 1);
INSERT INTO PARTNER (PERSON_ID, SALON_ID) VALUES (1, 2);
INSERT INTO PARTNER (PERSON_ID, SALON_ID) VALUES (1, 4);

INSERT INTO PARTNER (PERSON_ID, SALON_ID) VALUES (2, 3);
INSERT INTO PARTNER (PERSON_ID, SALON_ID) VALUES (2, 4);
INSERT INTO PARTNER (PERSON_ID, SALON_ID) VALUES (2, 5);

```

```
haircolors=# \d partner
                               Table "public.partner"
   Column   |  Type   |                          Modifiers                           
------------+---------+--------------------------------------------------------------
 partner_id | integer | not null default nextval('partner_partner_id_seq'::regclass)
 person_id  | integer | 
 salon_id   | integer | 
Indexes:
    "partner_pkey" PRIMARY KEY, btree (partner_id)
Foreign-key constraints:
    "partner_person_id_fkey" FOREIGN KEY (person_id) REFERENCES person(person_id)
    "partner_salon_id_fkey" FOREIGN KEY (salon_id) REFERENCES salon(salon_id)
```
```
haircolors=# select * from partner;
 partner_id | person_id | salon_id 
------------+-----------+----------
          1 |         1 |        1
          2 |         1 |        2
          3 |         1 |        4
          4 |         2 |        3
          5 |         2 |        4
          6 |         2 |        5
(6 rows)

```
Получилось мы еще упростили нашу таблицу ORDERS, теперь возможно добавить 
партнера (как связь покупатель-салон, допустим это может означать, что салон начал
работать с новым поставщиком) и мы можем это сделать, даже если покупатель не совершил
ни одного заказа, чего раньше мы сделать просто не могли, так как для выражения
связи того что какой то покупатель поставляет гипотетически что то в какой то салон,
нам было необходимо чтоб этот покупатель совершил заказ.
Теперь у нас могут быть партнеры не совершившие ни одного заказа !
Вот одно из положительных качеств нормализации.

Также можно удалить столбцы salon_id, person_id из таблицы ORDERS.

```postgresql
ALTER TABLE orders ADD COLUMN partner_id INT REFERENCES partner(partner_id);

UPDATE orders SET partner_id = 1 WHERE id IN (5,8);
UPDATE orders SET partner_id = 2 WHERE id IN (6,9);
UPDATE orders SET partner_id = 3 WHERE id IN (7,10);
UPDATE orders SET partner_id = 4 WHERE id IN (11,14);
UPDATE orders SET partner_id = 5 WHERE id IN (12,15);
UPDATE orders SET partner_id = 6 WHERE id IN (13,16);

ALTER TABLE orders DROP COLUMN salon_id ;
ALTER TABLE orders DROP COLUMN person_id ;

```

```
haircolors=# select * from orders order by id ;
 id |      dateorder      | qty | product_id | partner_id 
----+---------------------+-----+------------+------------
  5 | 2017-07-03 12:15:01 |   3 |          1 |          1
  6 | 2017-07-03 12:15:01 |   3 |          1 |          2
  7 | 2017-07-03 12:15:01 |   3 |          1 |          3
  8 | 2017-07-03 12:16:01 |   2 |          2 |          1
  9 | 2017-07-03 12:16:01 |   2 |          2 |          2
 10 | 2017-07-03 12:16:01 |   2 |          2 |          3
 11 | 2017-07-02 11:01:01 |  12 |          3 |          4
 12 | 2017-07-02 11:01:01 |  12 |          3 |          5
 13 | 2017-07-02 11:01:01 |  12 |          3 |          6
 14 | 2017-07-02 11:01:01 | 120 |          4 |          4
 15 | 2017-07-02 11:01:01 | 120 |          4 |          5
 16 | 2017-07-02 11:01:01 | 120 |          4 |          6
(12 rows)

```
Как видим тенденция такая, с каждым шагом появляется все больше таблиц, а изначальная 
таблица вырождается в описание связей. Управлять целостностью проще, данные разделяются
все больше по смыслу, но общую картину теперь возможно немного сложнее представить.

У нас присутствует дублирование на первый взгляд dateorder, qty, но это обусловлено
тем что мы изначально имели перечисление салонов в столбце **salon_name** и получается,
что покупатели как бы купили в одно и то же время разные товары сразу для нескольких
салонов, т.е. по смыслу здесь может быть и разное на самом деле время, то же 
самое относится к столбцу **qty**.

Но, и здесь можно убрать дублирование создадим таблицу ORDER_DETAILS
```postgresql
CREATE TABLE ORDER_DETAILS (
  ORDER_DETAILS_ID SERIAL PRIMARY KEY,
  DATEORDER TIMESTAMP,
  QTY INT
);

INSERT INTO ORDER_DETAILS (DATEORDER, QTY) VALUES ('2017-07-03 12:15:01', 3);
INSERT INTO ORDER_DETAILS (DATEORDER, QTY) VALUES ('2017-07-03 12:16:01', 2);
INSERT INTO ORDER_DETAILS (DATEORDER, QTY) VALUES ('2017-07-02 11:01:01', 12);
INSERT INTO ORDER_DETAILS (DATEORDER, QTY) VALUES ('2017-07-02 11:01:01', 120);

```
```
haircolors=# select * from order_details;
 order_details_id |      dateorder      | qty 
------------------+---------------------+-----
                1 | 2017-07-03 12:15:01 |   3
                2 | 2017-07-03 12:16:01 |   2
                3 | 2017-07-02 11:01:01 |  12
                4 | 2017-07-02 11:01:01 | 120
(4 rows)
```
Сошлемся на эти данные из таблицы ORDERS: 
 
```postgresql
ALTER TABLE orders ADD COLUMN ORDER_DETAILS_ID INT REFERENCES order_details(order_details_id);

UPDATE orders SET order_details_id = 1 WHERE id IN (5,6,7);
UPDATE orders SET order_details_id=2 WHERE id IN (8,9,10);
UPDATE orders SET order_details_id=3 WHERE id IN (11,12,13);
UPDATE orders SET order_details_id=4 WHERE id IN (14,15,16);

```
И теперь можно удалить столбцы dateorder, qty: 

```postgresql
ALTER TABLE orders DROP COLUMN dateorder ;
ALTER TABLE orders DROP COLUMN qty;
```

Все, на этом можно остановиться, у нас данные находятся, во 2НФ, мы избавились от 
дубликатов в колонках, и теперь таблица ORDERS содержит уникальный первичный ключ **id**
отражающий номер покупки, а также включает в себя отображение связей кто (**partner_id**),
какой именно продукт (**product_id**) купил и когда (**order_details_id**).
Эти три значения отражают уникальность каждой покупки, в принципе можно даже 
отказаться от параметра id и использовать первичный сложный ключ из трех столбцов,
но по моему мнению это неудобно, я хочу иметь номер заказа.

```
haircolors=# select * from orders;
 id | product_id | partner_id | order_details_id 
----+------------+------------+------------------
  5 |          1 |          1 |                1
  6 |          1 |          2 |                1
  7 |          1 |          3 |                1
  8 |          2 |          1 |                2
  9 |          2 |          2 |                2
 10 |          2 |          3 |                2
 11 |          3 |          4 |                3
 12 |          3 |          5 |                3
 13 |          3 |          6 |                3
 14 |          4 |          4 |                4
 15 |          4 |          5 |                4
 16 |          4 |          6 |                4
(12 rows)

```

В результате преобразований у нас получилось несколько таблиц, мы использовали 
связи различных типов, такие как **ОДИН К ОДНОМУ**, **ОДИН КО МНОГИМ**,
**МНОГИЕ КО МНОГИМ**.

 Мое лично субьективное мнение, что формы в которой находится база данных сейчас
с практической точки зрения достаточно. 

В следующей статье я возможно попробую привести некоторые данные в 3НФ, а также
нарисую схему связей нашей базы данных.

P.S. Я буду очень рад если кто то, прочитав заметку, укажет на мои ошибки. Я честно 
старался принимать логичные решения и эволюционировал связи без всяческих "подгонок".
Конечно же я мог ошибиться логически. Данная статья не является учебником для кого-то, и
написана мной для меня в первую очередь.

Для себя с некоторым удивлением замечаю как простая база в 4 записи превращается
во множество таблиц со связями. Советую людям которым интересно взять свой пример
и проделать похожее, как по мне это интересно и полезно ;-)
