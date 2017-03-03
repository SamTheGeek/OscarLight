#! /bin/bash

# run this first, if newly rebooted
#sudo servod --min=0 --max=100%

start=10
max=400
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
