Title: Процедура нормализации данных и нормальные формы данных (4НФ, 5НФ).
Category: Blog
Tags: SQL, theory, DB, database, 1NF, 2NF, 3NF, 4NF, 5NF

Завершаю серию заметок о нормализации, сведениями о понятиях более высоких 
нормальных форм 4НФ и 5НФ (чтобы иметь небольшую справку).

Большей частью это цитирование труда Криса Дж. Дейта, с его же примерами.
Поэтому возможны упоминания глав, и ссылок на литературу, присутствующую в 
книге. 

### Четвертая нормальная форма 4НФ.

Эта форма для многозначных зависимостей, когда значения - таблицы.

> Переменная отношения R находится в четвертой нормальной форме тогда и только 
тогда, когда в случае существования таких подмножеств A и В атрибутов этой 
переменной отношения R, для которых выполняется неривиальная многозначная 
зависимость A -> -> B, все атрибуты отношения R также зависят от атрибута А.

Когда приходится иметь дело с переменной отношения которая содержит как  
атрибуты - отношения, *{COURSE, TEXTS, TEACHERS}* когда *TEXTS*, *TEACHERS* 
это в свою очередь отношения *TEXT*, *TEACHER* (в которых несколько значений), 
допустим 1 курс может ссылаться на значение TEXT а там несколько учебников, и 
*TEACHER* - несколько учителей.
Тогда чтоб привести все в 4 нормальную форму - можно привести к НФБК
составить отношение *{COURSE, TEXT, TEACHER}* в которые включатся все 
комбинации, и явно будет видно избыточность и связанную с ним неудобство, 
затем разделить на проекции *{COURSE, TEXT}* , *{COURSE, TEACHER}* это и 
получится 4НФ

либо 2й способ - сразу разбить на проекции *{COURSE, TEACHERS}* , 
*{COURSE,TEXTS}* и затем привести эти проекции к НФБК, это будет фактически 4НФ.

### Пятая нормальная форма 5НФ.

Есть отношения которые нельзя выполнить декомпозицию на 2 составляющие без 
потерь, но можно на 3 и более.

