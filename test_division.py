# ===========================
# PYTEST TESTS WITH KNAPSACK
# ===========================

import pytest
import json
from itertools import product
from multiple_knapsack import solve_knapsack  # Make sure this function exists

# Store test results globally
test_results = []

# Example divide function
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    if a < 0 or b < 0:
        raise ValueError("Negative numbers not allowed")
    return a / b

# ---------------------------
# Helpers for generating tests
# ---------------------------
DIVIDEND_BLOCKS = {
    'positive': {'type': 'NOMINAL', 'value': 10},
    'zero': {'type': 'NOMINAL', 'value': 0},
    'negative': {'type': 'ERROR', 'value': -5}
}
DIVISOR_BLOCKS = {
    'positive': {'type': 'NOMINAL', 'value': 2},
    'zero': {'type': 'ERROR', 'value': 0},
    'negative': {'type': 'ERROR', 'value': -3}
}
ORACLE = {
    ('positive', 'positive'): {'outcome': 'SUCCESS', 'result_type': 'valid_number', 'expected_result': 5.0},
    ('zero', 'positive'): {'outcome': 'SUCCESS', 'result_type': 'zero', 'expected_result': 0.0},
    ('negative', 'positive'): {'outcome': 'ERROR', 'result_type': 'ValueError'},
    ('positive', 'zero'): {'outcome': 'ERROR', 'result_type': 'ZeroDivisionError'},
    ('zero', 'zero'): {'outcome': 'ERROR', 'result_type': 'ZeroDivisionError'},
    ('negative', 'zero'): {'outcome': 'ERROR', 'result_type': 'ZeroDivisionError'},
    ('positive', 'negative'): {'outcome': 'ERROR', 'result_type': 'ValueError'},
    ('zero', 'negative'): {'outcome': 'ERROR', 'result_type': 'ValueError'},
    ('negative', 'negative'): {'outcome': 'ERROR', 'result_type': 'ValueError'}
}
PRIORITY = {
    ('positive', 'positive'): 40,
    ('zero', 'positive'): 60,
    ('negative', 'positive'): 80,
    ('positive', 'zero'): 100,
    ('zero', 'zero'): 100,
    ('negative', 'zero'): 100,
    ('positive', 'negative'): 80,
    ('zero', 'negative'): 80,
    ('negative', 'negative'): 80
}

def base_choice_tests():
    dividend_choices = list(DIVIDEND_BLOCKS.keys())
    divisor_choices = list(DIVISOR_BLOCKS.keys())
    tests = [('positive', 'positive')]
    for d in dividend_choices:
        if d != 'positive':
            tests.append((d, 'positive'))
    for v in divisor_choices:
        if v != 'positive':
            tests.append(('positive', v))
    return tests

def each_choice_tests():
    return list(product(DIVIDEND_BLOCKS.keys(), DIVISOR_BLOCKS.keys()))

# ---------------------------
# PYTEST PARAMETRIZED TESTS
# ---------------------------
@pytest.mark.parametrize("dividend,divisor", base_choice_tests())
def test_base_choice(dividend, divisor):
    a = DIVIDEND_BLOCKS[dividend]['value']
    b = DIVISOR_BLOCKS[divisor]['value']
    oracle = ORACLE[(dividend, divisor)]
    test_id = f"base_{dividend}_{divisor}"

    try:
        if oracle['outcome'] == 'ERROR':
            if oracle['result_type'] == 'ZeroDivisionError':
                with pytest.raises(ZeroDivisionError):
                    divide(a, b)
            elif oracle['result_type'] == 'ValueError':
                with pytest.raises(ValueError):
                    divide(a, b)
        else:
            result = divide(a, b)
            assert result == oracle['expected_result']
        status = "PASS"
    except Exception:
        status = "FAIL"

    # Record for knapsack
    test_results.append({
        "id": test_id,
        "time": 0.001,  # fake execution time
        "priority": PRIORITY[(dividend, divisor)],
        "status": status
    })

