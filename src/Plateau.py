
class Plateau:
    class InvalidCoordinateError(BaseException):
        def __init__(self):
            pass

    class InvalidDirectionError(BaseException):
        def __init__(self):
            pass

    class Position:

        valid_directions = ('N', 'E', 'S', 'W')

        def __init__(self, x, y, plateau):
            self._plateau = plateau
            self._coords = (x, y)

        def X(self):
            return self._coords[0]

        def Y(self):
            return self._coords[1]

        def fromHere(self, direction):
            Plateau.Position.raiseIfNotAValidDirection(direction)
            coord_map = {
                Plateau.Position.valid_directions[0]: [self._coords[0], self._coords[1]+1], # N
                Plateau.Position.valid_directions[1]: [self._coords[0]+1, self._coords[1]], # E
                Plateau.Position.valid_directions[2]: [self._coords[0], self._coords[1]-1], # S
                Plateau.Position.valid_directions[3]: [self._coords[0]-1, self._coords[1]]  # W
            }
            new_pos = coord_map.get(direction, None)
            return self._plateau.getPosition(new_pos[0], new_pos[1])

        def raiseIfNotAValidDirection(direction):
            if direction not in Plateau.Position.valid_directions:
                raise Plateau.InvalidDirectionError

    def __init__(self, x_dim = 0, y_dim = 0):
        self._grid_dimensions = (x_dim, y_dim)

    def getDimensions(self):
        return [self._grid_dimensions[0], self._grid_dimensions[1]]

    def getPosition(self, x, y):
        if x < 0 or y < 0 or x >= self._grid_dimensions[0] or y >= self._grid_dimensions[1]:
            raise Plateau.InvalidCoordinateError 
        return Plateau.Position(x, y, self)


