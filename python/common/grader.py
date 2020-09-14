#!/usr/bin/python3

import click
import configparser
import json
import sys
import os.path


def print_empty_gradescope():
    gradescope_json = {}
    gradescope_json["score"] = 0.0
    gradescope_json["output"] = "We were unable to run the tests due to an error in your code."
    gradescope_json["visibility"] = "after_published"
    gradescope_json["stdout_visibility"] = "after_published"
    print(json.dumps(gradescope_json, indent=2))


@click.command(name="pytest-grader")
@click.option('--json-file', type=click.Path(), default="tests.json")
@click.option('--rubric-file', type=click.Path(), default="pytest.ini")
@click.option('--csv', is_flag=True)
@click.option('--gradescope', is_flag=True)
def cmd(json_file, rubric_file, csv, gradescope):

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

    if not os.path.exists(rubric_file):
        fail("Missing rubric file: {}".format(rubric_file))

    config = configparser.ConfigParser(delimiters=('='))
    config.optionxform = lambda option: option
    config.read(rubric_file)

    if "test-points" not in config:
        fail("Error: Rubric file {} does not have a [test-points] section.".format(rubric_file))

    categories = [[name] + value.split(",") for name, value in config["test-points"].items()]
    category_names = [name for name, _, _ in categories]
    cid2name = {cid: name for name, cid, _ in categories}
    total_points = {name: float(points) for name, _, points in categories}

    tests = {cname:{} for cname in category_names}

    for test in results["included"]:
        if test.get("type") == "test":
            test_id = test["attributes"]["name"]
            outcome = test["attributes"]["outcome"]

            if "metadata" in test["attributes"]:
                cid = test["attributes"]["metadata"][0]["category"]
            else:
                fail("ERROR: Incorrect JSON report file (missing metadata)")

            cname = cid2name[cid]

            if outcome == "passed":
                tests[cname][test_id] = 1
            else:
                tests[cname][test_id] = 0

    empty_categories = [cname for cname in category_names if len(tests[cname]) == 0]

    if gradescope:
        gradescope_json = {}
        gradescope_json["tests"] = []

    if len(empty_categories) > 0:
        print("WARNING: The following categories had no test results:", ", ".join(empty_categories), file=sys.stderr)
        print("         Make sure you run py.test without '-k' before you run the grader\n", file=sys.stderr)

        if gradescope:
            gradescope_json["output"] = "We were unable to run some or all of the tests due to an error in your code."

    scores = {}
    for cname in category_names:
        scores[cname] = {}
        num_total = len(tests[cname])
        num_success = sum(tests[cname].values())
        num_failed = num_total - num_success
        scores[cname] = (num_success, num_failed, num_total)

    pscores = []
    pscore = 0.0

    if not csv and not gradescope:
        print("%-62s %-6s / %-10s  %-6s / %-10s" % ("Category", "Passed", "Total", "Score", "Points"))
        print("-" * 100)

    for cname in category_names:
        (num_success, num_failed, num_total) = scores[cname]

        cpoints = total_points[cname]

        if num_total == 0:
            cscore = 0.0
        else:
            cscore = (float(num_success) / num_total) * cpoints

        pscore += cscore

        if not csv and not gradescope:
            print("%-62s %-6i / %-10i  %-6.2f / %-10.2f" % (cname, num_success, num_total, cscore, cpoints))
        elif gradescope:
            gs_test = {}
            gs_test["score"] = cscore
            gs_test["max_score"] = cpoints
            gs_test["name"] = cname

            gradescope_json["tests"].append(gs_test)

    if not csv and not gradescope:
        print("-" * 100)
        print("%81s = %-6.2f / %-10i" % ("TOTAL", pscore, sum(total_points.values())))
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