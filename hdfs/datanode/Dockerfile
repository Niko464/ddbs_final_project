FROM custom_hadoop_base

ADD run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]

# CMD ["tail", "-f", "/dev/null"]
#hdfs", "--daemon", "start", "datanode", ";", 