>Допустим есть отношение SPJ {S#, #P, #J} которое можно разбить на 3 проекции 
{#S, #P}, {#P, #J}, {#J, #S} в результате соединения 3х проекций получится SPJ.
Cледует выполнять такую 3-декомпозицию чтоб избавиться в исходной SPJ от 
аномалий обновления.

>Переменная отношения R находится в пятой нормальной форме, которую называют 
иногда проекционно-соединительной нормальной формой ПСНФ тогда и только тогда, 
когда каждая нетривиальная зависимость соединения в переменной 
отношения R определяется потенциальным ключом(ключами) R, если соблюдаются 
условия:

1. Зависимость соединения *{A,B, ..Z} в переменной отношения R является 
тривиальной тогда и только тогда когда по крайней мере одно из подмножеств A,
 B, ..Z множества атрибутов является множеством всех атрибутов R.

2. Зависимость соединения *{A,B,..Z} в переменной отношения R определяется 
потенциальным ключом (ключами) R тогда и только тогда когда каждое из 
подмножеств А,B..Z множества атрибутов является суперключом для R.

Переменная SPJ не находится в 5НФ, поскольку может быть 3-декомпонована.
Если переменная отношений находится в 5НФ - она не содержит аномалий.

Если переменная отношения находится в 5НФ то единственными в ней являются те 
зависимости соединения, которые определяются ее потенциальными ключами, и 
тогда единственными возможными декомпозициями будут декомпозиции, которые 
основаны на эти потенциальных ключах.
(Каждая проекция в подобной декомпозиции будет состоять из одного или нескольких
потенциальных ключей в сочетании с доп атрибутами в кол-ве от нуля и больше)

### Общая схема процедуры нормализации

(примечание от меня - предполагается что отношение(таблица) уже находится в 1НФ)

1. Переменную отношения в 1НФ следует разбить на такие проекции, которые 
позволят исключить все функциональные зависимости, не являющиеся неприводимыми.
В результате будет получен набор переменных отношения в 2НФ.

2. Полученные переменные отношения в 2НФ следует разбить на такие проекции,
которые позволят исключить все существующие транзитивные функциональные
зависимости. В результате будет получен набор переменных отношения в ЗНФ.

3. Полученные переменные отношения в ЗНФ следует разбить на проекции, 
позволяющие исключить все оставшиеся функциональные зависимости, в которых 
детерминанты не являются потенциальными ключами. В результате такого приведения 
будет получен набор переменных отношения в НФБК.
Примечание. Правила 1—3 могут быть объединены в одно: "Исходную переменную
отношения следует разбить на проекции, позволяющие исключить все функциональные 
зависимости, в которых детерминанты не являются потенциальными ключами".

4. Полученные переменные отношения в НФБК следует разбить на проекции, позво
ляющие исключить все многозначные зависимости, которые не являются также
функциональными. В результате будет получен набор переменных отношения в 4НФ.
Примечание. На практике такие многозначные зависимости обычно исключаются
перед выполнением этапов 1-3 (на этапе "устранения независимых МЗЗ(многознач 
зависимостей)")

5. Полученные переменные отношения в 4НФ следует разбить на проекции, 
позволяющие исключить все зависимости соединения, которые не определяются 
потенциальными ключами (хотя в данном случае в определение следовало бы добавить
фразу "если удастся их выявить"). В результате будет получен набор переменных 
отношения в 5НФ.

По поводу приведенных выше правил можно сделать несколько дополнительных 
замечаний.

1. Процесс разбиения на проекции на каждом этапе должен быть выполнен без потерь 
	и с сохранением зависимостей (там, где это возможно).
2. Обратите внимание, что существует довольно привлекательный набор следующих
   альтернативных определений НФБК, 4НФ и 5НФ:
	
	* переменная отношения R находится в НФБК тогда и только тогда, когда каждая
	 функциональная зависимость, удовлетворяемая переменной отношения R,
	 определяется ее потенциальными ключами;
	* переменная отношения R находится в 4НФ тогда и только тогда, когда каждая
      многозначная зависимость, удовлетворяемая переменной отношения R, 
      определяется ее потенциальными ключами;
	* переменная отношения R находится в 5НФ тогда и только тогда, когда каждая
	  зависимость соединения, удовлетворяемая переменной отношения R, опреде
	  ляется ее потенциальными ключами.
	  
Аномалии обновления были вызваны именно теми функциональными зависимостями, 
многозначными зависимостями или зависимостями соединения, которые не 
определялись потенциальными ключами.

(Подразумевается, что все упомянутые здесь
функциональные, многозначные зависимости и зависимости соединения являются
нетривиальными.)


### ОБЩИЕ СВЕДЕНИЯ О ДЕНОРМАЛИЗАЦИИ

До сих пор в этой (и предыдущей) главе в основном предполагалось, что полная 
нормализация вплоть до 5НФ весьма желательна.
Но на практике часто можно слышать утверждения, что для достижения высокой 
производительности системы иногда следует выполнить денормализацию. При этом 
используются доводы, подобные перечисленным ниже.

1. Полная нормализация приводит к появлению большого количества логически не
зависимых переменных отношения (и предполагается, что рассматриваемые переменные
отношения являются базовыми).

2. Большое количество логически независимых переменных отношения приводит к
появлению большого количества отдельно хранимых физических файлов.

3. Большое количество отдельно хранимых физических файлов приводит к появлению
 большого количества операций ввода-вывода.

Строго говоря, эти доводы, конечно же, не верны, поскольку (как многократно 
отмечалось в данной книге) в определении реляционной модели нигде не 
утверждается, что базовые переменные отношения должны находиться во взаимно-
однозначном соответствии с хранимыми файлами. Поэтому денормализацию в случае 
необходимости следует выполнять на уровне хранимых файлов, но не на уровне 
базовых переменных отношения.

Однако в некотором отношении эти доводы все же верны для современных продуктов
SQL, поскольку именно в них эти два уровня не разделены в требуемой степени. 

#### Общее определение денормализации

Напомним, что нормализация переменной отношения R означает ее замену множеством 
таких проекций Rl, R2, ..., Rn, что результатом обратного соединения проекций
Rl, R2, ..., Rn обязательно будет значение R. Конечной целью нормализации 
является сокращение степени избыточности данных за счет приведения проекций 
Rl, R2, ..., Rn к максимально высокому уровню нормализации.

Теперь можно перейти к определению понятия денормализации. Пусть Rl, R2, Rn
является множеством переменных отношения. Тогда денормализацией этих переменных
отношения называется такая замена переменных отношения их соединением R, что для
всех возможных значений i (где i = 1, ..., п) выполнение проекции R по атрибутам
Ri обязательно снова приводит к созданию значений Ri.
 
Конечной целью денормализации является увеличение степени избыточности данных за
счет приведения переменной отношения R к более низкому уровню нормализации по
сравнению с исходными переменными отношения Rl, R2, ..., Rn. Точнее, 
преследуется цель сократить количество соединений,
которые потребуется выполнять в приложении на этапе прогона,
поскольку (в действительности) некоторые из этих соединений уже выполнены 
заранее в составе работ по проектированию базы данных.

В случае денормализации прежний подход (применявшийся при нормализации), 
созданный на основании строго научной и логичной теории, заменяется чисто 
прагматическим и субъективным подходом.

Второе очевидное затруднение связано с проблемами избыточности и аномалиями
обновления, которые возникают из-за того, что приходится иметь дело с не 
полностью нормализованными переменными отношения. 

Самая главная, проблема формулируется следующим образом. (Это относится к 
"правильной" денормализации, т.е. к денормализации, которая выполняется
только на физическом уровне, а также к тому типу денормализации, которую иногда
приходится осуществлять в современных продуктах SQL.) Когда речь идет о том, что
денормализация "способствует достижению высокой производительности", фактически
подразумевается, что она способствует достижению высокой производительности 
некоторых конкретных приложений.
 
Любая выбранная физическая структура, которая прекрасно подходит для одних 
приложений с точки зрения их производительности, может оказаться совершенно 
непригодной для других. Например, предположим, что каждая базовая переменная 
отношения отображается на один физически хранимый файл, а каждый хранимый файл 
состоит из физически смежного набора хранимых записей, по одной для каждого 
кортежа соответствующей переменной отношения.


### Транзакции

>Транзакция — это логическая единица работы, а также единица
восстановления

>Свойства ACID транзакций
Заключение, что транзакции обладают (или должны обладать!) четырьмя важными
свойствами: неразрывностью (atomicity), правильностью6 (correctness), 
изолированностью (isolation) и устойчивостью (durability). 
Этот набор свойств принято называть свойствами ACID (по первым буквам их 
английских названий).

* Неразрывность. Транзакции неразрывны (выполняются по принципу "все или ни
чего").
* Правильность. Транзакции преобразуют базу данных из одного правильного со
стояния в другое; при этом правильность не обязательно должна обеспечиваться
на всех промежуточных этапах.
* Изолированность. Транзакции изолированы одна от другой. Таким образом, даже
если будет запущено множество транзакций, работающих параллельно, результаты
любых операций обновления, выполняемых отдельной транзакцией, будут скрыты
от всех остальных транзакций до тех пор, пока эта транзакция не будет зафиксиро
вана. Иначе говоря, для любых отдельных транзакций А и В справедливо следую
щее утверждение: транзакция А сможет получить результаты выполненных тран
закцией в обновлений только после фиксации транзакции в, а транзакция в смо
жет получить результаты выполненных транзакцией А обновлений только после
фиксации транзакции А.
* Устойчивость. После того как транзакция зафиксирована, выполненные ею 
обновления сохраняются в
базе данных на постоянной основе, даже если в дальнейшем произойдет аварийный 
останов системы

### Выводы:

Общее назначение процесса нормализации заключается в следующем:
* исключение некоторых типов избыточности;
* устранение некоторых аномалий обновления;
* разработка проекта базы данных, который является достаточно "качествен
  ным" представлением реального мира, интуитивно понятен и может служить
  хорошей основой для последующего расширения;
* упрощение процедуры применения необходимых ограничений целостности.

Понятия зависимости и дальнейшей нормализации по своему характеру являются 
семантическими, т.е. они связаны со смыслом данных, тогда как реляционная 
алгебра и реляционное исчисление, а также построенные на их основе языки 
наподобие SQL, наоборот, имеют дело со значениями данных и не требуют (да и 
не могут требовать) выполнения нормализации выше первого уровня. Рекомендации
по выполнению дальнейшей нормализации должны рассматриваться прежде всего 
как методика, позволяющая разработчику базы данных (и, следовательно, ее 
пользователю) выразить определенную часть семантики реального мира 
(пусть даже небольшую) в простой и понятной форме.

Сам я практически наглядно подтвердил себе, что 3НФ вполне достаточно, а 
возможно даже и 2НФ. Так как при 3НФ уже приходится для получения информации 
обращаться к нескольким таблицам.

Пока пожалуй на этом остановлюсь, но чувствую что время от времени придется 
возможно перечитывать главы из книги К.Дж. Дейта "Введение в системы баз 
данных".

### Ресурсы:

[Введение в системы баз данных К.Дж.Дейт](
http://www.ozon.ru/context/detail/id/136880774/)

[SQL Tutorial](https://www.w3schools.com/sql/)

[SQL для простых смертных](https://www.ozon.ru/context/detail/id/6577098/)

[Описание основных приемов нормализации базы данных](https://support.microsoft.com/ru-ru/help/283878/description-of-the-database-normalization-basics)

[Проектирование базы данных MySQL](http://addphp.ru/materials/mysql/1_3.php)

[www.postgresqltutorial.com](http://www.postgresqltutorial.com)

[tutorialspoint.com](https://www.tutorialspoint.com/postgresql)

[https://yuml.me](https://yuml.me)

[dbdesigner.net](http://dbdesigner.net/designer/schema/99345)

[Нормализация отношений. Шесть нормальных форм](https://habrahabr.ru/post/254773/)