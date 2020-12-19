linux-gravatar
==============
---

[![Build Status](https://travis-ci.org/jrosco/linux-gravatar.svg?branch=master)](https://travis-ci.org/jrosco/linux-gravatar)
[![GPL License](http://img.shields.io/badge/license-GPL-blue.svg?style=flat-square)](http://opensource.org/licenses/GPL-2.0)
![Version Status](https://img.shields.io/badge/version-v1.1%20Beta-green.svg)

Intro
-----
Set your Linux profile picture using gravatar.

<code>
**Supports Python 2.7+ (including Python 3)**
</code>

**N.B:** *Only tested on Mint 17 and Ubuntu 14.04, happy for people to try on other Distro and report back.*

Dependencies
-----

**Ubuntu:**

<code>
apt-get install python-glade2 python-appindicator
</code>


Build/Install/Setup/Run
-----
**Clone git repo:**

<code>
git clone https://github.com/jrosco/linux-gravatar.git
</code>

**Change directory and run setup:**

<code>
cd linux-gravatar; sudo python setup.py install
</code>

**Run application:**

<code>
/usr/local/bin/linux-gravatar
</code>
 
OR search in your **start menu** (Should be under category **"Other"**)

**Setup your settings:**

![(img_logo)](https://raw.githubusercontent.com/jrosco/linux-gravatar/master/data/gui/gravatar.png)

* Click on the linux-gravatar in your trayicon (example shown above)

* Enter your Gravatar username (not required). Only used to open your profile from the drop-down menu"

* Enter your email address used to grab the avatar and set the check time (number of minutes between scans)

* Select Apply

**Example:**

![screenshot](http://i62.tinypic.com/11hb4sh.png)


**Setting values explained:**

The settings file can be found in your home directory 
<code>
~/.gravatar_settings.cfg
</code>

<pre>
username = "Your Gravatar username (not required). Only used to open your profile from drop-down menu" (Default:None)<br>
email = "The email address used to download your avatar" (Default:None)<br>
check = "The amount of time in seconds to scrape the gravatar url for your avatar" (Default:60.0)<br>
notifications = "Toggle between showing or not showing notification messages in the system tray (Default:True)"<br>
startup = "Not currently used (Default:0)"
</pre>

Issues
-----

Please report any issues or request [here](https://github.com/jrosco/linux-gravatar/issues)
