FROM python:3.7
ENV PYTHONUNBUFFERED=1
EXPOSE 8848
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install uwsgi==2.0.20 -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt update
RUN apt install libgl1-mesa-glx -y
ADD . /code
CMD ["bash", "run.sh"]

