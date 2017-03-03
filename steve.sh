#! /bin/bash

start=10
max=800
c=$start
inc=2
while [[ $c -lt $max ]] ; do 
	echo -e "7=$c\n6=$c\n5=$c\n4=$c\n1=$c" > /dev/servoblaster; 
	c=$(($c+$inc)); 
	sleep 0.001
done
while [[ $c -gt $start ]] ; do 
	echo -e "7=$c\n6=$c\n5=$c\n4=$c\n1=$c" > /dev/servoblaster; 
	c=$(($c-$inc)); 
	sleep 0.001
done
