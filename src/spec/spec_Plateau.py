from Plateau import *
from sure import *

with description('MarsRover tests:'):
    with context(Plateau):
        with before.each:
            self.x_dim, self.y_dim = 3, 5
            self.sut = Plateau(self.x_dim, self.y_dim)
        with it('should exist'):
            self.sut.should.be.a(Plateau)
        with it('should default to a 0x0 grid'):
            try:
                self.sut = Plateau()
                self.sut.getPosition(0,0)
            except Plateau.InvalidCoordinateError:
                pass
            except Exception:
                assert(False)

        with context('.getDimensions()'):
            with it('should return the supplied grid dimensions'):
                self.sut.getDimensions().should.equal([self.x_dim, self.y_dim])

        with context('.getPosition()'):
            with it('should exist'):
                self.sut.getPosition
            with it('should take an x and y coordinate'):
                self.sut.getPosition(0,0)

            with context('if an invalid position is requested,'):
                with it('should raise an InvalidCoordinateError if first coord is < 0'):
                    try:
                        self.sut.getPosition(-1,0)
                        assert(False)
                    except AssertionError as e:
                        raise e
                    except Plateau.InvalidCoordinateError:
                        pass
                with it('should raise an InvalidCoordinateError if second coord is < 0'):
                    try:
                        self.sut.getPosition(0,-1)
                        assert(False)
                    except AssertionError as e:
                        raise e
                    except Plateau.InvalidCoordinateError:
                        pass
                with it('should raise an InvalidCoordinateError if first coord is >= supplied maximum width'):
                    try:
                        self.sut.getPosition(self.x_dim, 0)
                        assert(False)
                    except AssertionError as e:
                        raise e
                    except Plateau.InvalidCoordinateError:
                        pass
                with it('should raise an InvalidCoordinateError if second coord is >= supplied maximum height'):
                    try:
                        self.sut.getPosition(0, self.y_dim)
                        assert(False)
                    except AssertionError as e:
                        raise e
                    except Plateau.InvalidCoordinateError:
                        pass

            with context('if a valid position is requested,'):
                with before.each:
                    self.x_coord, self.y_coord = 1,2
                with it('should return an object with an X() method'):
                    self.sut.getPosition(self.x_coord, self.y_coord).X.should_not.be.none
                with it('should return an object with a Y() method'):
                    self.sut.getPosition(self.x_coord, self.y_coord).Y.should_not.be.none
                with it('should return an object whose X() method returns the first coordinate'):
                    self.sut.getPosition(self.x_coord, self.y_coord).X().should.equal(self.x_coord)
                with it('should return an object whose Y() method returns the second coordinate'):
                    self.sut.getPosition(self.x_coord, self.y_coord).Y().should.equal(self.y_coord)
                with it('should return an object with a fromHere() method'):
                    self.sut.getPosition(self.x_coord, self.y_coord).fromHere.should_not.be.none

            with context('.fromHere()'):
                with before.each:
                    self.x_coord, self.y_coord = 1,2
                    self.plateau = self.sut
                    self.sut = self.sut.getPosition(self.x_coord, self.y_coord)
                with it('should take a character argument'):
                    self.sut.fromHere('N')
                with context('if an invalid direction is supplied,'):
                    with it('should raise an InvalidDirectionError if character is not in [N,E,S,W]'):
                        valid_dirs_ordinals = (ord('N'),ord('E'),ord('S'),ord('W'))
                        invalid_dirs = [chr(code) for code in range(ord('A'), ord('Z')+1) if code not in valid_dirs_ordinals]
                        invalid_dirs.extend([chr(code) for code in range(ord('a'), ord('z')+1)])
                        for ndx in range(0, len(invalid_dirs)):
                            try:
                                self.sut.fromHere(invalid_dirs[ndx])
                                assert(False)
                            except Plateau.InvalidDirectionError:
                                pass
                with context('if a valid direction is supplied,'):
                    with it('should return an object of the same type'):
                        type(self.sut.fromHere('N')).should.equal(type(self.sut))
                    with context('if a direction of N is supplied'):
                        with it('should return an object whose Y() method returns self.Y()+1'):
                            self.sut.fromHere('N').Y().should.equal(self.sut.Y()+1)
                        with it('should return an object whose X() method returns self.X()'):
                            self.sut.fromHere('N').X().should.equal(self.sut.X())
                    with context('if a direction of E is supplied'):
                        with it('should return an object whose Y() method returns self.Y()'):
                            self.sut.fromHere('E').Y().should.equal(self.sut.Y())
                        with it('should return an object whose X() method returns self.X()+1'):
                            self.sut.fromHere('E').X().should.equal(self.sut.X()+1)
                    with context('if a direction of S is supplied'):
                        with it('should return an object whose Y() method returns self.Y()-1'):
                            self.sut.fromHere('S').Y().should.equal(self.sut.Y()-1)
                        with it('should return an object whose X() method returns self.X()'):
                            self.sut.fromHere('S').X().should.equal(self.sut.X())
                    with context('if a direction of W is supplied'):
                        with it('should return an object whose Y() method returns self.Y()'):
                            self.sut.fromHere('W').Y().should.equal(self.sut.Y())
                        with it('should return an object whose X() method returns self.X()-1'):
                            self.sut.fromHere('W').X().should.equal(self.sut.X()-1)

                    with context('if a direction is supplied which would result in an invalid coordinate,'):
                        with context('if the direction is N'):
                            with before.each:
                                self.x_coord, self.y_coord = 1, self.plateau.getDimensions()[1]-1
                                self.sut = self.plateau.getPosition(self.x_coord, self.y_coord)

                            with it('should raise an InvalidCoordinateError'):
                                try:
                                    self.sut.fromHere('N')
                                    assert(False)
                                except Plateau.InvalidCoordinateError:
                                    pass

                        with context('if the direction is E'):
                            with before.each:
                                self.x_coord, self.y_coord = self.plateau.getDimensions()[0]-1, 1
                                self.sut = self.plateau.getPosition(self.x_coord, self.y_coord)

                            with it('should raise an InvalidCoordinateError'):
                                try:
                                    self.sut.fromHere('E')
                                    assert(False)
                                except Plateau.InvalidCoordinateError:
                                    pass

                        with context('if the direction is S'):
                            with before.each:
                                self.x_coord, self.y_coord = 1, 0
                                self.sut = self.plateau.getPosition(self.x_coord, self.y_coord)

                            with it('should raise an InvalidCoordinateError'):
                                try:
                                    self.sut.fromHere('S')
                                    assert(False)
                                except Plateau.InvalidCoordinateError:
                                    pass

                        with context('if the direction is W'):
                            with before.each:
                                self.x_coord, self.y_coord = 0, 1
                                self.sut = self.plateau.getPosition(self.x_coord, self.y_coord)

                            with it('should raise an InvalidCoordinateError'):
                                try:
                                    self.sut.fromHere('W')
                                    assert(False)
                                except Plateau.InvalidCoordinateError:
                                    pass



