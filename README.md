# plex-recently-added-summary
Last Edited on 07/07/2017

A Python Script that, when run, checks your Plex server for recently added and summarizes the entries within the time frame you specify. Then sends the summary to different services you specify.

### Installation Instructions:

Download the script or clone the repo to a directory of your choice.
After that you will have to install several things to get this script to work.

1. Python 2.7
    - Go to https://www.python.org/downloads/ and download python for your platform.
    - Install Python and remember the directory, should be something like C:/Python27 on Windows machines
   >- Optional: Add the path to Python to your Windows PATH.

2. PIP
	- Newer version of Python 2.7 and 3.4 should come with pip installed.  PATH_TO_PYTHON/Scripts is where it should be.
	- If you are using a version of Python without pip manual instructions here [PIP Manual Instructions](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)
   >- Optional: Also add the path to pip to your Windows PATH.

3. PlexAPI
	- With Python and pip installed you should just have to run **pip install plexapi** or **{PATH_TO_PIP}/pip install plexapi**

### Notification/Post Service Installs:
> *You don't need to install all of these if you aren't going to use them, **_but you must edit the script not to use them if you don't install them._***

1. FacePy
    - There are other ways to post to FB with Python, but for now I've gone with FacePy.
    - With Python and pip installed you just need to run **pip install facepy** or **{PATH_TO_PIP}/pip install facepy**

2. PushBullet
    - With Python and pip installed you just need to run **pip install pushbullet** or **{PATH_TO_PIP}/pip install pushbullet**

After that you should have everything needed to get the script to run
