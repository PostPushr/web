if [ "$dev" == "True" ]; then
        python snapoverflow.py
else
        gunicorn snapoverflow:app
fi
