import time
import asyncio
'''
#定义一个协程
"""定义一个协程就像定义一个普通函数一样，只是在def 前面会用async关键字"""
now = lambda :time.time()
async def do_some_work1(x): #定义一个协程
    print('Waiting: ',x)
start = now()
coroutine = do_some_work1(1) #创建一个协程
loop = asyncio.get_event_loop()#创建时间循环
loop.run_until_complete(coroutine) #注册协程到时间循环，run_until_complete会把协程包装成一个task ，并启动循环
print('Time: ',now()-start)
print('*****'*10)
#task
"""协程是不能直接运行的，它会生成一个coroutine对象。所以需要run_until_complete包装成task，task是future类的子类。用来保存协程运行后的状态"""
async def do_some_word2(x):
    print('Waiting: ', x)
start = now()
coroutine = do_some_word2(2)
loop = asyncio.get_event_loop()
task = loop.create_task(coroutine)
#task = asyncio.ensure_future(coroutine)  这个也能创建task
print(task)#这个task的状态是pending 在等待的
loop.run_until_complete(task)
print(task)#这个task的状态是finished，完成
print('Time: ',now()-start)
print('*****'*10)
#绑定回调
"""在task执行完毕后可以回去执行的结果，回调的最后一个参数是futured对象，通过这个对象可以获取协程返回值"""
async def do_some_word3(x):
    print('Waiting: ', x)
    return ('Done after {}s'.format(x))

def callback3(future):
    print('Callback: ',future.result())
start = now()
coroutine = do_some_word3(3)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
#绑定回调 在task执行完后执行。
# task.add_done_callback(callback3)
loop.run_until_complete(task)
#不用回调试一下
if task.done:
    print(task.result())
print('Time: ',now()-start)
print('****'*10)
#阻塞和await
"""使用await可以对耗时操作进行挂起，就像生成器里的yield 函数让出控制权。在协程里遇到await 时间循环将会挂起该协程，执行别的协程"""
async  def do_some_word4(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return ('Done after {}s'.format(x))
start = now()
coroutine = do_some_word4(4)
loop = asyncio.get_event_loop()
task = loop.create_task(coroutine)
loop.run_until_complete(task)
print('Task ret: ', task.result())
print('TIME: ', now() - start)
print('****'*10)
#并发和并行
"""
并发：多个任务同时执行   一个老师同时辅导多个学生
并行：同一时刻多个任务执行 多个老师分别同时辅导多个学生
python 因为GIL的存在，无法实现真正意义上的多线程，所以这里用多个协程来完成并发，每当有任务阻塞的时候就用await，其他协程继续工作
"""
async def do_some_work5(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)
start = now()
coroutine1 = do_some_work5(1)
coroutine2 = do_some_work5(2)
coroutine3 = do_some_work5(4)
tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3)
]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
for task in tasks:
    print('Task ret: ', task.result())
print('TIME: ', now() - start)#这个执行时间和重要 总共花了4秒 如果按照正常时间应该是等待1+2+4=7秒的，但是因为在coroutine3挂起的时候，
#在等待的4s中，coroutine1和2都已经结束挂起，并且完成任务了。所以他们是并发执行的
print('****'*10)
#协程嵌套
async def do_some_work6(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)
async def main():
    coroutine1 = do_some_work6(1)
    coroutine2 = do_some_work6(3)
    coroutine3 = do_some_work6(6)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    # dones,pendings = await asyncio.wait(tasks)
    # print(dones)
    # for done in dones:
    #     print('Task ret: ', done.result())
    for done in asyncio.as_completed(tasks):
        done = await done
        print('Task ret: ', done)
start = now()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print('TIME: ', now() - start)
print('*****'*10)
#case
async def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))


'''


@asyncio.coroutine
def hello1():
    print('Hello world! (%s)' % '1')
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % '1')
def hello2():
    print('Hello world! (%s)' % '2')
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % '2')
"""
这个例子说明了当一个循环正在处理事件的时候，如果遇到await 另一个协程，则立即挂起，去执行其他排队的事件，等到处理完了，第一个协程结果返回了，便取消
挂起状态，继续运行
"""
loop = asyncio.get_event_loop()
tasks = [hello1(), hello2()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()