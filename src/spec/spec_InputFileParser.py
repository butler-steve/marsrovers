
from InputFileParser import *
from sure import *
from mock import *

with context(InputFileParser):
    with it('should exist and two arguments'):
        self.sut = InputFileParser('not really a callback', 'not really a filename')
    with it('should create a PlateauConfigState'):
        with patch('InputFileParser.InputFileParser.PlateauConfigState') as mock_PlateauConfigState:
            self.sut = InputFileParser('not really a callback', 'not really a filename')
            mock_PlateauConfigState.called.should.equal(True)
    with it('should pass argument into PlateauConfigState'):
        with patch('InputFileParser.InputFileParser.PlateauConfigState') as mock_PlateauConfigState:
            test_argument = 'not really a callback'
            self.sut = InputFileParser(test_argument, 'test filename')
            mock_PlateauConfigState.assert_called_with(test_argument)

    with context('methods:'):
        with before.each:
            self.sut = InputFileParser(None, '')
        with context('.getAllInputLines()'):
            with it('should exist'):
                self.sut.getAllInputLines.should.be.callable
        with context('.parseInputFile()'):
            with it('should exist'):
                self.sut.parseInputFile.should.be.callable
            with it('should invoke getAllInputLines()'):
                with patch('InputFileParser.InputFileParser.getAllInputLines') as mock_getAllInputLines:
                    mock_getAllInputLines.return_value = []
                    self.sut.parseInputFile()
                    mock_getAllInputLines.called.should.equal(True)
            with it('should invoke parseInputLine() method with the current input line'):
                with patch('InputFileParser.InputFileParser.getAllInputLines') as mock_getAllInputLines:
                    with patch('InputFileParser.InputFileParser.parseInputLine') as mock_parseInputLine:
                        test_input_line = 'atestline'
                        def side_effect():
                            nonlocal test_input_line
                            return [test_input_line]
                        mock_getAllInputLines.side_effect = side_effect

                        self.sut.parseInputFile()
                        self.sut.parseInputLine.assert_called_with(test_input_line)
        with context('.parseInputLine()'):
            with it('should exist'):
                self.sut.parseInputLine.should.be.callable
            with it('should take a string argument'):
                with patch('InputFileParser.InputFileParser.transitionState') as mock_transitionState:
                    self.sut.parseInputLine('test string')
            with it('should pass input string as argument to .parseString() method of current state object'):
                test_input_string = 'this is a test input string'
                self.sut.current_state = Mock()
                self.sut.parseInputLine(test_input_string)
                self.sut.current_state.parseString.assert_called_with(test_input_string)
               
            with it('should pass the return value from parseString() into transitionState()'):
                with patch('InputFileParser.InputFileParser.transitionState') as mock_transitionState:
                    stub_result = 'this is a test input string'
                    self.sut.current_state = Mock()
                    self.sut.current_state.parseString.return_value = stub_result
                    self.sut.parseInputLine('blah')
                    mock_transitionState.assert_called_with(stub_result)
        with context('.transitionState()'):
            with it('should exist'):
                self.sut.transitionState.should.be.callable
            with it('should take an argument'):
                self.sut.transitionState(InputFileParser.ParseState.Result.SUCCESS)
            with context('if current state is PlateauConfigState,'):
                with before.each:
                    self.sut.current_state = InputFileParser.PlateauConfigState(self.sut.command_callback)
                with context('if result argument is SUCCESS'):
                    with it('should set the current state to RoverLandingState'):
                        with patch('InputFileParser.InputFileParser.RoverLandingState') as mock_RoverLandingState:
                            stub_object = Mock()
                            mock_RoverLandingState.return_value = stub_object
                            self.sut.transitionState(InputFileParser.ParseState.Result.SUCCESS)
                            mock_RoverLandingState.called.should.equal(True)
                            self.sut.current_state.should.be(stub_object)
                with context('if result argument is FAIL'):
                    with it('should raise BadFileFormatError'):
                        try:
                            self.sut.transitionState(InputFileParser.ParseState.Result.FAIL)
                            assert(False)
                        except InputFileParser.BadFileFormatError:
                            pass
            with context('if current state is RoverLandingState,'):
                with before.each:
                    self.sut.current_state = InputFileParser.RoverLandingState(self.sut.command_callback)
                with context('if result argument is SUCCESS'):
                    with it('should set the current state to RoverInstructionsState'):
                        with patch('InputFileParser.InputFileParser.RoverInstructionsState') as mock_RoverInstructionsState:
                            stub_object = Mock()
                            mock_RoverInstructionsState.return_value = stub_object
                            self.sut.transitionState(InputFileParser.ParseState.Result.SUCCESS)
                            mock_RoverInstructionsState.called.should.equal(True)
                            self.sut.current_state.should.be(stub_object)
                with context('if result argument is FAIL'):
                    with it('should not change the current state'):
                        current_state = self.sut.current_state
                        self.sut.transitionState(InputFileParser.ParseState.Result.FAIL)
                        self.sut.current_state.should.be(current_state)
            with context('if current state is RoverInstructionsState,'):
                with before.each:
                    self.sut.current_state = InputFileParser.RoverInstructionsState(self.sut.command_callback, ('Rover1', 1, 2, 'N'))
                with context('if result argument is SUCCESS'):
                    with it('should set the current state to RoverLandingState'):
                        with patch('InputFileParser.InputFileParser.RoverLandingState') as mock_RoverLandingState:
                            stub_object = Mock()
                            mock_RoverLandingState.return_value = stub_object
                            self.sut.transitionState(InputFileParser.ParseState.Result.SUCCESS)
                            mock_RoverLandingState.called.should.equal(True)
                            self.sut.current_state.should.be(stub_object)
                with context('if result argument is FAIL'):
                    with it('should set the current state to RoverLandingState'):
                        with patch('InputFileParser.InputFileParser.RoverLandingState') as mock_RoverLandingState:
                            stub_object = Mock()
                            mock_RoverLandingState.return_value = stub_object
                            self.sut.transitionState(InputFileParser.ParseState.Result.FAIL)
                            mock_RoverLandingState.called.should.equal(True)
                            self.sut.current_state.should.be(stub_object)

