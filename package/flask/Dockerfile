FROM python:3.6.6

ADD . /www
WORKDIR /www

RUN python -m pip install --upgrade pip 

RUN apt-get update && \
    apt-get install dialog apt-utils -y && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get install -y vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN wget --quiet https://dlcdn.apache.org/spark/spark-3.0.3/spark-3.0.3-bin-hadoop2.7.tgz && \
    tar -xvzf spark-3.0.3-bin-hadoop2.7.tgz && \
    mv spark-3.0.3-bin-hadoop2.7 /opt/spark


ENV SPARK_HOME /opt/spark/
RUN export SPARK_HOME

ENV PATH $PATH:/opt/spark/bin:/opt/spark/sbin
RUN export PATH

COPY graphframes-0.8.1-spark3.0-s_2.12.jar /www/graphframes-0.8.1-spark3.0-s_2.12.jar

ENV PYTHONPATH $PYTHONPATH:/opt/spark/python:/opt/spark/python/lib/py4j-0.10.7-src.zip:/usr/local/lib/python3.6/site-packages/graphframes
RUN export PYTHTHONPATH

ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info --jars /www/graphframes-0.8.1-spark3.0-s_2.12.jar --py-files /www/graphframes-0.8.1-spark3.0-s_2.12.jar
ENV PYSPARK_SUBMIT_ARGS --master local[*] pyspark-shell --jars /www/graphframes-0.8.1-spark3.0-s_2.12.jar --py-files /www/graphframes-0.8.1-spark3.0-s_2.12.jar


COPY graphframes-0.8.1-spark3.0-s_2.12.jar /opt/spark/jars/graphframes-0.8.1-spark3.0-s_2.12.jar


RUN pip3 install Flask
RUN pip3 install uwsgi
RUN pip3 install -r requirements.txt
RUN pip3 install graphframes
RUN pip3 install findspark

CMD uwsgi uwsgi.ini


