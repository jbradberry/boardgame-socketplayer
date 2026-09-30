#!/usr/bin/env python
import argparse
from importlib.metadata import entry_points
import sys

from boardplayer import player


board_plugins = {ep.name: ep.load() for ep in entry_points(group='jrb_board.games')}
player_plugins = {ep.name: ep.load() for ep in entry_points(group='jrb_board.players')}

parser = argparse.ArgumentParser(
    description="Play a boardgame using a specified player type.")
parser.add_argument('game', choices=sorted(board_plugins))
parser.add_argument('player', choices=sorted(player_plugins))
parser.add_argument('address', nargs='?')
parser.add_argument('port', nargs='?', type=int)
parser.add_argument('-e', '--extra', action='append')


def main():
    args = parser.parse_args()

    board = board_plugins[args.game]
    player_obj = player_plugins[args.player]
    player_kwargs = {k: w for k, w in (arg.split('=') for arg in args.extra or ())}

    client = player.Client(player_obj(board(), **player_kwargs),
                           args.address, args.port)
    client.run()