with context(InputFileParser.ParseState):
    with it('should exist and take a single argument'):
        self.sut = InputFileParser.ParseState('not really a callback')
    with context(InputFileParser.ParseState.Result):
        with it('should exist'):
            InputFileParser.ParseState.Result
        with it('should contain SUCCESS'):
            InputFileParser.ParseState.Result.SUCCESS.should_not.be.none
        with it('should contain FAIL'):
            InputFileParser.ParseState.Result.FAIL.should_not.be.none

with context(InputFileParser.PlateauConfigState):
    with it('should exist'):
        InputFileParser.PlateauConfigState.should.be.callable
    with before.each:
        self.callback = Mock()
        self.sut = InputFileParser.PlateauConfigState(self.callback)
    with context('.parseString()'):
        with it('should take a string argument'):
            self.sut.parseString('Plateau:5 5')
        with context('if provided string starts with something other than "Plateau:",'):
            with it('should return a FAIL result'):
                self.sut.parseString('Incorrect format').should.equal(InputFileParser.ParseState.Result.FAIL)
        with context('if provided string starts with "Plateau:",'):
            with context('if provided string has something other than number pair following colon,'):
                with it('should return a FAIL result'):
                    self.sut.parseString('Plateau:Incorrect format').should.equal(InputFileParser.ParseState.Result.FAIL)
            with context('if provided string has a number pair followed by a string,'):
                with it('should return a FAIL result'):
                    self.sut.parseString('Plateau:5 5 unwanted').should.equal(InputFileParser.ParseState.Result.FAIL)
            with context('if provided string has a number pair followed by a number,'):
                with it('should return a FAIL result'):
                    self.sut.parseString('Plateau:5 5 5').should.equal(InputFileParser.ParseState.Result.FAIL)
            with context('if provided string has a number pair (x,y) following colon,'):
                with it('should invoke supplied callback with (CREATE_PLATFORM,x,y)'):
                    self.sut.parseString('Plateau:5 5')
                    self.callback.assert_called_with(InputFileParser.PlateauConfigState.Commands.CREATE_PLATEAU, 5, 5)
                with it('should return a SUCCESS result'):
                    self.sut.parseString('Plateau:5 5').should.equal(InputFileParser.ParseState.Result.SUCCESS)
                with it('should ignore >1 whitespace characters between tokens'):
                    self.sut.parseString('Plateau:  \t 29\t\t58   ').should.equal(InputFileParser.ParseState.Result.SUCCESS)

