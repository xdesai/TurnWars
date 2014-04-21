from board import Board, InvalidBoardDimensions
from coordinate import Coordinate
from nose.tools import assert_raises


class MockTile:
    tile_type = "none"

    def __init__(self, new_tile_type):
        self.tile_type = new_tile_type

    def flat(self):
        return "serial {}".format(self.tile_type)


def empty_board_test():
    tiles = []
    assert_raises(InvalidBoardDimensions, Board, tiles)
    tiles = [[], [], []]
    assert_raises(InvalidBoardDimensions, Board, tiles)


def non_square_board_test():
    tiles = []
    for row in range(0, 10):
        tiles.append([])
        for col in range(0, row):
            tiles[row].append(MockTile("{} {}".format(row, col)))

    assert_raises(InvalidBoardDimensions, Board, tiles)


def normal_board_test():
    tiles = []
    for row in range(0, 100):
        tiles.append([])
        for col in range(0, 10):
            tiles[row].append(MockTile("{} {}".format(row, col)))

    board = Board(tiles)
    coordinates = board.get_dimensions()
    assert coordinates.x == 10
    assert coordinates.y == 100


def get_tile_test():
    tiles = []
    for row in range(0, 30):
        tiles.append([])
        for col in range(0, 5):
            tiles[row].append(MockTile("{} {}".format(col, row)))

    board = Board(tiles)
    tile = board.get_tile_at_coordinate(1, 4)
    assert tile.tile_type == "1 4"
    tile = board.get_tile_at_coordinate(3, 10)
    assert tile.tile_type == "3 10"
    tile = board.get_tile_at_coordinate(0, 0)
    assert tile.tile_type == "0 0"
    tile = board.get_tile_at_coordinate(4, 29)
    assert tile.tile_type == "4 29"
    assert_raises(IndexError, board.get_tile_at_coordinate, 100, 100)


def json_test():
    print "serializing"
    tiles = []
    for row in range(0, 2):
        tiles.append([])
        for col in range(0, 2):
            tiles[row].append(MockTile("{} {}".format(col, row)))

    board = Board(tiles)
    json_string = (
        '[["serial 0 0", "serial 1 0"], '
        '["serial 0 1", "serial 1 1"]]'
    )
    serial_board = board.as_json()
    assert serial_board == json_string