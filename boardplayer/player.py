from __future__ import absolute_import
from __future__ import print_function
import json
import socket
import sys
from six.moves import input


class Client(object):
    def __init__(self, player, addr=None, port=None):
        self.player = player
        self.running = False
        self.receiver = {'player': self.handle_player,
                         'decline': self.handle_decline,
                         'error': self.handle_error,
                         'illegal': self.handle_illegal,
                         'update': self.handle_update}

        self.addr = addr if addr is not None else '127.0.0.1'
        self.port = port if port is not None else 4242

    def run(self):
        self.socket = socket.create_connection((self.addr, self.port))
        self.running = True
        while self.running:
            message = ''
            while not message.endswith('\r\n'):
                message += self.socket.recv(4096).decode('utf-8')
            messages = message.rstrip().split('\r\n')
            for message in messages:
                data = json.loads(message)
                if data['type'] not in self.receiver:
                    raise ValueError(
                        "Unexpected message from server: {0!r}".format(message))

                self.receiver[data['type']](data)

    def handle_player(self, data):
        player = data['message']
        print("You are player #{0}.".format(player))
        self.player.player = player

    def handle_decline(self, data):
        print(data['message'])
        self.running = False

    def handle_error(self, data):
        print(data['message']) # FIXME: do something useful

    def handle_illegal(self, data):
        print(data['message']) # FIXME: do something useful

    def handle_update(self, data):
        state = data['state']
        action = data.get('last_action', {}).get('action') or {}
        self.player.update(state)

        print(self.player.display(state, action))
        if data.get('winners') is not None:
            print(self.player.winner_message(data['winners']))
            self.running = False
        elif data['state']['player'] == self.player.player:
            self.send(self.player.get_action())

    def send(self, data):
        self.socket.sendall("{0}\r\n".format(json.dumps(data)).encode('utf-8'))


class HumanPlayer(object):
    def __init__(self, board):
        self.board = board
        self.player = None
        self.history = []

    def update(self, state):
        self.history.append(self.board.to_compact_state(state))

    def display(self, state, action):
        return self.board.display(state, action)

    def winner_message(self, winners):
        return self.board.winner_message(winners)

    def get_action(self):
        while True:
            notation = input("Please enter your action: ")
            action = self.board.from_notation(notation)
            if action is None:
                continue
            if self.board.is_legal(self.history[-1], action):
                break
        return {
            'type': 'action',
            'message': self.board.to_json_action(action),
        }
