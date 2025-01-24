#!/bin/bash

FAN_PIN=6

gpio -g mode $FAN_PIN out
if [ "$1" == "on" ]; then
    gpio -g write $FAN_PIN 1
    echo "Fan turned ON"
elif [ "$1" == "off" ]; then
    gpio -g write $FAN_PIN 0
    echo "Fan turned OFF"
else
    echo "Invalid command. Use 'on' or 'off'."
    exit 1
fi
