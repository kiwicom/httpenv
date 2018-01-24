from bottle import request, route, run


@route('/v1/<name>')
def v1(name):
    return envs.get(name, '')


@route('/v1/add/<name>/<value>')
def v1_add(name, value):
    envs[name] = value


if __name__ == '__main__':
    envs = {}
    run(host='0.0.0.0', port=80, quiet=True)
