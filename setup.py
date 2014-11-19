from distutils.core import setup

setup(
    name='BoardPlayer',
    version='0.1dev',
    author='Jeff Bradberry',
    author_email='jeff.bradberry@gmail.com',
    packages=['boardplayer'],
    scripts=['bin/board-play.py'],
    entry_points={
        'jrb_board.games': [],
        'jrb_board.players': 'human = boardplayer.player:HumanPlayer'
    },
    license='LICENSE',
    description="A generic board game player.",
)
