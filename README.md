# marsrovers

My solution to a coding problem sent to me by an interviewer.

# The Problem

A squad of robotic rovers are to be landed by NASA on a plateau on Mars.

This plateau, which is curiously rectangular, must be navigated by the rovers so that their on board cameras can get a complete view of the surrounding terrain to send back to Earth.

A rover's position is represented by a combination of an x and y co-ordinates and a letter representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify navigation. An example position might be 0, 0, N, which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters are 'L', 'R' and 'M'. 'L' and 'R' makes the rover spin 90 degrees left or right respectively, without moving from its current spot.

'M' means move forward one grid point, and maintain the same heading.

Assume that the square directly North from (x, y) is (x, y+1).

## Input
### Configuration Input
The first line of input is the upper-right coordinates of the plateau, the lower-left coordinates are assumed to be 0,0.
Per Rover.
#### Test Input
`8 4`

### Input 1
Landing co-ordinates for the Rover The position is made up of two integers and a letter separated by spaces, corresponding to the x and y co-ordinates and the rover's orientation.
#### Test Input
`1 2 N`

### Input 2
Navigation instructions i.e a string containing ('L', 'R', 'M').
#### Test Input
`LMLMLMLMM`

## Sample Input
```
Plateau:5 5
Rover1 Landing:1 2 N
Rover1 Instructions:LMLMLMLMM
Rover2 Landing:3 3 E
Rover2 Instructions:MMRMMRMRRM
```

### Expected Output:
```
Rover1:1 3 N
Rover2:5 1 E
```
## Task
Develop a command line app that can take the various inputs from the command line and generate the desired outputs.

# Solution
I constructed a solution to the problem using Behaviour-Driven Development (BDD) in Python 3.

## Testing Environment

- Python 3.5.1
- mamba 0.8.6
- mockito 0.5.2

### Setup Steps

Install all dependent pip packages: 
```
> pip install -r requirements.txt
```

Install modified version of mockito (because the real version fails to install due to an error):
```
> cd marsrovers
> pip install -e pip-cache/mockito-0.5.2
```

Run the spec files using mamba:
```
> mamba src/spec/spec*.py
```

