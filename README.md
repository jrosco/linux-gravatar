# linux-gravatar

---

[![Build Status](https://travis-ci.org/jrosco/linux-gravatar.svg?branch=master)](https://travis-ci.org/jrosco/linux-gravatar)
[![GPL License](http://img.shields.io/badge/license-GPL-blue.svg?style=flat-square)](http://opensource.org/licenses/GPL-2.0)
![Version Status](https://img.shields.io/badge/version-v1.1%20Beta-green.svg)

- [linux-gravatar](#linux-gravatar)
  - [Dependencies](#dependencies)
  - [Build/Install/Setup/Run](#buildinstallsetuprun)
  - [Settings](#settings)
  - [Issues](#issues)
Intro

---
Set your Linux profile picture using gravatar.

**Supports Python 2.7+ adm Python 3**

**N.B:** *Only Ubuntu 20.04, happy for people to try on other Distro and report back.*

## Dependencies

---

**Ubuntu: (Python 2 only)**

```bash
apt-get install python-glade2 python-appindicator
```

## Build/Install/Setup/Run

---

**Clone git repo:**

```bash
git clone https://github.com/jrosco/linux-gravatar.git
```

**Change directory and run setup:**

```bash
cd linux-gravatar; sudo python setup.py install
```

**Run application:**

```bash
/usr/local/bin/linux-gravatar
```

OR search in your **start menu** (Should be under category **"Other"**)

**Setup your settings:**

![(img_logo)](https://raw.githubusercontent.com/jrosco/linux-gravatar/master/data/gui/gravatar.png)

* Click on the linux-gravatar in your trayicon (example shown above)

* Enter your Gravatar username (not required). Only used to open your profile from the drop-down menu"

* Enter your email address used to grab the avatar and set the check time (number of minutes between scans)

* Select Apply

## Settings

The settings file can be found in your home directory

```text
~/.gravatar_settings.cfg
```

| Name  | Description | Default
|---|---|---|
| username  | Your Gravatar username (not required). Only used to open your profile from drop-down menu" | Null |
| email | The email address used to download your avatar | Null |
| check | The amount of time in seconds to scrape the gravatar url for your avatar | 60.0 |
| notifications | Toggle between showing or not showing notification messages in the system tray | True |
| startup | Not currently used | False |

## Issues

---

Please report any issues or request [here](https://github.com/jrosco/linux-gravatar/issues)
