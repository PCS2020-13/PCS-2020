# Project Computational Science 2020

This repository contains all files necessary for running the simulations used by project group 13 in the Project Computational Science course at the University of Amsterdam.

## Group members
Dorian Bekaert, Florine de Geus, Elisha Nieuwburg

## Installation

We recommend running the simulations through a *virtual environment* ([venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)). If you have not installed this yet on your machine, you can do so by using the commands below (do make shure you have Python 3 installed. I use Python 3.6.9):

For Linux/macOS:
```bash
python3 -m pip install --user virtualenv
```
For Windows:
```bash
py -m pip install --user virtualenv
```

### Creating and activating the virtual environment

Creating a new virtual environment can be done by running the following commands:

```bash
virtualenv venv/ -p /usr/bin/python3
source venv/bin/activate
pip install -r requirements.txt
```

The first line creates a new environment. You only have to run this command once.
The second line activates the environment. You need to run this command each time you revisit the project.
The third line installs all project dependencies in the virtual environment. It is good practice to run this command after each `pull`.

To exit the environment, simply type
```
deactivate
```
Remember to reactivate the environment when you return to the project.

It is possible to run the project without a virtual environment, though not recommended, since it might interfere with the python dependencies currently installed on your machine.
