import types
from coordinate import Coordinate, BadCoordinateCreation


def get_path(board, cost_table, from_position, to_position):
    evaluated = []
    queue = [from_position]
    path = {}
    score = {}
    score[from_position] = 0
    estimated_score = {}
    estimated_score[from_position] = score[from_position] + _path_length(
        from_position, to_position)

    while queue:
        current_index = queue.index(min(
            [x for x in estimated_score if x in queue],
            key=estimated_score.get))
        current = queue[current_index]
        if(current == to_position):
            return _traceback(path, to_position)

        del queue[current_index]
        evaluated.append(current)

        for neighbor in board.get_neighbors(current):
            if(neighbor in evaluated):
                continue

            cost = 0

            tile = board.get_tile_at_coordinate(neighbor)
            if tile.tile_type in cost_table:
                cost = cost_table[tile.tile_type]
            else:
                continue

            temp_score = score[current] + cost

            if (neighbor not in queue or
                    (neighbor in score and
                     temp_score < score[neighbor])):
                path[neighbor] = current
                score[neighbor] = temp_score
                estimated_score[neighbor] = (score[neighbor] +
                                             _path_length(neighbor,
                                                          to_position))
                if neighbor not in queue:
                    queue.append(neighbor)

    raise NoPathFound("Cannot find path between {} and {}".format(
        from_position, to_position))


def _is_path(board, cost_table, from_position, to_position):
    is_path = True
    try:
        get_path(board, cost_table, from_position, to_position)
    except NoPathFound:
        is_path = False

    return is_path


def path_cost(board, path, cost_table):
    cost = 0
    for coordinate in path:
        tile = board.get_tile_at_coordinate(coordinate)
        cost += cost_table[tile.tile_type]

    return cost


def tiles_in_range(board, cost_table, from_position, max_cost):
    can_move_to = []

    # add 1 to max cost so we're working on a closed interval
    for x in range(-max_cost, max_cost + 1):
        for y in range(-max_cost, max_cost + 1):
            if y == 0 and x == 0 or abs(y) + abs(x) > max_cost:
                continue
            try:
                to_position = Coordinate(from_position.x + x,
                                         from_position.y + y)
            except BadCoordinateCreation:
                continue

            if(board.is_on_board(to_position)):
                try:
                    path = get_path(board, cost_table, from_position,
                                    to_position)

                    path.remove(from_position)
                    if(path_cost(board, path, cost_table) <= max_cost):
                        can_move_to.append(to_position)
                except NoPathFound:
                    continue

    return can_move_to


def _traceback(path, coordinate):
    if coordinate in path:
        traceback = _traceback(path, path[coordinate])
        traceback.append(coordinate)
        return traceback
    else:
        return [coordinate]


def _path_length(start, goal):
    horizontal_distance = abs(start.x - goal.x)
    virtical_distance = abs(start.y - goal.y)
    return horizontal_distance + virtical_distance


class NoPathFound(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
