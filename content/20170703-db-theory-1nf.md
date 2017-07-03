Title: Процедура нормализации данных и нормальные формы данных (1НФ).
Category: Blog
Tags: SQL, theory, DB, database, 1NF

Данная заметка, делается в первую очередь для себя после прочтения 
монументального труда "Введение в системы баз данных" автора К. Дж. Дейт.  

Труд этот очень обширный и затрагивает множество теоретических и практических 
аспектов связанных с базами данных, теорией их устройства (большей
частью затронуты реляционные базы данных).  

Чтобы как-то оставить информацию в памяти я решил сделать заметку с некоторыми 
цитатами касательно понятия нормализации, денормализации и понятий нормальных 
форм.  


**Процедура нормализации** это процедура разбиения логически несвязанной информации
на отдельные переменные отношения (таблицы).

**Цель нормализации** - избавиться от избыточности, и избежать аномалий обновления к
которым приводит избыточность.

Проще говоря, преследуется цель разделить данные так, чтоб они были максимально 
независимыми друг от друга, тогда не возникает проблем с обновлением/удалением/добавлением
новых данных.

В качестве небольшого отступления для примера создадим базу в PostgreSQL с 
которой будем проводить эксперимент дальнейших преобразований:

```
postgres=# CREATE DATABASE haircolors;
CREATE DATABASE
postgres=# 
postgres=# \c haircolors 
You are now connected to database "haircolors" as user "postgres".
haircolors=# \dt
No relations found.

```
Представим, что мы оптовый продавец всякой всячины для салонов красоты и есть некая 
база данных покупателей которые делают у нас заказы для каких то салонов красоты,
которая может выглядеть допустим примерно так:

```postgresql
CREATE TABLE CUSTOMERS(
   ID INT PRIMARY KEY     NOT NULL,
   FIRSTNAME      VARCHAR(128) NOT NULL,
   LASTNAME       VARCHAR(128) NOT NULL,
   PHONENUMBER    VARCHAR(20) NOT NULL,
   SALON_NAME     VARCHAR(256) NOT NULL,
   ADDRESS        VARCHAR(256) NOT NULL,
   MANUFACTURER   VARCHAR(256) NOT NULL,
   PRODUCT_NAME	  VARCHAR(256) NOT NULL,
   DATEORDER	  TIMESTAMP NOT NULL, 
   PRICE         MONEY NOT NULL,
   QTY INT NOT NULL 
);
```

Покупатель с FIRSTNAME, LASTNAME, PHONENUMBER который живет по ADDRESS и производит 
закупки продукции PRODUCT_NAME неких производителей MANUFACTURER по цене PRICE 
в количестве QTY для салонов SALON_NAME, мы отмечаем дату и время когда произошел
заказ DATEORDER.

Данный пример больше учебный, взял очень произвольно, попробуем найти проблемы в 
процессе нормализации.

```
haircolors=# \d customers
                Table "public.customers"
    Column    |            Type             | Modifiers 
--------------+-----------------------------+-----------
 id           | integer                     | not null
 firstname    | character varying(128)      | not null
 lastname     | character varying(128)      | not null
 phonenumber  | character varying(20)       | not null
 salon_name   | character varying(256)      | not null
 address      | character varying(256)      | not null
 manufacturer | character varying(256)      | not null
 product_name | character varying(256)      | not null
 dateorder    | timestamp without time zone | not null
 price        | money                       | not null
 qty          | integer                     | not null
Indexes:
    "customers_pkey" PRIMARY KEY, btree (id)

```

Заполним нашу условную базу данных некоторыми значениями:

```postgresql
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY) 
VALUES (1, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Matrix', 'Краска для волос', '2017-07-03 12:15:01 +0000', 899.01, 3);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY) 
VALUES (2, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Loreal', 'Краска для волос', '2017-07-03 12:16:01 +0000', 599.12, 2);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY) 
VALUES (3, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Blond', 'Краска для волос', '2017-07-02 11:01:01 +0000', 299.12, 12);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY) 
VALUES (4, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Союз', 'Полотенца одноразовые', '2017-07-02 11:01:01 +0000', 199.12, 120);

```

Из произвольно набранных данных видим, что таблица не удовлетворяет 1НФ:
  
