def use_logging(func):
    def wrapper(*args, **kwargs):
        print("%s is running" % func.__name__)
        return func(*args)
    return wrapper

@use_logging
def foo():
    print("i am foo")

# @use_logging
def bar():
    print("i am bar")

bar = use_logging(bar)

bar()

def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("%s is running" % func.__name__)
            return func(*args)
        return wrapper
    return decorator

@use_logging
def foo():
    print("i am foo")

# @use_logging(level='warn')
def bar():
    print("i am bar")
bar = use_logging(level='warn')(bar)

bar()

# class Foo(object):
#     def __init__(self, func):
#         self._func = func
#
#     def __call__(self):
#         print ('class decorator runing')
#         self._func()
#         print('class decorator ending')
#
# # @Foo
# def bar():
#     print('bar')
#
# bar = Foo(bar)
# bar()