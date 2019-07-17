FROM python:3.5.3
WORKDIR /Code
RUN pip install --upgrade pip
ADD requirements.txt /Code/
RUN pip install --upgrade asgiref
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
ADD . /Code/
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]