#!/bin/bash
#X11

#sudo docker login docker.io -u kmjeon -p # Type yourself

#sudo bash attach_NAS_ftp.sh
sudo xhost +local:root

#Mount Data folders
sudo mkdir /DL_data_big
sudo mount 192.168.0.18:/DL_data_big /DL_data_big
#sudo mount 192.168.0.14:/NAS1 /NAS1

#Pull update docker image
sudo docker pull intflow/audio_engine:SE_engine
#sudo docker pull intflow/nvidia-odtk:20.03_v0.1_2080x8_24

#Run Dockers for CenterNet+DeepSORT
sudo docker run --name SE_engine \
--gpus all --rm \
--mount type=bind,src=/home/intflow/works,dst=/works \
--mount type=bind,src=/DL_data_big,dst=/data \
--net=host \
--privileged \
--ipc=host \
-it intflow/audio_engine:SE_engine /bin/bash
#-it intflow/nvidia-odtk:20.12_lm3_p /bin/bash
#-it intflow/nvidia-odtk:20.03_v0.1_3090x2_63 /bin/bash


