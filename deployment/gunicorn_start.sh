#!/bin/bash

NAME="django_app"                              #Name of the application (*)
DJANGODIR=/home/ubuntu/git_dir/US_Name_Stats/django_app             # Django project directory (*)
#SOCKFILE=/run/gunicorn.sock        # we will communicate using this unix socket (*)
SOCKFILE=0.0.0.0:8000
USER=ubuntu                                        # the user to run as (*)
GROUP=webdata                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=django_app.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=django_app.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR

source ~/anaconda3/etc/profile.d/conda.sh
conda activate /home/ubuntu/git_dir/US_Name_Stats/US_Name/
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

#Create the run directory if it doesn't exist
#RUNDIR=$(dirname $SOCKFILE)
#test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/ubuntu/git_dir/US_Name_Stats/US_Name/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=$SOCKFILE
