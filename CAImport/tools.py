import concurrent.futures


# ********************
# I copied isIter function from:
# https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
def isIter(obj):
    try:
        return iter(obj)
    except TypeError as te:
        return False
# ********************


def isDict(o):
    try:
        return getattr(o, 'keys')
    except Exception:
        return False


def dictConverter(obj):

    def convert(o):
        ret = []
        for k in o:
            ret.append((('k', k), ('v', o[k])))
        return ret

    def extractItems(o):
        ret = []
        for i in o:
            ret.append(
                convert(i)
                if isDict(i)
                else extractItems(i)
                if isIter(i)
                else i
            )
        return ret

    assert isIter(obj)
    return convert(obj) \
        if isDict(obj) else extractItems(obj)


def hasInstancecheck(__instance):
    try:
        isinstance(object, __instance)
        return True
    except Exception as e:
        return False


def getAttrs(objects, attrName):
    for obj in objects:
        yield getattr(obj, attrName)


def setAttrs(objects, attrName, attrValue):
    for obj in objects:
        setattr(obj, attrName, attrValue)


def retThread(func, *args, **kwargs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return executor.submit(func, *args, **kwargs).result()


def exceptLoop(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return exceptLoop(func, *args, **kwargs)
