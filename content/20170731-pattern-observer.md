Title: Паттерн НАБЛЮДАТЕЛЬ
Category: Blog
Tags: OOP, Patterns, Observer

Паттерн НАБЛЮДАТЕЛЬ определяет отношение "один ко многим" между объектами таким
образом, что при изменении состояния одного объекта происходит автоматическое
оповещение и обновление всех зависимых объектов.

Схема данного определения может выглядеть примерно так.   
 
![observer_schema.png]({static}/images/observer_schema.png)

Есть субъект (Subject) и объекты-наблюдатели (Object) которые определяют 
отношение "один ко многим". Наблюдатели зависят от субъекта - при 
изменении состояния последнего наблюдатели получают оповещения. 

Данный паттерн еще называют Publisher-Subscriber (издатель-подписчик), поскольку
отношения издателя и подписчиков характеризуют действие данного паттерна: 
подписчики подписываются email-рассылку определенного сайта. 
Сайт-издатель с помощью email-рассылки уведомляет всех подписчиков о изменениях.
А подписчики получают изменения и производят определенные действия: могут зайти 
на сайт, могут проигнорировать уведомления и т.д.

Паттерн наблюдатель строится на основе классов, реализующих интерфейсы 
субъекта и наблюдателя.

Диаграмма классов выглядит вот так:

![observer_uml.png]({static}/images/observer_uml.png)

Итак, каждый субъект может иметь много наблюдателей. Каждый потенциальный 
наблюдатель должен реализовать интерфейс Observer который содержит 
единственный метод update() который вызывается при изменении состояния субъекта.
Класс ConcreteObserver реализация интерфейса Observer, каждый наблюдаетль 
регистрируется у конкретного субьекта для получения обновлений.

Субьект реализует интерфейс Subject. Кроме методов регистрации, удаления, 
субъект также реализует метод notifyObservers() оповещающий всех текущих 
наблюдателей об изменении состояния.
Субъект также может иметь методы set- и get- для изменения состояния.

На базе слабосвязанных архитектур строятся гибкие ОО-системы, которые хорошо 
адаптируются к изменениям благодаря минимальным зависимостям между оъектами.

Опишем данные интерфейсы наблюдателя и субъекта. В реализации конкретного 
класса субъекта представим что у нас есть класс абстракция некоего шлагбаума,
 который перекрывает движение и он будет рассылать всем наблюдателям свое 
 состояние открыто-закрыто.

```python
from abc import ABCMeta, abstractmethod

class ISubject(metaclass=ABCMeta):
    
    @abstractmethod
    def registerObserver(self, observer):
        raise NotImplementedError()
        
    @abstractmethod 
    def removeObserver(self, observer):
        raise NotImplementedError()

    @abstractmethod 
    def notifyObservers(self):
        raise NotImplementedError()


class IObserver(metaclass=ABCMeta):
    @abstractmethod
    def update(self, subject, arg):
        raise NotImplementedError()       


class ConcreteSubject:
    def __init__(self):
        self._observers = []
        self.changed = 0
        self.state = "open"
    
    def registerObserver(self, observer):
        if observer not in self._observers:
            print("Register observer: {0}".format(observer.name))
            self._observers.append(observer)
    
    def removeObserver(self, observer):
        print("Remove observer: {0}".format(observer.name))
        self._observers.remove(observer)
        
    def notifyObservers(self, arg=None):
        '''
        If 'changed' indicates that this object
        has changed, notify all its observers, then
        call clearChanged(). Each observer has its
        update() called with two arguments: this
        observable object and the generic 'arg'.
        '''
        
        if not self.changed:
            return
        observers = self._observers[:]
        for observer in observers:
            observer.update(self, arg)
        self.clearChanged()

    def deleteObservers(self): 
        self._observers = []

    def countObservers(self): 
        return len(self._observers)    
        
    def setChanged(self): 
        self.changed = 1
        
    def clearChanged(self): 
        self.changed = 0
        
    def hasChanged(self): 
        return self.changed
    
    def setState(self, state):
        self.state = state
        self.changed = 1
        self.notifyObservers(arg=self.state)


class ConcreteObserver:
    def __init__(self, name):
        self.name = name
    
    def update(self, observable, arg):
        print("Observer {2} Got update from Subject: {0} with arg: {1}".format
        (observable, arg, self.name))
        print("State (arg) = {0}".format(arg))
        print("State (Subject) = {0}".format(observable.state))
        

observer1 = ConcreteObserver("Observer-1")
observer2 = ConcreteObserver("Observer-2")
observer3 = ConcreteObserver("Observer-3")

subject1 = ConcreteSubject()

subject1.registerObserver(observer1)
subject1.registerObserver(observer2)
subject1.registerObserver(observer3)

subject1.setState("closed")

subject1.removeObserver(observer3)

subject1.setState("opened")
 
       
```

