FROM python:3.11-slim-bullseye
ARG FUNCTION_DIR="/function"
ENV FUNCTION_DIR=${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

RUN pip install --upgrade pip
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install mangum

COPY pyproject.toml ${FUNCTION_DIR}
COPY app ${FUNCTION_DIR}/app
COPY requirements.txt ${FUNCTION_DIR}
RUN pip install -r requirements.txt

COPY /lambda_app/* ${FUNCTION_DIR}/

ENTRYPOINT [ "python3", "-m", "awslambdaric" ]
CMD [ "lambda_app.handler" ]