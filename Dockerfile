FROM python:3.11-slim-bullseye
ARG FUNCTION_DIR="/function"
ENV FUNCTION_DIR=${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

RUN pip install --upgrade pip
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

COPY setup.py ${FUNCTION_DIR}
COPY cgt_map_backend ${FUNCTION_DIR}/cgt_map_backend
COPY requirements.txt ${FUNCTION_DIR}
RUN pip install -r requirements.txt

COPY /app/* ${FUNCTION_DIR}/

ENTRYPOINT [ "python3", "-m", "awslambdaric" ]
CMD [ "app.handler" ]