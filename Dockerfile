FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
RUN chown root:root /code
RUN chmod 755 /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/