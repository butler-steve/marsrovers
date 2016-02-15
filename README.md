# marsrovers

My solution to a coding problem sent to me by an interviewer.

# The Problem

The Problem involves sending remote commands to rovers on Mars, read from a formatted input file. The rovers can land on arbitrarily configured plateaus and have position coordinates relative to the plateau.  The full statement of the problem has been omitted here by request of the author.

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

