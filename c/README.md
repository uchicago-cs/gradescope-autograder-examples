C Autograder Example
====================

In this example, we run a series of unit tests using [Criterion](https://github.com/Snaipe/Criterion), and use the result of those tests to compute a score for the Gradescope autograder.

This directory contains the following

- `autograder/`: The autograder files
- `common/`: Contains the grading script that takes the JSON produced by Criterion and either produces a human-readable report or JSON that can be consumed by the Gradescope autograder.
- `dist/`: The "distribution" code (the code we would give to the students)
- `soln/`: The solution code.

Both the `dist/` and `soln/` directories contain a `include/` directory (for public header files), a `src/` directory (for source code), and a `tests/` directory (for the unit tests).

If you set up a Gradescope autograder with this code, you will need to submit the `arithmetic.c` file from the `soln/src/` directory.

Building the code
-----------------

Building the code requires [CMake](https://cmake.org/).

To build the code, run the following (from either the `dist/` and `soln/` directories):

    $ cmake -S . -B build
    $ cd build
    $ make

Running the tests
-----------------

To run the tests, run the `test-arithmetic` executable inside the `build` directory (after building the code).

For example, if you ran it from inside the `soln` directory:

    $ ./test-arithmetic 
    [====] Synthesis: Tested: 10 | Passing: 10 | Failing: 0 | Crashing: 0


Running the grading script
--------------------------

After running the tests, you can produce a human-readable report like this:

    $ ../tests/grader.py 
    Category                                                       Passed / Total       Score  / Points    
    ----------------------------------------------------------------------------------------------------
    Exercise 1: Addition                                           5      / 5           25.00  / 25.00     
    Exercise 2: Multiplication                                     5      / 5           25.00  / 25.00     
    ----------------------------------------------------------------------------------------------------
                                                                                TOTAL = 50.00  / 50        
    ====================================================================================================


Or see the Gradescope JSON like this:

    $ ../tests/grader.py --gradescope
    {
    "tests": [
        {
        "score": 25.0,
        "max_score": 25.0,
        "name": "Exercise 1: Addition"
        },
        {
        "score": 25.0,
        "max_score": 25.0,
        "name": "Exercise 2: Multiplication"
        }
    ],
    "score": 50.0,
    "visibility": "after_published",
    "stdout_visibility": "after_published"
    }