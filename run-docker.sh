#!/bin/bash

# This script runs the Docker container with mounted volume and port forwarding
sudo docker run --publish 8000:8000 -it -v /home/zuegelwagen/videoflix-backend:/usr/src/app videoflix bash