##### Первая нормальная форма
> **1НФ** - переменная отношения находится в 1нф тогда и только тогда, когда в 
любом допустимом значении этой переменной отношения (таблицы) 
каждый ее кортеж содержит одно значение для каждого из атрибутов (столбцов).
(короче говоря, повторяющиеся группы п1,п2,п3 в значении столбца запрещены) 
(фактически избавляемся от дубликации информации в ячейке столбца - 
не должно быть столбцов которые в ячейке имеют данные через запятую)

```
haircolors=# select * from customers ;
 id | firstname | lastname | phonenumber  |        salon_name        |                          address                          | manufacturer |     product_name      |      dateorder      |   price    | qty 
----+-----------+----------+--------------+--------------------------+-----------------------------------------------------------+--------------+-----------------------+---------------------+------------+-----
  1 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3
  2 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:15:01 | 599.12 руб |   2
  3 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12
  4 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120
(4 rows)

```
Здесь явно что то не так как минимум со столбцом **salon_name** в котором имеются
данные по смыслу означающие разные салоны (разные сущности) перечисленные через запятую.
Например если я захочу добавить заказчику "Денис Петров" еще 1 название салона, 
мне придется обновить все записи, причем не забыть ни одного вхождения. 
В примере малое количество записей (строк) и поэтому кажется ничего страшного, но 
представим что записей сотни тысяч и проблема станет ощутимее.
Кроме того очень неудобно работать с данными которые представлены вот так через 
запятую. Для получения какой либо полезной информации придется как то парсить
значение этого столбца.

Можно также увидеть что покупатель Юлия Бабкина поставляет товары в тот же салон 
ViVa, что и Денис Петров, следовательно сделаем заключение, что **"несколько разных 
покупателей могут поставлять продукцию в один и тот же салон.**

Приведем данные к первой нормальной форме, для чего создадим таблицу SALON c полями 
(столбцами) SALON_ID# и SALON_NAME, (на самом-то деле сейчас нет особой надобности в поле
SALON_ID#, так как само имя салона может являться первичным ключом, но представим, 
вдруг у нас могут быть 2 салона с одинаковым именем, и нам все же придется их 
как то различать) - вынесем возможные значения salon_name и привяжем с помощью 
внешнего ключа к нашей таблице **customers**.

```postgresql
CREATE TABLE SALON (
   SALON_ID SERIAL PRIMARY KEY,
   SALON_NAME VARCHAR(128) NOT NULL
);
```

```
haircolors=# \d salon
                                      Table "public.salon"
   Column   |          Type          |                        Modifiers                         
------------+------------------------+----------------------------------------------------------
 salon_id   | integer                | not null default nextval('salon_salon_id_seq'::regclass)
 salon_name | character varying(128) | not null
Indexes:
    "salon_pkey" PRIMARY KEY, btree (salon_id)

```

Добавим значения - названия салонов в таблицу SALON:
```postgresql
INSERT INTO salon (salon_name) VALUES ('Е-Студия');
INSERT INTO salon (salon_name) VALUES ('Ле-туаль');
INSERT INTO salon (salon_name) VALUES ('UpDo');
INSERT INTO salon (salon_name) VALUES ('ViVa');
INSERT INTO salon (salon_name) VALUES ('Diana');
```
получается следующее, обратим внимание что **salon_id** заполнен автоматически,
мы не определяли его значение:

```
haircolors=# select * from salon;
 salon_id | salon_name 
----------+------------
        1 | Е-Студия
        2 | Ле-туаль
        3 | UpDo
        4 | ViVa
        5 | Diana
(5 rows)

```

Переименуем столбец таблицы CUSTOMERS **salon_name** в **salon_name_old**
```postgresql
ALTER TABLE CUSTOMERS RENAME COLUMN SALON_NAME TO SALON_NAME_OLD;
```

Добавим столбец **salon_name** как внешний ключ который ссылается на первичный 
ключ таблицы SALON **salon_id**. Cначала создадим столбец, потом "навесим" на 
него ограничение:

```postgresql
ALTER TABLE customers ADD COLUMN SALON_NAME INT;

ALTER TABLE customers 
   ADD CONSTRAINT fk_salon_name
   FOREIGN KEY (salon_name) 
   REFERENCES salon(salon_id);

```

Ради примера удалим допустим ограничение NOT NULL столбца **salon_name_old**:

```postgresql
ALTER TABLE customers ALTER COLUMN salon_name_old DROP NOT NULL;
```

Можем наблюдать нами созданный столбец и ограничение:

