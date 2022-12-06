FROM centos

RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

RUN yum -y install net-tools initscripts java-1.8.0-openjdk-devel wget

#install Hadoop
RUN wget http://apache.mirrors.pair.com/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz
RUN tar -xzf hadoop-3.3.4.tar.gz
RUN rm -f hadoop-3.3.4.tar.gz
RUN mv hadoop-3.3.4 /usr/local/hadoop/

RUN mkdir /data

#move config files
ADD core-site.xml /usr/local/hadoop/etc/hadoop/core-site.xml
ADD hdfs-site.xml /usr/local/hadoop/etc/hadoop/hdfs-site.xml

#set la variable d'environnement JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk/
ENV PATH="$PATH:/usr/local/hadoop/bin:/usr/local/hadoop/sbin"