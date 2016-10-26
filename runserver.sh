#!/bin/bash

read -n 1 -p  "Do you want this with nohup? <y/N>" prompt
if [[ $prompt == "y" || $prompt == "Y" || $prompt == "YES" || $prompt == "yes" ]] ; then
 nohup python manage.py runserver 0.0.0.0:8082 >> nohup.out &
else
 python manage.py runserver 0.0.0.0:8082
fi
