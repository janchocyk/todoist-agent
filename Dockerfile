FROM python:3.11.7-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    CUDA_VISIBLE_DEVICES=0 \
    ROOT_DIR="/" \
    APP_DIR="/app" \
    MODULE_DIR="/module" \
    ACCEPT_EULA=Y

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    gnupg2 \
    poppler-utils && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    apt-get install -y msodbcsql18 mssql-tools18 unixodbc-dev libgssapi-krb5-2 && \
    echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

COPY Dockerfile *app/requirements* $APP_DIR/
COPY Dockerfile *module/requirements* $MODULE_DIR/

RUN pip install --upgrade uv
RUN if [ -f $APP_DIR/requirements.txt ]; then uv pip install -r $APP_DIR/requirements.txt --extra-index-url  https://repo.assecobs.pl/repository/pre-cloud-pypi/simple --system; fi
RUN if [ -f $MODULE_DIR/requirements.txt ]; then uv pip install -r $MODULE_DIR/requirements.txt --extra-index-url  https://repo.assecobs.pl/repository/pre-cloud-pypi/simple --system; fi

COPY app $APP_DIR
COPY module $MODULE_DIR

RUN if [ -f $APP_DIR/setup.py ]; then uv pip install ./app --extra-index-url  https://repo.assecobs.pl/repository/pre-cloud-pypi/simple --system; fi
RUN if [ -f $MODULE_DIR/setup.py ]; then uv pip install ./module --extra-index-url  https://repo.assecobs.pl/repository/pre-cloud-pypi/simple --system; fi

WORKDIR $ROOT_DIR

ENTRYPOINT ["python", "-m", "app"]
