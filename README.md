# httpenv

A very simple service serving environment variables over HTTP. It's basically in memory registry for variables. The service exposes only two endpoints:

- `GET /v1/add/<name>/<value>` - adds a variable to registry
  + `name` is the name of variable to add in registry
  + `value` is the value of the variable
- `GET /v1/<name>` - retrieves variable from the registry
  + `name` is the name of the added variable

## Usage

The possible usage is to pass secret variables to `docker build` command in a continuous integration. Here is an example how to do that with Gitlab CI to pass credentials for your own [PyPI cloud](https://pypi.org/project/pypicloud/) (but you could use it for any other service):

```yaml
docker_build:
  stage: build
  image: docker:stable
  services:
    - name: kiwicom/httpenv
      alias: httpenv
  script:
    - export HE=$(getent hosts httpenv|awk '{print $1}')
    - wget -qO- http://httpenv/v1/add/PYPI_USERNAME/${PYPI_USERNAME}
    - wget -qO- http://httpenv/v1/add/PYPI_PASSWORD/${PYPI_PASSWORD}
    - docker build . --add-host=httpenv:$HE
```

In this case, the `Dockerfile` being built would have some parts of code like in the following example:

```dockerfile
FROM python

RUN echo "machine pypi.example.com" >> ~/.netrc && \
    echo "  login $(curl -sS http://httpenv/v1/PYPI_USERNAME)" >> ~/.netrc && \
    echo "  password $(curl -sS http://httpenv/v1/PYPI_PASSWORD)" >> ~/.netrc && \
    chmod 600 ~/.netrc && \
    pip install -e . && \
    rm ~/.netrc

COPY . /app/

CMD ["sh"]
```

Note that the `.netrc` file is a file for storing credentials and is read by `pip`.
