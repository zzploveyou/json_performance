import time

default_data = {
    "name": "Foo",
    "type": "Bar",
    "count": 1,
    "info": {
        "x": 203,
        "y": 102,
    },
}


def ttt(f, data=None, x=100 * 1000):
    start = time.time()
    while x:
        x -= 1
        foo = f(data)
    return time.time() - start


def profile(serial, deserial, data=None, x=100 * 1000):
    if not data:
        data = default_data
    squashed = serial(data)
    return (ttt(serial, data, x), ttt(deserial, squashed, x))


def test(serial, deserial, data=None):
    if not data:
        data = default_data
    assert deserial(serial(data)) == data


def main_many_times():
    contenders = []

    try:
        import yajl
        contenders.append(('yajl', (yajl.Encoder().encode,
                                    yajl.Decoder().decode)))
    except ImportError:
        pass

    try:
        import ujson
        contenders.append(('ujson', (ujson.dumps, ujson.loads)))
    except ImportError:
        pass

    try:
        import cjson
        contenders.append(('cjson', (cjson.encode, cjson.decode)))
    except ImportError:
        pass

    try:
        import simplejson
        contenders.append(('simplejson', (simplejson.dumps, simplejson.loads)))
    except ImportError:
        pass

    try:
        import json
        contenders.append(('json', (json.dumps, json.loads)))
    except ImportError:
        pass

    for name, args in contenders:
        test(*args)
        x, y = profile(*args)
        print("%-11s serialize: %0.3f  deserialize: %0.3f  total: %0.3f" %
              (name, x, y, x + y))


def main_big_file(size):
    import json
    import ujson

    a = {}
    N = size

    # read big json file.
    start_time = time.time()
    for i in range(N):
        with open("total.json") as f:
            a = json.load(f)
    jr = time.time() - start_time

    start_time = time.time()
    for i in range(N):
        with open("total.json") as f:
            a = ujson.load(f)
    ujr = time.time() - start_time

    # write big json file.
    start_time = time.time()
    for i in range(N):
        with open("total.json", 'w') as f:
            json.dump(a, f, indent=2, ensure_ascii=False, sort_keys=True)
    jw = time.time() - start_time

    start_time = time.time()
    for i in range(N):
        with open("total.json", 'w') as f:
            ujson.dump(a, f, indent=2, ensure_ascii=False, sort_keys=True)
    ujw = time.time() - start_time

    print("\ncomparation between json and ujson[test size: {}]:\n".format(N))
    print("      {:}  {:}".format("Read", "Write"))
    print(" json {:.3f} {:.3f}".format(jr, jw))
    print("ujson {:.3f} {:.3f}".format(ujr, ujw))


if __name__ == '__main__':
    import os
    main_many_times()
    if os.path.exists("total.json"):
        main_big_file(size=10)
