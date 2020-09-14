#!/usr/bin/env bash

apt-get install apt-transport-https ca-certificates gnupg software-properties-common wget

wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null

add-apt-repository ppa:snaipewastaken/ppa
apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'

apt-get update

apt-get install -y python3 python3-pip gcc cmake
apt-get install -y criterion-dev

pip3 install -r /autograder/source/requirements.txt