```
haircolors=# \d customers
                 Table "public.customers"
     Column     |            Type             | Modifiers 
----------------+-----------------------------+-----------
 id             | integer                     | not null
 firstname      | character varying(128)      | not null
 lastname       | character varying(128)      | not null
 phonenumber    | character varying(20)       | not null
 salon_name_old | character varying(256)      | 
 address        | character varying(256)      | not null
 manufacturer   | character varying(256)      | not null
 product_name   | character varying(256)      | not null
 dateorder      | timestamp without time zone | not null
 price          | money                       | not null
 qty            | integer                     | not null
 salon_name     | integer                     | 
Indexes:
    "customers_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_salon_name" FOREIGN KEY (salon_name) REFERENCES salon(salon_id)

```

Теперь пришла очередь заполнить колонку **salon_name** таблицы CUSTOMERS:
 
```postgresql
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (5, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Matrix', 'Краска для волос', '2017-07-03 12:15:01 +0000', 899.01, 3, 1);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (6, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Matrix', 'Краска для волос', '2017-07-03 12:15:01 +0000', 899.01, 3, 2);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (7, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Matrix', 'Краска для волос', '2017-07-03 12:15:01 +0000', 899.01, 3, 4);

INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (8, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Loreal', 'Краска для волос', '2017-07-03 12:16:01 +0000', 599.12, 2, 1);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (9, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Loreal', 'Краска для волос', '2017-07-03 12:16:01 +0000', 599.12, 2, 2);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (10, 'Денис', 'Петров', '+79784567897', 'Е-Студия, ViVa, Ле-туаль', 'ул. Александра Косарева, д.77, кв. 54, Севастополь 299006', 'Loreal', 'Краска для волос', '2017-07-03 12:16:01 +0000', 599.12, 2, 4);


INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (11, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Blond', 'Краска для волос', '2017-07-02 11:01:01 +0000', 299.12, 12, 3);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (12, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Blond', 'Краска для волос', '2017-07-02 11:01:01 +0000', 299.12, 12, 4);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (13, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Blond', 'Краска для волос', '2017-07-02 11:01:01 +0000', 299.12, 12, 5);


INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (14, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Союз', 'Полотенца одноразовые', '2017-07-02 11:01:01 +0000', 199.12, 120, 3);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (15, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Союз', 'Полотенца одноразовые', '2017-07-02 11:01:01 +0000', 199.12, 120, 4);
INSERT INTO CUSTOMERS (ID,FIRSTNAME,LASTNAME,PHONENUMBER, SALON_NAME_OLD,ADDRESS,MANUFACTURER,PRODUCT_NAME,DATEORDER, PRICE, QTY, SALON_NAME) 
VALUES (16, 'Юлия', 'Бабкина', '+79784168585', 'UpDo, ViVa, Diana', 'ул. Кесаева, д.1, кв. 55, Севастополь 299003', 'Союз', 'Полотенца одноразовые', '2017-07-02 11:01:01 +0000', 199.12, 120, 5);

```
База значительно выросла, но не страшно, зато мы убрали перечисление в столбце:

```
haircolors=# select * from customers;
 id | firstname | lastname | phonenumber  |      salon_name_old      |                          address                          | manufacturer |     product_name      |      dateorder      |   price    | qty | salon_name 
----+-----------+----------+--------------+--------------------------+-----------------------------------------------------------+--------------+-----------------------+---------------------+------------+-----+------------
  1 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |           
  2 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:15:01 | 599.12 руб |   2 |           
  3 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |           
  4 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |           
  5 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          1
  6 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          2
  7 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          4
  8 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          1
  9 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          2
 10 | Денис     | Петров   | +79784567897 | Е-Студия, ViVa, Ле-туаль | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          4
 11 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          3
 12 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          4
 13 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          5
 14 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          3
 15 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          4
 16 | Юлия      | Бабкина  | +79784168585 | UpDo, ViVa, Diana        | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          5
(16 rows)

```
Теперь можно удалить столбец **salon_name_old** и строки с id 1-4, информация о
названии салона у нас представлена в столбце **salon_name**

