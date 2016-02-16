import sys
from InputFileParser import *
from Plateau import *
from Rover import *

plateau = None 

def main():
    if len(sys.argv) < 2:
        print("Syntax: python MarsRovers.py <input_filename>")
        exit()
    do_file_parse(sys.argv[1])

def commandInterpreter(command, *args):
    global plateau
    if command is InputFileParser.PlateauConfigState.Commands.CREATE_PLATEAU:
        plateau = Plateau(args[0]+1, args[1]+1)
    elif command is InputFileParser.RoverInstructionsState.Commands.CREATE_ROVER:
        rover_name = args[0]
        rover_position = tuple(args[1:3])
        rover_bearing = args[3]
        rover_instructions = args[4]

        rover = Rover(rover_name, plateau.getPosition(*rover_position), rover_bearing)

        execute_rover_instructions(rover, rover_instructions)
        print_rover_position(rover)

def execute_rover_instructions(rover, instructions):
    try:
        for this_char in instructions:
            if this_char is 'L':
                rover.rotate(True)
            elif this_char is 'R':
                rover.rotate()
            elif this_char is 'M':
                rover.advance()
            else:
                raise InputFileParser.BadFileFormatError
    except Plateau.InvalidCoordinateError:
        print('Rover tried to drive off the plateau!')

def print_rover_position(rover):
    print('{0}:{1} {2} {3}'.format(rover.getName(), rover.getPosition()[0], rover.getPosition()[1], rover.getBearing()))

def do_file_parse(input_filename):
    file_parser = InputFileParser(commandInterpreter, input_filename)
    file_parser.parseInputFile()

if __name__ == '__main__':
    main()