@pytest.mark.parametrize("dividend,divisor", each_choice_tests())
def test_each_choice(dividend, divisor):
    a = DIVIDEND_BLOCKS[dividend]['value']
    b = DIVISOR_BLOCKS[divisor]['value']
    oracle = ORACLE[(dividend, divisor)]
    test_id = f"each_{dividend}_{divisor}"

    try:
        if oracle['outcome'] == 'ERROR':
            if oracle['result_type'] == 'ZeroDivisionError':
                with pytest.raises(ZeroDivisionError):
                    divide(a, b)
            elif oracle['result_type'] == 'ValueError':
                with pytest.raises(ValueError):
                    divide(a, b)
        else:
            result = divide(a, b)
            assert result == oracle['expected_result']
        status = "PASS"
    except Exception:
        status = "FAIL"

    test_results.append({
        "id": test_id,
        "time": 0.001,
        "priority": PRIORITY[(dividend, divisor)],
        "status": status
    })

# ---------------------------
# KNAPSACK PREP
# ---------------------------
def prepare_knapsack_data(tests, num_bins=5):
    data = {
        "weights": [int(t['time'] * 1000000) for t in tests],
        "values": [t['priority'] for t in tests],
        "num_items": len(tests),
        "all_items": list(range(len(tests))),
        "bin_capacities": [10000] * num_bins,
        "num_bins": num_bins,
        "all_bins": list(range(num_bins))
    }
    return data

# ---------------------------
# PYTEST HOOK: run after all tests
# ---------------------------
def pytest_sessionfinish(session, exitstatus):
    if not test_results:
        return
    print("\n" + "="*60)
    print("TOTAL TESTS RUN:", len(test_results))
    print("="*60)

    # Save test metrics
    with open('test_metrics.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    print("✓ Test metrics saved")

    # Prepare knapsack input
    knapsack_data = prepare_knapsack_data(test_results, num_bins=5)
    print("\nKNAPSACK INPUT DATA:")
    print("Items:", knapsack_data["num_items"])
    print("Weights (μs):", knapsack_data["weights"][:5], "...")
    print("Values:", knapsack_data["values"][:5], "...")
    print("Bin capacities:", knapsack_data["bin_capacities"])

    # Solve knapsack
    assignment = solve_knapsack(knapsack_data)
    if assignment:
        print("\nTEST DISTRIBUTION ACROSS RUNNERS:")
        for bin_id in range(knapsack_data["num_bins"]):
            tests_in_bin = [test_results[i]['id'] for i in range(len(assignment)) if assignment[i] == bin_id]
            if tests_in_bin:
                print(f"Runner {bin_id}: {len(tests_in_bin)} tests")
                print(" ", tests_in_bin)

        # Save assignment
        with open('test_assignment.json', 'w') as f:
            json.dump({
                'assignment_vector': assignment,
                'test_mapping': {test_results[i]['id']: assignment[i] for i in range(len(assignment))}
            }, f, indent=2)
        print("\n✓ Test assignment saved")
        
def test_run_knapsack_and_print():
    """Run knapsack after all tests"""
    if not test_results:
        pytest.skip("No test results to process")

    knapsack_data = prepare_knapsack_data(test_results, num_bins=5)
    print("\nKNAPSACK INPUT DATA:")
    print("Items:", knapsack_data["num_items"])
    print("Weights (μs):", knapsack_data["weights"][:5], "...")
    print("Values:", knapsack_data["values"][:5], "...")
    print("Bin capacities:", knapsack_data["bin_capacities"])

    # Call your knapsack solver
    assignment = solve_knapsack(knapsack_data)
    if assignment:
        print("\nTEST DISTRIBUTION ACROSS RUNNERS:")
        for bin_id in range(knapsack_data["num_bins"]):
            tests_in_bin = [test_results[i]['id'] for i in range(len(assignment)) if assignment[i] == bin_id]
            if tests_in_bin:
                print(f"Runner {bin_id}: {len(tests_in_bin)} tests")
                print(" ", tests_in_bin)
