boardgame-socketplayer
======================

A client for pluggable board game implementations.

The client included here is designed to work with
`jbradberry/boardgame-socketserver
<https://github.com/jbradberry/boardgame-socketserver>`_ and the Monte
Carlo Tree Search implementation `jbradberry/mcts
<https://github.com/jbradberry/mcts>`_.


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

To connect a client using one of the compatible `Monte Carlo Tree
Search AI <https://github.com/jbradberry/mcts>`_ players ::

    $ board-play.py t3 jrb.mcts.uct    # number of wins metric
    $ board-play.py t3 jrb.mcts.uctv   # point value of the board metric

Configuration variables can be passed in using ``-e <variable
name>=<variable value>``.  The ``-e`` flag may be repeated to pass in
multiple variables.  For example, ::

    $ board-play.py t3 jrb.mcts.uct -e time=120 -e C=3.5

would configure the UCT player to use 2 minutes of thinking time, with
an exploration coefficient of 3.5.


Games
-----

Compatible games that have been implemented include:

* `Reversi <https://github.com/jbradberry/reversi>`_
* `Connect Four <https://github.com/jbradberry/connect-four>`_
* `Ultimate (or 9x9) Tic Tac Toe
  <https://github.com/jbradberry/ultimate_tictactoe>`_
* `Chong <https://github.com/jbradberry/chong>`_
