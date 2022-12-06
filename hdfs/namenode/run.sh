#!/bin/bash

if [ "`ls -A $namedir`" == "" ]; then
  echo "Formatting namenode name directory: $namedir"
  hdfs namenode -format
fi

hdfs --daemon start namenode

sleep infinity