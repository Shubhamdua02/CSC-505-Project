#!/bin/sh
unzip csc505-spring-2022-main.zip
mv csc505-spring-2022-main/Project1/A .
mv csc505-spring-2022-main/Project1/B .
mv csc505-spring-2022-main/Project1/C .
rm -r csc505-spring-2022-main
cd C/
gunzip *.gz
cd ..
cd B/
gunzip *.gz
cd ..
cd A/
gunzip *.gz