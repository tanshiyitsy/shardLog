for port in  $(seq 5000 5400)
do
	pid=$(lsof -i:$port | awk '{print $2}'| awk 'NR==2')
	if [  -n  "$pid"  ];  then
		sudo kill  -9  $pid;
	fi
done