ISubject: представляет наблюдаемый объект (Субъект). 
Определяет три основных метода, необходимых для реализации субъекта: 
- registerObserver() (для добавления наблюдателя), 
- removeObserver() (удаление набюдателя) 
- notifyObservers() (уведомление наблюдателей)

ConcreteSubject: конкретная реализация интерфейса ISubject. 
В этом классе приведена чуть большая реализация чем указано на диаграмме 
классов, добавлены несколько методов.
- Для управления списком наблюдаетелей **self._observers**:
    - deleteObservers() - позволяет очистить список подписчиков-наблюдаетелей
    - countObservers() - возвращает текущее число подписчиков данного обьекта 

- Для управления состянием **self.changed**      
    - setChanged()
    - clearChanged()
    - hasChanged()

- Для тестирования мне нужен метод с помощью которого я смогу менять 
состояние Subject объекта **self.state** (открыт или закрыт шлагбаум), которое 
отсылается всем наблюдателям:
    - setState()

IObserver: представляет интерфейс наблюдателя, который подписывается на все 
уведомления наблюдаемого объекта. Определяет метод update(), который вызывается 
наблюдаемым объектом для уведомления наблюдателя.

ConcreteObserver: конкретная реализация интерфейса IObserver.
Также дополнен для удобства параметром **name** чтобы как то различать 
подписчиков-наблюдателей.

В тестовом коде происходит следующее:
- создание наблюдателей: 
```python
observer1 = ConcreteObserver("Observer-1")
observer2 = ConcreteObserver("Observer-2")
observer3 = ConcreteObserver("Observer-3")

```
- создание субъекта (обьекта за которым ведется наблюдение):
```python
subject1 = ConcreteSubject()
```

- происходит подписка-регистрация на получение обновлений состяния субъекта:
```python
subject1.registerObserver(observer1)
subject1.registerObserver(observer2)
subject1.registerObserver(observer3)

```
- происходит рассылка нового состяния:
```python
subject1.setState("closed")

```
- удаление наблюдателя из списка рассылки:
```python
subject1.removeObserver(observer3)
```

- происходит повторная рассылка нового состояния, видно что observer3 не 
получил ничего так как был удален из списка оповещаемых наблюдателей:
```python
subject1.setState("opened")

```
Вывод выглядит как то так:
```
Register observer: Observer-1
Register observer: Observer-2
Register observer: Observer-3

Observer Observer-1 Got update from Subject: <__main__.ConcreteSubject object at 0x7f2799608710> with arg: closed
State (arg) = closed
State (Subject) = closed

Observer Observer-2 Got update from Subject: <__main__.ConcreteSubject object at 0x7f2799608710> with arg: closed
State (arg) = closed
State (Subject) = closed

Observer Observer-3 Got update from Subject: <__main__.ConcreteSubject object at 0x7f2799608710> with arg: closed
State (arg) = closed
State (Subject) = closed

Remove observer: Observer-3

Observer Observer-1 Got update from Subject: <__main__.ConcreteSubject object at 0x7f2799608710> with arg: opened
State (arg) = opened
State (Subject) = opened

Observer Observer-2 Got update from Subject: <__main__.ConcreteSubject object at 0x7f2799608710> with arg: opened
State (arg) = opened
State (Subject) = opened
```

На данный момент мы используем один из вариантов информирования наблюдателя о
состоянии - это push-модель, при которой наблюдаемый объект передает 
(иначе говоря толкает - push) принудительно данные о своем состоянии, то есть 
передает в виде параметра метода update() наблюдателю.

Альтернативой push-модели является pull-модель, когда наблюдатель вытягивает 
(pull) из наблюдаемого объекта данные о состоянии с помощью дополнительных 
методов.

Переработаем немного код, превратим нашу модель в pull - модель.

- изменим код метода setState, уберем передачу состяния через параметр напрямую:
```python
    def setState(self, state):
        self.state = state
        self.changed = 1
        self.notifyObservers()
```
- добавим метод получения состяния субьекта, чтобы наблюдатель мог сам 
получить состояние у субъекта:
```python
    def getState(self, state):
        return self.state
```

