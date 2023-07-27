# PyRenamer
Application en ligne de commande pour renommer des fichiers ou dossiers

[![Python](https://img.shields.io/badge/python-3.11.4-blue.svg)](https://www.python.org/downloads/release/python-3114/) 

## Sommaire
 - [Objectif](#objectif)
 - [How To Use](#how-to-use)
 - [License](#license)

## Objectif
Ce programme a été créé dans le cadre d'une initiation au langage Python.
Il sert au renommage de fichiers ou dossiers via une ligne de commande

## How To Use
Après avoir installé l'application.
Ouvrez un terminal, vous pouvez vous placer dans le répertoire où vous souhaitez effectuer la transformation ou alors le spécifier dans votre commande.

Vous trouvez ci-dessous le résultat de la commande help

```
usage: app.py [-h] [-e {FILE,FOLDER}] [-f FILTER] [-n NEW_NAME] [-s {NAME,DATE,TYPE} | -r {NAME,DATE,TYPE}] [-p] [path]

positional arguments:
  path                  Path of the directory from which to retrieve the items to be renamed

options:
  -h, --help            show this help message and exit
  -e {FILE,FOLDER}, --element {FILE,FOLDER}
                        Select the type of item to rename (FILE by default)
  -f FILTER, --filter FILTER
                        Entry directory item selection filter (all by default)
  -n NEW_NAME, --new-name NEW_NAME
                        New element name format (%N% by default)
                        Available options :
                                %N% represents a 4-character numeric increment
                                %NA% represents an increment whose format is automatically defined according to the number of elements to be renamed
                                %D% represents a date in yymmdd format
  -i INCREMENT_START, --increment-start INCREMENT_START
                        Defines the integer on which to start incrementing the name if there is one
  -s {NAME,DATE,TYPE}, --sort {NAME,DATE,TYPE}
                        Sorting type
  -r {NAME,DATE,TYPE}, --reverse {NAME,DATE,TYPE}
                        Reverse sorting type
  -p, --preview         Show preview of renaming
```