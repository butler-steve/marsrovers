
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
