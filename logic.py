from math import floor
from sys import stderr

from settings import Settings
from state import State


def is_in_bounds(settings: Settings, coordinate):
    if 0 >= coordinate['x'] or coordinate['x'] >= settings.get_field_width():
        return False
    
    if 0 >= coordinate['y'] or coordinate['y'] >= settings.get_field_height():
        return False
    
    return True


def get_available_moves(settings: Settings, state: State):
    from bot import Move

    my_position = get_coordinate_for(settings, state.get_field(), settings.get_your_botid())
    neighboring_fields = get_neighboring_fields(settings, state.get_field(), my_position)
    available_moves = [Move.none]

    for move, field_value in neighboring_fields:
        if field_value is not 'x':
            available_moves.append(move)

    return available_moves


def get_field_size(settings: Settings):
    return settings.get_field_width() * settings.get_field_height()


def get_coordinate_for(settings: Settings, field, bot_id):
    index = field.index(bot_id)
    return index_to_coordinate(settings, index)


def get_neighboring_fields(settings: Settings, field, coordinate):
    neighboring_fields = {}
    
    directions = {
        'up': {'x': coordinate['x'], 'y': coordinate['y'] - 1},
        'down': {'x': coordinate['x'], 'y': coordinate['y'] + 1},
        'left': {'x': coordinate['x'] - 1, 'y': coordinate['y']},
        'right': {'x': coordinate['x'] + 1, 'y': coordinate['y']},
    }
    
    for direction_name, direction_coordinate in directions:
        if is_in_bounds(settings, direction_coordinate):
            direction_index = coordinate_to_index(settings, direction_coordinate)
            neighboring_fields[direction_name] = field[direction_index]

    return neighboring_fields


def index_to_coordinate(settings: Settings, index):
    if index >= get_field_size(settings):
        stderr.write('index > fieldsize\n')
        stderr.flush()

    field_width = settings.get_field_width()
    x = index % field_width
    y = floor(index / field_width)

    return {'x': x, 'y': y}


def coordinate_to_index(settings: Settings, coordinate):
    if not is_in_bounds(settings, coordinate):
        return -1

    field_width = settings.get_field_width()

    return coordinate['y'] * field_width + coordinate['x']
