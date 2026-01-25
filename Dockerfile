FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY pyproject.toml ./
COPY src ./src

RUN python -m pip install --upgrade pip \
    && python -m pip install .

CMD ["windtrend.handler.handler"]
