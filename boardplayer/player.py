import sys
import ast
import socket


class Client(object):
    def __init__(self, player, addr=None, port=None):
        self.player = player
        self.running = False
        self.receiver = {'player': self.handle_player,
                         'decline': self.handle_decline,
                         'error': self.handle_error,
                         'illegal': self.handle_illegal,
                         'update': self.handle_update,
                         'action': self.handle_action,
                         'winners': self.handle_winners,}

        self.addr = addr if addr is not None else '127.0.0.1'
        self.port = port if port is not None else 4242

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
        self.player.player = msg

    def handle_decline(self, msg):
        print msg
        self.running = False

    def handle_error(self, msg):
        print msg # FIXME: do something useful

    def handle_illegal(self, msg):
        print msg # FIXME: do something useful

    def handle_update(self, msg):
        action, state = msg
        self.player.update(state)
        print self.player.display(state, action)

    def handle_action(self, msg):
        action = self.player.get_action()
        self.socket.sendall("play {0!r}\r\n".format(action))

    def handle_winners(self, msg):
        print self.player.winner_message(msg)
        self.running = False


class HumanPlayer(object):
    def __init__(self, board):
        self.board = board
        self.player = None
        self.states = []

    def update(self, state):
        self.states.append(state)

    def display(self, state, action):
        return self.board.display(state, action)

    def winner_message(self, msg):
        return self.board.winner_message(msg)

    def get_action(self):
        while True:
            action = raw_input("Please enter your action: ")
            action = self.board.parse(action)
            if action is None:
                continue
            if self.board.is_legal(self.states, action):
                break
        return action
