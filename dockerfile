FROM python:3.9
WORKDIR /app
COPY requirments.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirments.txt
COPY script.sh .
RUN chmod 777 script.sh
COPY ./compiler ./compiler
COPY ./webClient ./webClient
CMD ./script.sh