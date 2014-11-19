import sys
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


args = sys.argv[1:]
addr, port = None, None

board = board_plugins[args[0]]
player_obj = player_plugins[args[1]]

if len(args) > 2:
    addr = args[2]
if len(args) > 3:
    port = int(args[3])


client = player.Client(player_obj(board()), addr, port)
client.run()
