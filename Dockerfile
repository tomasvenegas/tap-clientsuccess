FROM python:3.9.1

WORKDIR /usr/src/app

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./
COPY ./tap_clientsuccess tap_clientsuccess
RUN poetry install

ENTRYPOINT [ "poetry", "run", "tap-clientsuccess" ]
CMD [ "--help" ]
