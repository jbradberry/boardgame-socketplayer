import sys
import ast
import socket


class Player(object):
    def __init__(self, board):
        self.board = board
        self.player = None
        self.states = []
        self.running = False
        self.receiver = {'player': self.handle_player,
                         'decline': self.handle_decline,
                         'error': self.handle_error,
                         'illegal': self.handle_illegal,
                         'update': self.handle_update,
                         'action': self.handle_action,
                         'winner': self.handle_winner,}

        self.addr = '127.0.0.1'
        self.port = 4242
        pos_args = sys.argv[1:]
        if len(pos_args) > 0:
            self.addr = pos_args[0]
        if len(pos_args) > 1:
            self.port = int(pos_args[1])

    def run(self):
        self.socket = socket.create_connection((self.addr, self.port))
        self.running = True
        while self.running:
            message = self.socket.recv(4096)
            messages = message.rstrip().split('\r\n')
            for message in messages:
                for action in self.receiver:
                    if message.startswith(action):
                        msg_contents = message[len(action)+1:]
                        if msg_contents:
                            msg_contents = ast.literal_eval(msg_contents)
                        self.receiver[action](msg_contents)
                        break
                else:
                    raise ValueError(
                        "Unexpected message from server: {0!r}".format(message))

    def parse_item(self, item):
        result = ast.literal_eval(item)
        return result

    def handle_player(self, msg):
        print "You are player #{0}.".format(msg)
        self.player = msg

    def handle_decline(self, msg):
        print msg
        self.running = False

    def handle_error(self, msg):
        print msg # FIXME: do something useful

    def handle_illegal(self, msg):
        print msg # FIXME: do something useful

    def handle_update(self, msg):
        play, state = msg # FIXME: do something with 'play'
        self.states.append(state)
        print self.board.display(state)

    def handle_action(self, msg):
        move = self.get_play()
        self.socket.sendall("play {0!r}\r\n".format(move))

    def handle_winner(self, msg):
        print self.board.winner_message(msg)
        self.running = False

    def get_play(self):
        pass
