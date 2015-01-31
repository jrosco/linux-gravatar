linux-gravatar
==============
---

[![Build Status](https://travis-ci.org/jrosco/linux-gravatar.svg?branch=master)](https://travis-ci.org/jrosco/linux-gravatar)

Intro
-----
Set your Linux profile picture using gravatar. 

*Version Alpha 0.1.1*

**N.B: Only tested on Mint 17 and Ubuntu 14.04**

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
python -m linux-gravatar
</code>

**Setup your settings:**

* Click on the linux-gravatar trayicon ![(img_logo)](|https://github.com/jrosco/linux-gravatar/tree/master/gui])

* Enter your email address used to grab the avatar and set the check time (number of minutes between scans)

* Select Apply


**Setting values explained:**

The settings file can be found in your home directory 
<code>
~/.gravatar_settings.cfg
</code>

<pre>
email = "The email address used to get your avatar"<br>
check = "The amount of time in seconds to scrape the gravatar url for your avatar"<br>
startup = "Not currently used"
</pre>

**N.B: You need to run the application first before apply the settings, as the application creates the settings file after it is ran.**