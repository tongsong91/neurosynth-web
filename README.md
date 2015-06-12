
# neurosynth-web

This is the stuff that runs [neurosynth.org](http://neurosynth.org).

## Installation

There are two ways to install a development version of the neurosynth web server. The recommended approach is to use Docker and Fig. For masochists, there's also an alternative manual installation procedure.

### Installing via Docker and Fig

The easiest way to get a dev environment up and running is to follow the following steps:

1. Install [Docker](https://www.docker.com/).
2. Install fig with pip:

    pip install fig
3. Clone this repository somewhere convenient:

    git clone https://github.com/neurosynth/neurosynth-web.git

4. Optionally (but strongly recommended), edit the docker-compose.yml file in the repository root to point to a folder on your host system where you want all data files generated by the Neurosynth server code to live. For example, if you want files written to /opt/data on your host machine, replace /CHANGEME with /opt/data. If you don't set a valid host directory to mount within the disk image, a fresh /data directory will be created for you. But since this directory exists only inside the image, you won't be able to easily view generated files from the host. So it's strongly recommended that you point to a valid local folder.

5. Use fig to build the Docker image. This should take anywhere between ten minutes and a couple of hours, depending on the speed of your connection and machine, plus local availability of intermediate images. From the repository root, politely ask fig to set everything up:

    fig up

6. Run the Docker container fig just created for you, making sure to enable service ports:

    fig run --service-ports web

7. You should now be dropped into a bash shell, with the working directory set to /code (where the neurosynth-web server code lives). At this point, if this is your first time running the image, you'll want to run the neurosynth-web Flask app's setup. By default, no configuration is required--the Flask app will use a SQLite driver. If you want to customize settings, you can find the config file at /code/nsweb/initializers/settings.py. To run the setup script:

    python setup_database.py

8. Now you can run the Flask app!

    python runserver.py

Flask will run the development server on port 5001. Docker should automatically open this port on your local machine, but depending on your platform and Docker setup, you may or may not be able to access the dev site at http://localhost:5001. If you're on OS X and running under boot2docker, you'll most likely need to point your browser to the VirtualBox IP rather than localhost (which you should be able to get with 'boot2docker ip').


### Manual installation

Manual installation is a rather cumbersome process, and you should probably avoid it unless you enjoy self-flagellation. There are a large number of dependencies, some of which are platform-specific. To get a working development app, something like the following steps should work:

1. Create a new virtual-env to house all the Python dependencies.
2. Install the [Neurosynth](http://github.com/neurosynth/neurosynth) package and its dependencies, as well as core computational/plotting packages:

	pip install numpy scipy matplotlib pandas seaborn scikit-learn ply neurosynth

3. Install node and coffeescript
4. Install Flask and various other packages (see requirements.txt):

	pip install SQLalchemy Flask simplejson jinja2 cssmin webassets pyscss Flask-Assets Flask-Babel Flask-Cake Flask-Mail Flask-Migrate Flask-Script Flask-SQLAlchemy Flask-User Flask-WTF

5. Install MySQL or MariaDB and a Python MySQL adapter (PyMySQL or MySQL-Python)
6. Optional: Install and configure uwsgi. Copy or rename deploy/deploy-dev-template.ini to deploy/deploy-dev.ini. Modify settings as needed. Alternatively, you can just run python run_server.py to rely on the built-in server for local development.
7. Optional: install and configure nginx or Apache to point to the development app. This isn't covered here. Alternatively, you can just run python run_server.py to rely on the built-in server for local development.
8. Install redis and celery
9. Copy or rename nsweb/initializers/settings-template.py to nsweb/initializers/settings.py. Change the root data path at the top to a writeable directory, and edit the MySQL settings as needed. Make sure the user exists in MySQL and has write privileges to the correct database(s).
10. Download the latest Neurosynth data files from  [https://github.com/neurosynth/neurosynth-data/blob/master/current_data.tar.gz](https://github.com/neurosynth/neurosynth-data/blob/master/current_data.tar.gz). Extract the .txt files and put the in the assets/ folders below the data root specified in settings.py.
11. Optional: obtain ~300GB of functional connectivity images from Thomas Yeo and put them in an 'fcmri' folder under settings.IMAGE_DIR.
12. Edit setup_database.py if desired. For rapid development/prototyping, set PROTOTYPE=True in settings.py. This will only populate the DB with a small fraction of the data rather than using all of it.
13. Run python setup_database.py. Wait somewhere between a few minutes and a day or two. Check MySQL database to make sure that tables have stuff in them.
14. Launch the web server and navigate to the site. Make sure everything works. It probably won't. Fix whatever's broken. Then try again. Rinse and repeat.

