"""
装饰器本质上是一个Python的函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外的功能
装饰器的返回值是一个函数对象，它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景
有了装饰器，我们就可以抽离大量与函数功能本身无关的雷同代码并继续重用
简单地说：就是给已有的函数添加额外的功能
"""
#sample case
def foo():
    print("I'am foo")
foo()
print('*'*50)
#现在有个新的需求 每个函数输出的时候 还要输出函数名称
def printName():
    import inspect
    caller = inspect.stack()[1][3]
    print('[DEBUG] : ENTER {}()'.format(caller))
def foo1():
    printName()
    print("I'am foo1")
foo1()
print('*'*50)
#但这样 需要在每个函数里写入printName() 很麻烦。这时候装饰器要登场了
def printName1(func):
    def wrapper():
        print('[DEBUG] : ENTER {}()'.format(func.__name__))
        return func()
    return wrapper
foo = printName1(foo)
foo()
print('*'*50)
#上面的这个就是一个装饰器，当然如果每个装饰器都这么写，很麻烦。有时候理解起来也很困难
#python 提供了语法糖用来简化
@printName1
def foo2():
    print("I'am foo2")
foo2()
print('*'*50)
#那么如果碰到带参数的函数，装饰器也支持参数
def printName2(func):
    def wrapper(*args,**kwargs):
        print('[DEBUG] : ENTER {}()'.format(func.__name__))
        return func(*args,**kwargs)
    return wrapper
@printName2
def foo3(something):
    print("I'am foo3 and want to say :{}".format(something))
foo3('WTF')
print('*'*50)
#高级一点的装饰器
#现在有需求，需要输出函数不但要有函数名 还要有级别，比如之前的debug 或者是production，test
#这就要求装饰器本身也要带参数
def printName3(level):
    def wrapper(func):
        def inner_wrapper(*args,**kwargs):
            print('[{level}] : ENTER {funcName}()'.format(level=level,funcName=func.__name__))
            return func(*args,**kwargs)
        return inner_wrapper
    return wrapper
@printName3(level='production')
def foo4(something):
    print("I'am foo4 and want to say :{}".format(something))
foo4('WTF')
#从这里看出装饰器的参数是在最外层传入的，被修饰的函数本身在第二层传入，函数的参数实在第三层传入的，最后在一层层的返回
print('*'*50)
#装饰器其实是是一个约束接口，他必须接收一个callable的对象作为参数，然后返回一个callable的对象。在python中callabled的对象一般是函数
#但是也有例外，只要某个对象重载了_call_()方法，那么这个对象就是callable的
# class test():
#     def __call__(self):
#         print('call me')
# t = test()
# t()
#那么用类来实现装饰器也是可行的
class printName4(object):
    def __init__(self,level = 'Debug'):
        self.level = level
    def __call__(self, func):
        def wrapper(*args,**kwargs):
            print('[{level}] : ENTER {funcName}()'.format(level=self.level, funcName=func.__name__))
            func(*args, **kwargs)
        return wrapper
@printName4(level='TEST')
def foo5(something):
    print("I'am foo5 and want to say :{}".format(something))
foo5('WTF')
print('*'*50)
#装饰器的坑
def printName5(func):
    def wrapper(*args,**kwargs):
        print('[DEBUG] : ENTER {}()'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper
@printName5
def foo6(something):
    print("I'am foo6 and want to say :{}".format(something))
foo6('WTF')
print(foo6.__name__) #wrapper

print('-'*25)
#用functools.wrap 可以基本解决这个问题
from functools import wraps
def printName6(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print('[DEBUG] : ENTER {}()'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper
@printName6
def foo7(something):
    print("I'am foo7 and want to say :{}".format(something))
foo7('WTF')
print(foo7.__name__)#foo7
# #但是函数的签名还是拿不到
# import inspect
# print(inspect.getargspec(foo7))
print('*'*50)
#一些好用的装饰器包
#decrotate
from decorator import decorate
import datetime
def wrapper(func,*args,**kwargs):
    print("[DEBUG] {}: enter {}()".format(datetime.datetime.now(), func.__name__))
    return func(*args, **kwargs)
def logging(func):
    return decorate(func,wrapper)#运用decorate 可以让装饰器嵌套没那么复杂看起来
@logging
def foo8(something):
    print("I'am foo8 and want to say :{}".format(something))
foo8('WTF')
print('*'*50)
#wrapt 是一个功能完善的包，使用它不用担心获得不了函数名，和源码的问题
import wrapt
@wrapt.decorator
def logging(wrapped,instance,args,kwargs):#instance is must
    print("[DEBUG] {}: enter {}()".format(datetime.datetime.now(), wrapped.__name__))
    return wrapped(*args,**kwargs)
@logging
def foo9():
    print('哈哈')
foo9()
print('*'*50)
#如果需要带参数的可以这么写
def logging(level):
    @wrapt.decorator
    def wrapper(wrapped,instance,args,kwargs):
        print("[{level}] {time}: enter {name}()".format(level=level,time=datetime.datetime.now(), name=wrapped.__name__))
        return wrapped(*args, **kwargs)
    return wrapper
@logging(level='INFO')
def foo10(something):
    print(something)
foo10('WTF')