with context(InputFileParser.RoverLandingState):
    with it('should exist'):
        InputFileParser.RoverLandingState.should.be.callable
    with context('methods:'):
        with before.each:
            self.callback = Mock()
            self.sut = InputFileParser.RoverLandingState(self.callback)
        with context('.getConfig()'):
            with it('should exist'):
                self.sut.getConfig.should.be.callable
        with context('.getName()'):
            with it('should exist'):
                self.sut.getName.should.be.callable
        with context('.parseString()'):
            with it('should take a string argument'):
                self.sut.parseString('Rover1 Landing:1 2 N')
            with context('if provided string does not contain "Landing:"'):
                with it('should return a FAIL result'):
                    self.sut.parseString('Rover1 Blanding:1 3 N').should.equal(InputFileParser.ParseState.Result.FAIL)
            with context('if provided string does contain "Landing:"'):
                with it('should return the string prefix from getName()'):
                    test_name = "    This is a name    "
                    self.sut.parseString('{0}Landing:8 9 Z'.format(test_name))
                    self.sut.getName().should.equal(test_name.rstrip().lstrip())
                with context('if provided string has a number pair (x,y) and character z following colon,'):
                    with it('should return (x,y,z) from getConfig()'):
                        self.sut.parseString('Rover1 Landing:8 9 Z')
                        self.sut.getConfig().should.equal((8,9,'Z'))
                    with it('should return a SUCCESS result'):
                        self.sut.parseString('Rover1 Landing:8 9 Z').should.equal(InputFileParser.ParseState.Result.SUCCESS)

with context(InputFileParser.RoverInstructionsState):
    with it('should exist'):
        InputFileParser.RoverInstructionsState.should.be.callable
    with it('should take two arguments: a callback and a tuple'):
        self.sut = InputFileParser.RoverInstructionsState(Mock(), ('Rover1', 8, 9, 'Z'))
    with context('methods:'):
        with before.each:
            self.callback = Mock()
            self.rover_config = ('Rover1', 8, 9, 'Z')
            self.sut = InputFileParser.RoverInstructionsState(self.callback, self.rover_config)
        with context('.parseString()'):
            with it('should exist'):
                self.sut.parseString.should.be.callable
            with it('should take a string argument'):
                self.sut.parseString('Rover1 Instructions:MMRMMRMRRM')
            with context('if provided string does not contain "Instructions:"'):
                with it('should return a FAIL result'):
                    self.sut.parseString('Rover1 Binstructions:MMRMMRMRRM').should.equal(InputFileParser.ParseState.Result.FAIL)
            with context('if provided string does contain "Instructions:"'):
                with context('if name does not match provided config info'):
                    with it('should return a FAIL result'):
                        self.sut.parseString('Rover2 Instructions:MMRMMRMRRM').should.equal(InputFileParser.ParseState.Result.FAIL)
                with context('if name does match provided config info'):
                    with it('should pass the rover_config and string contents following colon to supplied callback, with command CREATE_ROVER'):
                        rover_instructions = 'MMRMMRMRRM'
                        self.sut.parseString('{0} Instructions: {1}'.format(self.rover_config[0], rover_instructions))
                        expected_args = [InputFileParser.RoverInstructionsState.Commands.CREATE_ROVER] + list(self.rover_config) + [rover_instructions]
                        self.callback.assert_called_with(*expected_args)
                    with it('should return a SUCCESS result'):
                        self.sut.parseString('Rover1 Instructions:MMRMMRMRRM').should.equal(InputFileParser.ParseState.Result.SUCCESS)

