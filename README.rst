boardgame-socketplayer
======================

A client for pluggable board game implementations.


Requirements
------------

You need to have the following system packages installed:

* Python >= 2.6


Getting Started
---------------

To set up your local environment you should create a virtualenv and
install everything into it. ::

    $ mkvirtualenv boardgames

Pip install this repo, either from a local copy, ::

    $ pip install -e boardgame-socketplayer

or from github, ::

    $ pip install git+https://github.com/jbradberry/boardgame-socketplayer

To connect to a server as a human player playing (for example) `Ultimate Tic Tac Toe
<https://github.com/jbradberry/ultimate_tictactoe>`_ ::

    $ board-play.py t3 human
    $ board-play.py t3 human 192.168.1.1 8000   # with ip addr and port
