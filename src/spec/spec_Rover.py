
from Plateau import *
from Rover import *
from mockito import *
from sure import *

def setupRoverArguments(self):
    self.plateau_dims = 8, 4
    self.plateau = Plateau(*self.plateau_dims)
    self.initial_pos_coords = 2, 1
    self.initial_position = self.plateau.getPosition(*self.initial_pos_coords)
    self.initial_bearing = 'E'

with context(Rover):
    with it('should take an initial position and bearing as arguments'):
        setupRoverArguments(self)
        self.sut = Rover(self.initial_position, self.initial_bearing)
    with context('if an invalid bearing is supplied,'):
        with it('should raise an InvalidDirectionError'):
            setupRoverArguments(self)
            try:
                self.sut = Rover(self.initial_position, 'A')
                assert(False)
            except Plateau.InvalidDirectionError:
                pass

    with context('methods:'):
        with before.each:
            setupRoverArguments(self)
            self.sut = Rover(self.initial_position, self.initial_bearing)

        with context('.getPosition()'):
            with it('should exist'):
                self.sut.getPosition.should.be.callable
            with it('should return the supplied position coordinates'):
                self.sut.getPosition().should.equal(self.initial_pos_coords)

        with context('.getBearing()'):
            with it('should exist'):
                self.sut.getBearing.should.be.callable
            with it('should return the supplied bearing'):
                self.sut.getBearing().should.equal(self.initial_bearing)

        with context('.rotate()'):
            with it('should exist'):
                self.sut.rotate.should.be.callable
            with it('should take a bool argument'):
                self.sut.rotate(False)
            with it('should raise an error if the wrong argument type is supplied'):
                try:
                    self.sut.rotate('L')
                    assert(False)
                except ValueError:
                    pass
            with context('if clockwise rotation is specified,'):
                with it('should set bearing to the next valid direction in list'):
                    self.sut.rotate()
                    this_dir_ndx = Plateau.Position.valid_directions.index(self.initial_bearing)
                    Plateau.Position.valid_directions.index(self.sut.getBearing()).should.equal(this_dir_ndx+1)
                with it('should wrap around to the beginning of the valid direction list'):
                    this_dir_ndx = Plateau.Position.valid_directions.index(self.initial_bearing)
                    number_of_valid_directions = len(Plateau.Position.valid_directions)
                    for _ in range(0, number_of_valid_directions):
                        self.sut.rotate()
                        this_dir_ndx += 1
                        if this_dir_ndx >= number_of_valid_directions:
                            Plateau.Position.valid_directions.index(self.sut.getBearing()).should.equal(0)
                            break
            with context('if counter clockwise rotation is specified,'):
                with it('should set bearing to the previous valid direction in list'):
                    self.sut.rotate(True)
                    this_dir_ndx = Plateau.Position.valid_directions.index(self.initial_bearing)
                    Plateau.Position.valid_directions.index(self.sut.getBearing()).should.equal(this_dir_ndx-1)
                with it('should wrap around to the end of the valid direction list'):
                    this_dir_ndx = Plateau.Position.valid_directions.index(self.initial_bearing)
                    number_of_valid_directions = len(Plateau.Position.valid_directions)
                    for _ in range(0, number_of_valid_directions):
                        self.sut.rotate(True)
                        this_dir_ndx -= 1
                        if this_dir_ndx < 0:
                            Plateau.Position.valid_directions.index(self.sut.getBearing()).should.equal(number_of_valid_directions-1)
                            break

        with context('.advance()'):
            with before.each:
                self.mock_position = mock()
                self.sut = Rover(self.mock_position, self.initial_bearing)
            with it('should exist'):
                self.sut.advance.should.be.callable
            with it('should invoke fromHere() method on current position'):
                self.sut.advance()
                verify(self.mock_position).fromHere(any())
            with it('should pass current bearing to fromHere() method'):
                self.sut.advance()
                verify(self.mock_position).fromHere(self.sut.getBearing())
            with it('should replace the current position with the result of the fromHere() method'):
                stub_x, stub_y = 'xcoordinate', 'ycoordinate'
                class MockPosition:
                    def X(self):
                        return stub_x
                    def Y(self):
                        return stub_y
                new_position_stub = MockPosition()
                when(self.mock_position).fromHere(any()).thenReturn(new_position_stub)
                self.sut.advance()
                self.sut.getPosition().should.equal((stub_x, stub_y))


