# Connect 4
> A personal implementation

This is a personal implementation of the connect 4 game.
This is made in Python3 and played in the terminal.

## Installing / Getting started

To run this you'll need [Python3](www.python.org) installed and the dependencies in `requirements.txt`.
You can install those globally by typing `pip install -r requirements.txt`, but I would suggest creating a virtual environment for this project using [venv](https://docs.python.org/3/library/venv.html).

### Venv

To create a virtual environment en install the dependencies type:

```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

This will create a venv in the current directory, activate it and install the dependencies.

### Conda

You can also manage the dependencies using [conda](https://docs.conda.io/projects/conda/en/latest/index.html).

```
conda env create -f environment.yml
```

This will create and activate the environment.

## Running the game

To run the game type

```
python -m connect4
```
or run
```
python -m connect4 -h
```
to see extra options.

To play game simply type the number of the column you want the put the disc in and press enter.

## Features

Different playstyles of this game:
 - [x] Play locally against another player
 - [x] Play locally against a bot
 - [ ] Play online against another player

## Licensing

The code in this project is licensed under The Unlicense.
