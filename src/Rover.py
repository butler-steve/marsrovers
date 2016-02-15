from Plateau import *

class Rover:
    def __init__(self, initial_position, initial_bearing):
        Plateau.Position.raiseIfNotAValidDirection(initial_bearing)
        self._bearing = initial_bearing
        self._position = initial_position

    def getPosition(self):
        return self._position.X(), self._position.Y()

    def getBearing(self):
        return self._bearing

    def rotate(self, is_counterCW = False):
        if type(is_counterCW) is not type(True):
            raise ValueError('Boolean argument is expected')

        from_bearing_ndx = Plateau.Position.valid_directions.index(self._bearing)
        if is_counterCW:
            to_bearing_ndx = (from_bearing_ndx - 1)
        else:
            to_bearing_ndx = (from_bearing_ndx + 1)
        to_bearing_ndx %= len(Plateau.Position.valid_directions)
        self._bearing = Plateau.Position.valid_directions[to_bearing_ndx]

    def advance(self):
        self._position = self._position.fromHere(self._bearing)

