# Table of Contents
1. [Synopsis](README.md#synopsis)
2. [Code Example](README.md#code-example)
3. [Motivation](README.md#motivation)
4. [Library Dependencies](README.md#library-dependencies)
5. [Tests](README.md#tests)
6. [Comments](README.md#comments)


# Synopsis

A platform which analyzes purchases within a social network of users and detects any behavior that is far from average within the social network.

Implemented as a part of coding challenge for Insight Data Engineering Fellowship application.

# Code Example

You can run the program with the following command from within the main folder:

    ~$ ./run.sh

Execution command is

    ~$ python ./src/python/run_stream.py ./log_input/batch_log.json ./log_input/stream_log.json ./log_output/flagged_purchases.json

All code resides within

    '/src/python'.

Unit Tests reside in

    'src/tests/unit_tests.py'.

The engine execution is made using the python file 'run_stream.py'

The command is also available in the 'run.sh' file.

### Run File for Execution

main file:

    ./src/python/run_stream.py

### System Command Line Arguments

batch log input file path:

    ./log_input/batch_log.json

stream log input file path:

    ./log_input/stream_log.json

flagged purchases output file path:

    ./log_output/flagged_purchases.json

### Working

The actual logic and processing is done in

    '/src/python/engine.py'

The object for storing individual profile state is derived from

    '/src/python/user_profile.py'

The parameters are collected from the batch_log and stream_log json files.

Output is stored in the output file path passed as command line arguments.

# Motivation

Implemented as a part of coding challenge for Insight Data Engineering Fellowship application.

# Library Dependencies

### Python packages used:

    json
    dateutil
    collections
    sys
    os
    random
    numpy
    pytest (for writing unit test cases)

### External packages

    numpy
    pytest

### Install instructions for packages

    pip install packagename

    eg: pip install numpy

# Tests

### Unit Tests

Unit tests present in '/src/tests/unit_tests.py'

They can be run using the command '$ py.test -q unit_tests.py'

### Component and Functionality Tests

Custom tests added in '/insight_testsuite/tests/'

# Comments

i) Few warnings are raised by numpy when an empty list is sent for mean and standard deviation calculation, this is perfectly safe and tested for errors.

ii) An Edge case to take care of while evaluating:

Truncating (as opposed to rounding) the mean and standard deviation values as a string to two decimal points without rounding the number is probably a bad idea.

Using the example in the question:

Truncating eg: 3.46732 is truncated as 3.46. This is not really an optimal method.
               The only way to do this is converting it to String and slicing the values or typecasting to int and recasting to String.
               I have implemented this in my solution as the example in the question demanded this.

Rounding eg: Using the round(3.46732, 2) method rounds 3.46732 as 3.47. This is the ideal method for such kind of operations.















