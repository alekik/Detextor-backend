FROM python:3.10-slim as python-base

    # - python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # - pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # - poetry
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # - paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.3.2
RUN curl -sSL https://install.python-poetry.org | python -

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-root --only main

FROM python-base as production
ENV DETEXTOR_ENV=prod

COPY --from=builder-base $VENV_PATH $VENV_PATH

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR ./
COPY . .
RUN chmod +x /docker-entrypoint.sh

EXPOSE 3000
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["gunicorn", "--log-level", "INFO", "-b", ":3000", "-t", "120", "run:APP"]

