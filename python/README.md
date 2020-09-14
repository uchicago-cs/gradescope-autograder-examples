Python Autograder Example
=========================

In this example, we run a series of unit tests using [pytest](https://docs.pytest.org/en/stable/), and use the result of those tests to compute a score for the Gradescope autograder.

This directory contains the following

- `autograder/`: The autograder files
- `common/`: Contains the grading script that takes the JSON produced by `pytest` and either produces a human-readable report or JSON that can be consumed by the Gradescope autograder.
- `dist/`: The "distribution" code (the code we would give to the students)
- `soln/`: The solution code.

If you set up a Gradescope autograder with this code, you will need to submit the `arithmetic.py` file from the `soln/` directory.

Running the tests
-----------------

To run the tests, simply run `pytest` inside the `dist` or `soln` directory.

For example, if you ran it from inside the `soln` directory:

    $ pytest 
    ============================= test session starts ==============================
    platform linux -- Python 3.8.2, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
    rootdir: /home/borja/repos/gradescope-autograder-examples/python/soln, configfile: pytest.ini
    plugins: json-0.4.0, metadata-1.10.0
    collected 10 items                                                             

    test_arithmetic.py ..........                                            [100%]

    - generated json report: /home/borja/repos/gradescope-autograder-examples/python/soln/tests.json -
    ============================== 10 passed in 0.01s ==============================


Running the grading script
--------------------------

After running the tests, you can produce a human-readable report like this:

    $ ../common/grader.py 
    Category                                                       Passed / Total       Score  / Points    
    ----------------------------------------------------------------------------------------------------
    Exercise 1: Addition                                           5      / 5           25.00  / 25.00     
    Exercise 2: Multiply                                           5      / 5           25.00  / 25.00     
    ----------------------------------------------------------------------------------------------------
                                                                                TOTAL = 50.00  / 50        
    ====================================================================================================


Or see the Gradescope JSON like this:

    $ ../common/grader.py --gradescope
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
        "name": "Exercise 2: Multiply"
        }
    ],
    "score": 50.0,
    "visibility": "after_published",
    "stdout_visibility": "after_published"
    }

