import sys
import argparse

from pkg_resources import iter_entry_points

from boardplayer import player


board_plugins = dict(
    (ep.name, ep.load())
    for ep in iter_entry_points('jrb_board.games')
)

player_plugins = dict(
    (ep.name, ep.load())
    for ep in iter_entry_points('jrb_board.players')
)

parser = argparse.ArgumentParser(
    description="Play a boardgame using a specified player type.")
parser.add_argument('game', choices=sorted(board_plugins))
parser.add_argument('player', choices=sorted(player_plugins))
parser.add_argument('address', nargs='?')
parser.add_argument('port', nargs='?', type=int)
parser.add_argument('-e', '--extra', action='append')

args = parser.parse_args()

board = board_plugins[args.game]
player_obj = player_plugins[args.player]
player_kwargs = dict(arg.split('=') for arg in args.extra or ())


client = player.Client(player_obj(board(), **player_kwargs),
                       args.address, args.port)
client.run()
