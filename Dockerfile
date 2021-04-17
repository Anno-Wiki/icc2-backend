FROM python
WORKDIR /code

ENV FLASK_APP icc2.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["./entrypoint.sh"]