A вот код наблюдателя тоже поменяется, нам нужно чтобы наблюдатель вызывал 
метод **getState()** чтобы узнать состояние (таким образом мы можем 
инкапсулировать значение состояния переменной **state**, сделаем ее приватной
принадлежащей внутренней реализации Subject, что означает что клиенты 
наблюдатели не должны обращаться ко внутреннему состоянию субъекта, а должны
 пользоваться методом **getState()**):

```python
class ConcreteObserver:
    def __init__(self, name):
        self.name = name
    
    def update(self, observable, arg):
        print("Observer {2} Got update from Subject: {0} with arg: {1}".format
        (observable.getState(), arg, self.name))
        print("State (arg) = {0}".format(arg))
        print("State (Subject) = {0}".format(observable.getState()))

```

Полностью код и результат будут выглядеть вот так:

```python

from abc import ABCMeta, abstractmethod

class ISubject(metaclass=ABCMeta):
    
    @abstractmethod
    def registerObserver(self, observer):
        raise NotImplementedError()
        
    @abstractmethod 
    def removeObserver(self, observer):
        raise NotImplementedError()

    @abstractmethod 
    def notifyObservers(self):
        raise NotImplementedError()


class IObserver(metaclass=ABCMeta):
    @abstractmethod
    def update(self, subject, arg):
        raise NotImplementedError()       


class ConcreteSubject:
    def __init__(self):
        self._observers = []
        self.changed = 0
        self._state = "open"
    
    def registerObserver(self, observer):
        if observer not in self._observers:
            print("Register observer: {0}".format(observer.name))
            self._observers.append(observer)
    
    def removeObserver(self, observer):
        print("Remove observer: {0}".format(observer.name))
        self._observers.remove(observer)
        
    def notifyObservers(self, arg=None):
        '''
        If 'changed' indicates that this object
        has changed, notify all its observers, then
        call clearChanged(). Each observer has its
        update() called with two arguments: this
        observable object and the generic 'arg'.
        '''
        
        if not self.changed:
            return
        observers = self._observers[:]
        for observer in observers:
            observer.update(self, arg)
        self.clearChanged()

    def deleteObservers(self): 
        self._observers = []
        
    def setChanged(self): 
        self.changed = 1
        
    def clearChanged(self): 
        self.changed = 0
        
    def hasChanged(self): 
        return self.changed
        
    def countObservers(self): 
        return len(self._observers)    
    
    def setState(self, state):
        self._state = state
        self.changed = 1
        self.notifyObservers()

    def getState(self):
        return self._state


class ConcreteObserver:
    def __init__(self, name):
        self.name = name
    
    def update(self, observable, arg):
        print("Observer {2} Got update from Subject: {0} with arg: {1}".format
        (observable.getState(), arg, self.name))
        print("State (arg) = {0}".format(arg))
        print("State (Subject) = {0}".format(observable.getState()))
        

observer1 = ConcreteObserver("Observer-1")
observer2 = ConcreteObserver("Observer-2")
observer3 = ConcreteObserver("Observer-3")

subject1 = ConcreteSubject()

subject1.registerObserver(observer1)
subject1.registerObserver(observer2)
subject1.registerObserver(observer3)

subject1.setState("closed")

subject1.removeObserver(observer3)

subject1.setState("opened")

```

```
Register observer: Observer-1
Register observer: Observer-2
Register observer: Observer-3
Observer Observer-1 Got update from Subject: closed with arg: None
State (arg) = None
State (Subject) = closed
Observer Observer-2 Got update from Subject: closed with arg: None
State (arg) = None
State (Subject) = closed
Observer Observer-3 Got update from Subject: closed with arg: None
State (arg) = None
State (Subject) = closed
Remove observer: Observer-3
Observer Observer-1 Got update from Subject: opened with arg: None
State (arg) = None
State (Subject) = opened
Observer Observer-2 Got update from Subject: opened with arg: None
State (arg) = None
State (Subject) = opened

```

Как видно теперь Субъект рассылает оповещения о изменении состояния, но не 
рассылает это состояние, а наблюдатели вызывают соответствующий метод Субъекта 
чтобы получить состояние. Таким образом если состояние Субъекта это большой 
обьект с кучей информации, можно реализовать методы которые отдают части этой
информации и таким образом наблюдатели смогут решать какую часть информации им 
интересно получить. 
В книге приведен пример когда Субьект хранит 3 параметра, но не всем клиентам
нужны сразу все 3 параметра, кому то нужен 1 кому то 2. Поэтому реализация 
каждого наблюдателя включает получение только тех данных которые нужны.
 
### Вывод

Паттерн НАБЛЮДАТЕЛЬ это реализация отношений один ко многим. 
Новый принцип проектирования - стремиться к слабой связанности между объектами. 
   

