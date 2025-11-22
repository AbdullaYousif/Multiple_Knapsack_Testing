from testflows.combinatorics import CoveringArray
from multiple_knapsack_SUT import multiple_knapsack_SUT
import argparse

#generating pairwise, third-order, and fourth-order test cases given the parameters
parameters = ({
  "num_items": [10, 50, 100, 500],
  "num_knapsacks": [1, 2, 5, 10],
  "item_weights": [5, 20, 50, 100],
  "item_values": [5, 50, 250, 1000],
  "bin_capacity": [100, 200, 500, 1000],
})


def generate_test_inputs(test_case):
    """Takes test case parameters and converts them into inputs for the SUT (System Under Test)."""
    num_items = test_case["num_items"]
    num_knapsacks = test_case["num_knapsacks"]
    item_weights = test_case["item_weights"]
    item_values = test_case["item_values"]
    bin_capacity = test_case["bin_capacity"]
    
    bin_capacities = [bin_capacity] * num_knapsacks
    weights = [item_weights] * num_items
    values = [item_values] * num_items

    data = {
        "weights": weights,
        "values": values,
        "num_items": num_items,
        "all_items": range(num_items),
        "bin_capacities": bin_capacities,
        "num_bins": num_knapsacks,
        "all_bins": range(num_knapsacks),
        "test_case": test_case
    }
    return data
    

def pairwise_tests():
    """Executes the pairwise combinatorial test suite.
    Generates and runs all pairwise test cases against the multiple knapsack solver, verifying combinatorial coverage for pairwise tests.
    """
    print("Running Pairwise Test Suite")
    pairwise_tests = (CoveringArray(parameters,strength=2))
    for test_case in pairwise_tests:
        data = generate_test_inputs(test_case)
        multiple_knapsack_SUT(data)
    print(f"Pairwise Coverage Check: {pairwise_tests.check()}")

def third_order_tests():
    """Executes the third-order combinatorial test suite.
    Generates and runs all third-order test cases against the multiple knapsack solver, verifying combinatorial coverage for third-order tests.
    """

    print("Running Third-Order Test Suite")
    third_order_tests = (CoveringArray(parameters,strength=3))
    for test_case in third_order_tests:
        data = generate_test_inputs(test_case)
        multiple_knapsack_SUT(data)
    print(f"Third-Order Coverage Check: {third_order_tests.check()}")


def fourth_order_tests():
    """Executes the fourth-order combinatorial test suite.
    Generates and runs all fourth-order test cases against the multiple knapsack solver, verifying combinatorial coverage for fourth-order tests.
    """

    print("Running Fourth-Order Test Suite")
    fourth_order_tests = (CoveringArray(parameters,strength=4))
    for test_case in fourth_order_tests:
        data = generate_test_inputs(test_case)
        multiple_knapsack_SUT(data)
    print(f"Fourth-Order Coverage Check: {fourth_order_tests.check()}")
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Choose which Combinatorial Test Suite to execute (Pairwise, Third-Order, Fourth-Order)")

    parser.add_argument('suite', choices=['pairwise', 'third-order', 'fourth-order'])

    args = parser.parse_args()
    suite_name = args.suite
    if suite_name == 'pairwise':
        pairwise_tests()
    elif suite_name == 'third-order':
        third_order_tests()
    elif suite_name == 'fourth-order':
        fourth_order_tests()
    else:
        print("Invalid Parameter")


#COMMAND FOR RUNNING COVERAGE EXAMPLE: coverage run --branch --source=multiple_knapsack_SUT test_combinatorial.py fourth-order
#COMMAND FOR CHECKING COVERAGE REPORT: coverage report -m

#all test suites have 97% coverage, missing lines 83

#line 9-10 is if solver is unavailable, line has been commented out because branch cannot be reached as it is due to changes in environment

#line 83 is only run when an optimal solution cannot be found, 
# knapsack is an optimization problem, meaning all typical test inputs will be a mathematically optimal solution 
# meaning it will always execute the "if status == pywraplp.Solver.OPTIMAL:" and else branch infeasible


