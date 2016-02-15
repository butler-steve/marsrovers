
from InputFileParser import *
from sure import *
from mock import *

with context(InputFileParser):
    with it('should exist and receive a single argument'):
        self.sut = InputFileParser('not really a callback')
    with it('should create a PlateauConfigState'):
        with patch('InputFileParser.InputFileParser.PlateauConfigState') as mock_PlateauConfigState:
            self.sut = InputFileParser('not really a callback')
            mock_PlateauConfigState.called.should.equal(True)
    with it('should pass argument into PlateauConfigState'):
        with patch('InputFileParser.InputFileParser.PlateauConfigState') as mock_PlateauConfigState:
            test_argument = 'not really a callback'
            self.sut = InputFileParser(test_argument)
            mock_PlateauConfigState.assert_called_with(test_argument)

    with context('methods:'):
        with before.each:
            self.sut = InputFileParser(None)
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
            with it('should continue to invoke getAllInputLines() until it returns EOF'):
                with patch('InputFileParser.InputFileParser.getAllInputLines') as mock_getAllInputLines:
                    return_values = [
                            (InputFileParser.FileStates.OK, 'one'),
                            (InputFileParser.FileStates.OK, 'two'),
                            (InputFileParser.FileStates.OK, 'three'),
                            (InputFileParser.FileStates.EOF, 'four'),
                            (InputFileParser.FileStates.OK, 'five')
                        ]
                    num_calls = 0
                    def side_effect():
                        nonlocal num_calls
                        while True:
                            this_value = return_values[num_calls % len(return_values)]
                            num_calls += 1
                            yield this_value
                    mock_getAllInputLines.side_effect = side_effect
                    self.sut.parseInputFile()
                    num_calls.should.equal(4)

            with it('should invoke parseInputLine() method with the current input line'):
                with patch('InputFileParser.InputFileParser.getAllInputLines') as mock_getAllInputLines:
                    with patch('InputFileParser.InputFileParser.parseInputLine') as mock_parseInputLine:
                        test_input_line = 'atestline'
                        mock_getAllInputLines.return_value = [(InputFileParser.FileStates.OK, test_input_line)]

                        self.sut.parseInputFile()
                        self.sut.parseInputLine.assert_called_with(test_input_line)
        with context('.parseInputLine()'):
            with it('should exist'):
                self.sut.parseInputLine.should.be.callable
            with it('should take a string argument'):
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
                self.sut.transitionState('test string')

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

