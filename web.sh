if [ "$dev" == "True" ]; then
        python postpushr.py
else
        gunicorn postpushr:app
fi
