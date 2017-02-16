#!/bin/bash

source ~/.profile

python networkGen.py
scp -i ~/.ssh/brennan-young.pem network.csv ubuntu@ec2-52-33-88-184.us-west-2.compute.amazonaws.com:~/Cerebrate/cerebrate/StreamProcessing/src/main/resources
scp -i ~/.ssh/brennan-young.pem supplies.csv ubuntu@ec2-52-33-88-184.us-west-2.compute.amazonaws.com:~/Cerebrate/cerebrate/StreamProcessing/src/main/resources