#!/bin/bash

source ~/.profile

python networkGen.py
scp -i ~/.ssh/brennan-young.pem network.json ubuntu@ec2-35-162-123-34.us-west-2.compute.amazonaws.com:~
scp -i ~/.ssh/brennan-young.pem network.json ubuntu@ec2-35-161-11-7.us-west-2.compute.amazonaws.com:~
scp -i ~/.ssh/brennan-young.pem network.json ubuntu@ec2-35-163-48-63.us-west-2.compute.amazonaws.com:~


scp -i ~/.ssh/brennan-young.pem networkGraph.txt ubuntu@ec2-52-10-155-148.us-west-2.compute.amazonaws.com:~/cerebrate/Web

scp -i ~/.ssh/brennan-young.pem ~/Downloads/build.zip ubuntu@ec2-52-10-155-148.us-west-2.compute.amazonaws.com:~/cerebrate/Web