```postgresql
ALTER TABLE customers DROP COLUMN salon_name_old ;

DELETE FROM customers WHERE id IN (1,2,3,4);
```
```
haircolors=# select * from customers;
 id | firstname | lastname | phonenumber  |                          address                          | manufacturer |     product_name      |      dateorder      |   price    | qty | salon_name 
----+-----------+----------+--------------+-----------------------------------------------------------+--------------+-----------------------+---------------------+------------+-----+------------
  5 | Денис     | Петров   | +79784567897 | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          1
  6 | Денис     | Петров   | +79784567897 | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          2
  7 | Денис     | Петров   | +79784567897 | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Matrix       | Краска для волос      | 2017-07-03 12:15:01 | 899.01 руб |   3 |          4
  8 | Денис     | Петров   | +79784567897 | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          1
  9 | Денис     | Петров   | +79784567897 | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          2
 10 | Денис     | Петров   | +79784567897 | ул. Александра Косарева, д.77, кв. 54, Севастополь 299006 | Loreal       | Краска для волос      | 2017-07-03 12:16:01 | 599.12 руб |   2 |          4
 11 | Юлия      | Бабкина  | +79784168585 | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          3
 12 | Юлия      | Бабкина  | +79784168585 | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          4
 13 | Юлия      | Бабкина  | +79784168585 | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Blond        | Краска для волос      | 2017-07-02 11:01:01 | 299.12 руб |  12 |          5
 14 | Юлия      | Бабкина  | +79784168585 | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          3
 15 | Юлия      | Бабкина  | +79784168585 | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          4
 16 | Юлия      | Бабкина  | +79784168585 | ул. Кесаева, д.1, кв. 55, Севастополь 299003              | Союз         | Полотенца одноразовые | 2017-07-02 11:01:01 | 199.12 руб | 120 |          5
(12 rows)

```

Вот что получилось, убрали перечисление для названия салонов, но не будем 
закрывать глаза на перечисление в столбце **address** , создадим отдельную 
табличку ADDRESS и заполним данными:  

```postgresql
CREATE TABLE ADDRESS (
   ID INT PRIMARY KEY,
   CITY VARCHAR(128) NOT NULL,
   BUILDING INT NOT NULL,
   FLAT_NO INT NOT NULL,
   STREET VARCHAR(128) NOT NULL,
   ZIP_CODE INT NOT NULL
);

INSERT INTO address (ID, CITY, STREET, BUILDING, FLAT_NO, ZIP_CODE) VALUES (
1, 'Севастополь', 'ул. Александра Косарева', 77, 54, 299006);
INSERT INTO address (ID, CITY, STREET, BUILDING, FLAT_NO, ZIP_CODE) VALUES (
2, 'Севастополь', 'ул. Кесаева', 1, 55, 299003);

```

```
haircolors=# select * from address;
 id |    city     | building | flat_no |         street          | zip_code 
----+-------------+----------+---------+-------------------------+----------
  1 | Севастополь |       77 |      54 | ул. Александра Косарева |   299006
  2 | Севастополь |        1 |      55 | ул. Кесаева             |   299003
(2 rows)

```
Теперь переименуем столбец **address** в таблице CUSTOMERS в **address_old**, 
создадим столбец **address** и заполним соответствующими значениями 
(пока не будем использовать никакие ограничения)

```postgresql
ALTER TABLE CUSTOMERS RENAME COLUMN address TO address_old;
ALTER TABLE CUSTOMERS ADD COLUMN address INT;

UPDATE customers SET address=1 WHERE id in (5,6,7,8,9,10);

UPDATE customers SET address=2 WHERE id not in (5,6,7,8,9,10);
```

Проверим, что не потеряли информацию о адресе и удалим столбец **address_old**

```postgresql
ALTER TABLE customers DROP COLUMN address_old ;
```

В результате получится так:

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

Итак, мы в конце концов привели нашу первоначальную таблицу к первой нормальной
форме **1НФ**. Как видим никакие данные в столбцах более не перечисляются.

В итоге мы получили 3 разные таблицы которые уже имеют связи, которые несложно проследить
такие как:

**ОДИН КО МНОГИМ** salon.salon_id (1) -> customers.salon_name (\*), такая связь
как видим организована с помощью customers.salon_name (FOREIGN KEY)(\*) -> salon.salon_id (PRIMARY KEY)(1)

**ОДИН К ОДНОМУ** 
Мы видим что пара значений firstname, lastname образуют первичный ключ, который 
может идентифицировать уникального пользователя, который живет по некоторому адресу
следовательно прослеживается связь (firstname, lastname) (1) <-> address.id (1).
В дальнейшем я вижу возможность использовать это, поэтому решил для упрощения 
примера не навешивать никаких ограничений, просто опишу эту связь словами.

Думаю можно переходить к приведению наших данных ко 2й нормальной форме, о чем 
будет мой завтрашний рассказ.
