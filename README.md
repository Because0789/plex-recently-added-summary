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

### Example Output:
The Daily Summary of recently added Movies and TV Shows from {Your_Server}:  
No Movies Added.  
TV Shows:  
-Dark Matter-  
--Dark Matter S03E06 - One Last Card to Play  
-Hellsing Ultimate-  
--Hellsing Ultimate S01E08 - Hellsing VIII  
--Hellsing Ultimate S01E09 - Hellsing IX  
-Heroes-  
--Heroes S04E01 - Orientation  
--Heroes S04E02 - Jump, Push, Fall  
-I Am Cait-  
--8 episodes added in Season 02.  
-Knights of Sidonia-  
--11 episodes added in Season 02.  
-Luther-  
--Luther S01E03 - Episode 3  
-Modern Family-  
--16 episodes added in Season 08.  
-Parks and Recreation-  
--2 episodes added in Season 05.  
--8 episodes added in Season 07.  
-Rizzoli & Isles-  
--Rizzoli & Isles S06E18 - A Shot in the Dark  
-Supergirl-  
--Supergirl S01E18 - Worlds Finest  
-The Legend of Neil-  
--7 episodes added in Season 02.  
--7 episodes added in Season 03.  
-The Librarians (2014)-  
--5 episodes added in Season 02.  
-The Mist-  
--The Mist S01E04 - Pequod  
-Valvrave the Liberator-  
--7 episodes added in Season 01.  
--8 episodes added in Season 02.  
-Weeds-  
--6 episodes added in Season 07.  

### TODOs:  
- Send email based on a whitelist in a file  
- Loop through all library sections(More than just TV Shows and Movies) and make a message chunk for each  
- Figure out how to get a permenant FB auth token  
- Log out to log file(arg for whether or not to clear log file on run or append)  
- Multiple Libraries?
