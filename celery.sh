until celery worker -q -A tasks > /dev/null 2>&1; do
    echo "Server 'celery worker -q -A tasks' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done