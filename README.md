linux-gravatar
==============
---

[![Build Status](https://travis-ci.org/jrosco/linux-gravatar.svg?branch=master)](https://travis-ci.org/jrosco/linux-gravatar)
[![GPL License](http://img.shields.io/badge/license-GPL-blue.svg?style=flat-square)](http://opensource.org/licenses/GPL-2.0)
![Version Status](https://img.shields.io/badge/version-v1.0%20Beta-green.svg)

Intro
-----
Set your Linux profile picture using gravatar.

**N.B:** *Only tested on Mint 17 and Ubuntu 14.04*

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
/usr/bin/linux-gravatar
</code>
 
OR search in your **start menu** (Should be under category **"Other"**)

**N.B:** *Running from commandline will display debugging messages at the moment*

**Setup your settings:**

![(img_logo)](https://raw.githubusercontent.com/jrosco/linux-gravatar/master/gui/gravatar.png)

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
username = "Your Gravatar username (not required). Only used to open your profile from drop-down menu"<br>
email = "The email address used to get your avatar"<br>
check = "The amount of time in seconds to scrape the gravatar url for your avatar"<br>
startup = "Not currently used"
</pre>

