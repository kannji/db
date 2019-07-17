FROM python:3.7.4-slim-buster

WORKDIR /kannji

COPY setup.py .
COPY db db/
RUN pip install .

ENTRYPOINT ["python"]

