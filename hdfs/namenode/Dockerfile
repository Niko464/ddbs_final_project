FROM custom_hadoop_base

ENV namedir /data

COPY run.sh ./run.sh
RUN chmod a+x ./run.sh

CMD ["sh", "./run.sh"]