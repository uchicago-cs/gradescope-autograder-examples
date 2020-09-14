#!/usr/bin/python3

import click
import configparser
import json
import sys
import os.path

# Hard-coded rubric
# TODO: Load from a configuration file

RUBRIC = [
          ("Exercise 1: Addition", "addition", 25.0),
          ("Exercise 2: Multiplication", "multiplication", 25.0)
         ]

def print_empty_gradescope():
    gradescope_json = {}
    gradescope_json["score"] = 0.0
    gradescope_json["output"] = "We were unable to run the tests due to an error in your code."
    gradescope_json["visibility"] = "after_published"
    gradescope_json["stdout_visibility"] = "after_published"
    print(json.dumps(gradescope_json, indent=2))


@click.command(name="criterion-grader")
@click.option('--json-file', type=click.Path(), default="results.json")
@click.option('--csv', is_flag=True)
@click.option('--gradescope', is_flag=True)
def cmd(json_file, csv, gradescope):

    def fail(msg):
        print(msg, file=sys.stderr)

        if gradescope:
            print_empty_gradescope()
            sys.exit(0)
        else:
            sys.exit(1)

    if not os.path.exists(json_file):
        msg = "No such file: {}\n".format(json_file)
        msg += "Make sure you run py.test before running the grader!"

        fail(msg)

    with open(json_file) as f:
        results = json.load(f)

    rubric_ids = [x[1] for x in RUBRIC]

    tests = {}
    for rubric_id in rubric_ids:
        tests[rubric_id] = {}

    for test_suite in results["test_suites"]:
        rubric_entry = test_suite["name"]
        
        for test in test_suite["tests"]:
            test_id = test["name"]
            if test["status"] == "PASSED":
                tests[rubric_entry][test_id] = 1
            else:
                tests[rubric_entry][test_id] = 0

    scores = {}

    for rubric_id in rubric_ids:
        num_total = len(tests[rubric_id])
        num_success = sum(tests[rubric_id].values())
        num_failed = num_total - num_success
        scores[rubric_id] = (num_success, num_failed, num_total)

    empty_categories = [rubric_id for rubric_id in rubric_ids if len(tests[rubric_id]) == 0]

    if gradescope:
        gradescope_json = {}
        gradescope_json["tests"] = []

    if len(empty_categories) > 0:
        msg  = "WARNING: The following test suites had no test results:", ", ".join(empty_categories)
        msg += "\n         Make sure you run py.test without '-k' before you run the grader\n"

        fail(msg)

    pscores = []
    pscore = 0.0

    if not csv and not gradescope:
        print("%-62s %-6s / %-10s  %-6s / %-10s" % ("Category", "Passed", "Total", "Score", "Points"))
        print("-" * 100)

    total_points = 0.0
    for rubric_name, rubric_id, rubric_points in RUBRIC:
        total_points += rubric_points

        (num_success, num_failed, num_total) = scores[rubric_id]

        if num_total == 0:
            cscore = 0.0
        else:
            cscore = (float(num_success) / num_total) * rubric_points

        pscore += cscore

        if not csv and not gradescope:
            print("%-62s %-6i / %-10i  %-6.2f / %-10.2f" % (rubric_name, num_success, num_total, cscore, rubric_points))
        elif gradescope:
            gs_test = {}
            gs_test["score"] = cscore
            gs_test["max_score"] = rubric_points
            gs_test["name"] = rubric_name

            gradescope_json["tests"].append(gs_test)

    if not csv and not gradescope:
        print("-" * 100)
        print("%81s = %-6.2f / %-10i" % ("TOTAL", pscore, total_points))
        print("=" * 100)
        print()
    pscores.append(pscore)

    if csv:
        print(",".join([str(s) for s in pscores]))
    elif gradescope:
        gradescope_json["score"] = pscore
        gradescope_json["visibility"] = "after_published"
        gradescope_json["stdout_visibility"] = "after_published"

        print(json.dumps(gradescope_json, indent=2))

if __name__ == "__main__":
    cmd()