
from enum import Enum
import re 

class InputFileParser:

    class FileStates(Enum):
        EOF = -1
        OK = 0

    class ParseState:
        class Result(Enum):
            FAIL = -1
            SUCCESS = 0

        def __init__(self, command_callback):
            self._command_callback = command_callback

    class PlateauConfigState(ParseState):
        class Commands(Enum):
            CREATE_PLATEAU = 0

        def parseString(self, input_string):
            match_regex = re.compile('^Plateau:\s*([0-9]+)\s+([0-9]+)\s*$')
            match_result = match_regex.match(input_string)
            if match_result is None:
                return self.Result.FAIL
            max_x_coord, max_y_coord = int(match_result.group(1)), int(match_result.group(2))
            self._command_callback(self.Commands.CREATE_PLATEAU, max_x_coord, max_y_coord)
            return self.Result.SUCCESS

    class RoverLandingState(ParseState):
        def __init__(self, command_callback):
            super(InputFileParser.RoverLandingState, self).__init__(command_callback)
            self._config = None
            self._name = None

        def getConfig(self):
            return self._config

        def getName(self):
            return self._name 

        def parseString(self, input_string):
            match_regex = re.compile('^\s*([a-zA-Z _0-9]*\w)\s+Landing:\s*([0-9]+)\s+([0-9]+)\s+(\w)\s*$')
            match_result = match_regex.match(input_string)
            if match_result is None:
                return self.Result.FAIL
            self._name = match_result.group(1)
            self._config = int(match_result.group(2)), int(match_result.group(3)), match_result.group(4)
            return self.Result.SUCCESS

    class RoverInstructionsState(ParseState):
        class Commands(Enum):
            CREATE_ROVER = 0

        def __init__(self, command_callback, rover_config):
            super(InputFileParser.RoverInstructionsState, self).__init__(command_callback)
            self._rover_config = rover_config

        def parseString(self, input_string):
            match_regex = re.compile('^\s*([a-zA-Z _0-9]*\w)\s+Instructions:\s*(\w+)\s*$')
            match_result = match_regex.match(input_string)
            rover_name = self._rover_config[0]
            if match_result is None or match_result.group(1) != rover_name:
                return self.Result.FAIL
            callback_commands = [self.Commands.CREATE_ROVER] + list(self._rover_config) + [match_result.group(2)]
            self._command_callback(*callback_commands)
            return self.Result.SUCCESS

    def __init__(self, command_callback):
        self.current_state = InputFileParser.PlateauConfigState(command_callback)

    def getAllInputLines(self):
        pass

    def parseInputFile(self):
        read_state = InputFileParser.FileStates.OK
        for read_state, input_line in self.getAllInputLines():
            if read_state is InputFileParser.FileStates.EOF:
                break
            self.parseInputLine(input_line)

    def parseInputLine(self, input_line):
        result = self.current_state.parseString(input_line)
        self.transitionState(result)

    def transitionState(self, current_state_result):
        pass
