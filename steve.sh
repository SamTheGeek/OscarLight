start=10
c=$start
inc=2
while [[ $c -lt 800 ]] ; do 
	echo -e "7=$c\n6=$c\n5=$c\n4=$c\n1=$c" > /dev/servoblaster; 
	c=$(($c+$inc)); 
	sleep 0.001
done
while [[ $c -gt $start ]] ; do 
	echo -e "7=$c\n6=$c\n5=$c\n4=$c\n1=$c" > /dev/servoblaster; 
	c=$(($c-$inc)); 
	sleep 0.001
done
