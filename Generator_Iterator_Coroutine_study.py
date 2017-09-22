"""
1.生成器
2.迭代器
3.协程
"""
#1.生成器 生成器的作用主要是延迟操作，也就是说需要的时候才给结果，不是立即产生结果。遵循了迭代器协议。只能遍历一次
#迭代器协议是指：对象需要提供next方法，它要么返回迭代中的下一项，要么就引起一个StopIteration异常，以终止迭代
# sum([i for i in xrange(10000000000)]) 内存大量占用
# sum(i for i in xrange(10000000000)) 内存基本不占用

"""
生成器：生成器不会把结果保存在一个系列中，而是保存生成器的状态，在每次进行迭代时返回一个值，直到遇到StopIteration异常结束。
生成器表达式：gen = (x**2 for x in range(5))
生成器函数：函数内部有yield则为生成器函数
如果函数里面有return 则今后不再迭代了
如果return 后面带值的话 是StopIteration异常的说明，不是程序的返回值
"""
def odd():#无限奇数的生成器
    n=1
    while True:
        yield n
        n+=2
odd_num = odd()
count = 0
# for o in odd_num:
#     if count >=5: break
#     print(o)
#     count +=1
# exit('生成器')

"""
解释一下：
这个函数的重点在于send
当函数里面有yield是，解释器不在认为这是普通函数，而是生成器函数。
当函数运行到yiled 这个语句时就停止了（可以理解为挂起了，保存状态，和参数）。yield生成一个迭代出来的对象，也就相当于for i in alist 里面的i。
当你下次再迭代时，函数会从上次挂起的地方再次开始继续执行
send()这个方法是给生成器传值，在第一次迭代完成后，receive并没有得到赋值，而在第二次的时候，send（）会把值发给receive
然后判断receive的值，并且充值value的值，并且生成新的迭代对象
"""
def gen():
    value = 0
    while True:
        receive = yield value
        if receive == 'e':
            break
        value = 'got:%s'%receive
g = gen()
# print(g)
# print(g.send(None))
# print(g.send('aaa'))
# print(g.send(3))
# print(g.send('e'))
# exit('python的协程模型')
"""
翻译一下：
因为L是个列表，在一开始L被当做参数运行flatten的时候。
1。会进入 for sublist in nested：在进入for element in flatten flatten(sublist)
这个时候。这个流程在这里就挂起了。在开启一个流程，sublist被放入了flatten ，那么因为L的第一个元素是字符串，会在 if isinstance 那里抛出异常
直接yield 了这个字符串 ,因为yield不是return，element 就是'aaadf' 最后 print('aaaf')。
2.这时候内部的流程结束，外面挂起的流程继续工作，到了sublist = [1,2,3]了，循环这个list 每个元素是数字，也就变成了for element in flatten(1)
这时候外部的流程继续挂起，进入内部流程，flatten（1），1不是字符串，则继续 到了 for sublist in 1：是 因为数字不能当做迭代器，所以会抛出异常，这个异常
恰恰就是typeError，也就是说又会直接yield这个数字，然后打印got：1 。剩下的和上面描述的一样
"""
def flatten(nested):
    try:
        # 如果是字符串，那么手动抛出TypeError。
        if isinstance(nested, str):
            raise TypeError
        for sublist in nested:
            for element in flatten(sublist):
                yield element
                print('got:', element)
    except TypeError:
        print('here')
        yield nested

L = ['aaadf', [1, 2, 3], 2, 4, [5, [6, [8, [9]], 'ddf'], 7]]
# for num in flatten(L):
#     print(num)
# for item in flatten(['dsdsdsddg',23]):
#     print(item)
# exit('多维列表扁平化')

#迭代器 为了方便循环 遵循了迭代器协议
"""
可迭代对象：一个可以被for in 循环的对象就是可迭代对象(Iterable) 如：list，tuple，str等
迭代器：一个可以被next()函数调用并不断的返回下一个值（直到碰到StopIteration异常）的叫做迭代器(Iterator)
所有的可迭代对象 都可以通过内置的iter()方法转化成迭代器
迭代器是继承自可迭代对象 ，而可迭代对象继承自内置的object对象
也就说 next() 方法是迭代器独有的，iter()是两个类都有的
for in 循环在内部事实上就是先调用了iter()把iterable转化成iterator的
"""
lista = [1,2,3,4,5]
try:
    next(lista) #会报错 证明list只是可迭代对象 没有next方法
except TypeError as error:
    print(str(error))
Lista = iter(lista) #将list转换为可迭代对象
counts = 0
# while counts <5:
#     print(next(Lista)) #就可以迭代了
#     counts+=1
"""
迭代器是一次性消耗品，使用完了就空了
我们可以通过copy包中提供的deepCopy来完成赋值 （浅拷贝只能把外层拷贝，而深拷贝可以把里面的对象也拷贝）
最后注意一下：迭代器是不能回退的，开始迭代不能回到刚开始
"""
listb = [1,2,3]
I = iter(listb)
from copy import deepcopy
J = deepcopy(I)
for i in I:
    print(i,end='~~~')
try:
    print(next(I),end='----')#无法再次使用I了
except:
    #如果需要复制得深拷贝
    print(next(J),end='----')

#协程
"""
协程 又称为为微线程。
子程序或者称为函数，在所有语言中都是层级调用的，比如A调用B,B调用C，C执行完返回，B执行完返回，最后A执行完毕
子程序是通过栈完成的（先进后出），它总是调用总是一个入口，一次返回。顺序明确
协程和子程序不同，协程在python 看着和子程序也就是函数很像，但是，协程是可以在内部中断的，去执行别的子程序，在适当的时候返回
子程序或者说函数 只是协程的一种特例
"""
import time
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('消费者正在消费...%s'%n)
        time.sleep(1)
        r = '200 OK'

def producer(c):
    next(c)#开启消费
    n = 0
    while n < 5:
        n = n+1
        print('生产者正在生产....%s'%n)
        r = c.send(n)
        print('消费者返回状态...%s'%r)
    c.close()
aConsumer = consumer()
producer(aConsumer)
