# marsrovers

My solution to a coding problem sent to me by an interviewer.

# The Problem

The Problem involves sending remote commands to rovers on Mars, read from a formatted input file. The rovers can land on arbitrarily configured plateaus and have position coordinates relative to the plateau.  The full statement of the problem has been omitted here by request of the author.

# Solution
I constructed a solution to the problem using Behaviour-Driven Development (BDD) in Python 3.

## Features
The implementation of the solution features:
- An initial UML class diagram representing the domain model (for conceptualization purposes - this does not reflect the final code architecture)
- Low cohesion among the main classes: Plateau, Rover, and InputFileParser
  - For example: The InputFileParser does not know about Rovers or Plateaus, but instead generates commands to pass to an interpreter function injected from the client. 
- Responsibility assignment following the [Low Representational Gap](http://www.csci.csusb.edu/dick/cs375/12q.html#Chapter%2012%20pages%20271-319%20--%20LRG) design principle
  - For example: The Rover class does not include logic to manage the Rover's position, but instead requests position changes from the environment (ie. Plateau).  This is more reflective of real-world behaviour.
- Parsing using a State machine Design Pattern in InputFileParser

## Running

Takes input files with this format:
```
Plateau:<max_x_coord> <max_y_coord>
<Rover name> Landing:<x_coord> <y_coord> <orientation>
<Rover name> Instructions:<string of single letter instructions>
```

Rover instructions include:
- 'L' - rotate counter-clockwise
- 'R' - rotate clockwise
- 'M' - go forward


To execute the solution from the src sub-directory:

```
python MarsRovers.py sampleInput.txt
```

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

