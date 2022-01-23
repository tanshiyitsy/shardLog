python3 genMapTable.py
cd ./Logger
python3 main.py &
sleep 10
echo "run logSyatem"
cd ../logSystem
python3 logSystem.py
for port in {5000..5400}
do
	pid=$(netstat -nlp | grep :$port | awk '{print $7}' | awk -F"/" '{ print $1 }');
	if [  -n  "$pid"  ];  then
		kill  -9  $pid;
	fi
done
