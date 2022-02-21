#!/bin/bash

#sudo docker login docker.io -u kmjeon -p # Type yourself

sudo docker commit SE_engine audio_engine:SE_engine
sudo docker tag audio_engine:SE_engine intflow/audio_engine:SE_engine
sudo docker push intflow/audio_engine:SE_engine
