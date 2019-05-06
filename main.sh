# based on this so q: https://stackoverflow.com/questions/39373837/kill-processes-started-in-parallel
pids=()
SIGINT=2 

function cleanup() {
    echo "performing cleanup"
    
    for pid in ${pids[@]}
    do
        # echo "$pid"
        pkill -STOP -P $pid
    done 

    echo "done cleaning up"

    exit $SIGINT
}

trap "cleanup" SIGINT

python3 -m example.client > client.log & pids+=($!) ; echo $!  &
python3 -m auth_server.auth_server > auth_server.log & pids+=($!) ; echo $! &
python3 -m resource_server.resource_server > resource_server.log & pids+=($!) ; echo $! &
wait

# use lsof -i [PORT_NUM] to check processes listening to port