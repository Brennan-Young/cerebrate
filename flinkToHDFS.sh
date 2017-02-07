#!/bin/bash

hdfs dfs -rm /test/* 
hdfs dfs -copyFromLocal ~/Cerebrate/cerebrate/StreamProcessing/src/main/resources/network.csv /test
hdfs dfs -copyFromLocal ~/Cerebrate/cerebrate/StreamProcessing/src/main/resources/supplies.csv /test