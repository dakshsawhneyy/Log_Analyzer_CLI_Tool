#!/bin/bash

log_file="/var/log/auth.log"

mkdir -p logs

KEYWORDS="error|fail|critical|invalid"

time_stamp=$(date +"%d-%m-%Y")

tail -F "$log_file" | grep --line-buffered -Ei "$KEYWORDS" >> "logs/filtered_${time_stamp}.log"