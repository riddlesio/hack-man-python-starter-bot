#
# Copyright 2016 riddles.io (developers@riddles.io)
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#     For the full copyright and license information, please view the LICENSE
#     file that was distributed with this source code.

import pprint
import random
from enum import Enum
from sys import stderr, stdin, stdout

from logic import get_available_moves
from settings import Settings
from state import State


class Bot(object):
    """
    Main bot class
    """

    def __init__(self):
        """
        Initializes a settings dict and sets previous move
        """
        self.settings = Settings()
        self.state = State()
        self.previous_move = None

    def run(self):
        """
        Main loop
        
        Keeps running while being fed data from stdin.
        Writes output to stdout, remember to flush!
        """
        while not stdin.closed:
            try:
                rawline = stdin.readline()

                # End of file check
                if len(rawline) == 0:
                    break

                line = rawline.strip()

                # Empty lines can be ignored
                if len(line) == 0:
                    continue

                parts = line.split()

                command = parts[0]

                # All different commands besides the opponents' moves
                if command == 'settings':
                    self.update_settings(parts[1:])

                elif command == 'update':
                    if parts[1] == 'game':
                        self.update_game(parts[2:])
                    else:
                        self.update_player_data(parts[1:])

                elif command == 'action':
                    self.update_action(parts[1:])

                else:
                    stderr.write('Unknown command: {}\n'.format(command))
                    stderr.flush()
            except EOFError:
                return

    def print_var(self, *args):
        for var in enumerate(args):
            stderr.write('%s\n' % pprint.pformat(var))
            stderr.flush()

    def update_settings(self, options):
        """
        Method to update game settings at the start of a new game.
        """
        key, value = options
        self.settings = self.settings.update(key, value)

    def update_game(self, options):
        if options[0] == 'round':
            self.state = self.state.update('round', int(options[1]))
        elif options[0] == 'field':
            self.state = self.state.update('field', options[1].split(','))

    def update_player_data(self, options):
        player_id, attribute, value = options

        players = self.state.get_players()
        player = players.setdefault(player_id, {
            'snippets': None,
            'has_weapon': None,
            'is_paralyzed': None,
        })

        if attribute == 'snippets':
            player['snippets'] = value
        elif attribute == 'has_weapon':
            player['has_weapon'] = value == 'true'
        elif attribute == 'is_paralyzed':
            player['is_paralyzed'] = value == 'true'

        # players[player_id] = player
        self.state = self.state.update('players', players)

    def update_action(self, options):
        if options[0] == 'move':
            self.settings = self.settings.update('timebank', options[1])
            self.do_unreversed_move()

    def do_unreversed_move(self):
        valid_moves = get_available_moves(self.settings, self.state)
        if self.previous_move:
            valid_moves.remove(self.previous_move)
        stdout.write('{}\n'.format(random.choice(valid_moves)))
        stdout.flush()


class Move(Enum):
    up = 'up'
    down = 'down'
    left = 'left'
    right = 'right'
    none = 'pass'  # pass is a python reserved keyword

    @classmethod
    def get_moves(cls):
        return [cls.up, cls.down, cls.left, cls.right, cls.none]


if __name__ == '__main__':
    """
    Not used as module, so run
    """
    Bot().run()
