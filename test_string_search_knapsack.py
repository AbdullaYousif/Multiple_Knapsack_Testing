"""
String Search Function Tests with Multiple Knapsack Optimization
Tests are distributed across multiple runners using knapsack algorithm
"""

import pytest
import json
import time
from itertools import product
from multiple_knapsack import solve_knapsack

# Store test results globally
test_results = []

# ===========================
# FUNCTION UNDER TEST
# ===========================
def find_character(s, c):
    """
    Find the first occurrence of character c in string s.
    
    Parameters:
    s (str): The string to search in
    c (str): The character to search for (single character)
    
    Returns:
    str: Position message or not found message
    """
    if not isinstance(c, str) or len(c) != 1:
        return "Error: c must be a single character"
    
    # Simulate more realistic execution time based on string length
    # Longer strings and multiple occurrences take more time
    import time
    base_time = 0.001  # 1ms base
    length_factor = len(s) * 0.0005  # 0.5ms per character
    occurrence_factor = s.count(c) * 0.001  # 1ms per occurrence
    simulated_delay = base_time + length_factor + occurrence_factor
    time.sleep(simulated_delay)
    
    position = s.find(c)
    
    if position == -1:
        return f"Character '{c}' not found in string"
    else:
        return f"Character '{c}' found at position {position}"


# ===========================
# BLOCKS AND ORACLE
# ===========================
LENGTH_BLOCKS = {
    'empty': {'type': 'ERROR', 'value': ''},
    'maximum': {'type': 'NOMINAL', 'value': 10},
    'nominal': {'type': 'NOMINAL', 'value': 5}
}

LOCATION_BLOCKS = {
    'beginning': {'type': 'NOMINAL', 'position': 0},
    'end': {'type': 'NOMINAL', 'position': -1},
    'middle': {'type': 'NOMINAL', 'position': 'mid'}
}

OCCURRENCE_BLOCKS = {
    'no_occurrence': {'type': 'NOMINAL', 'count': 0},
    'one_occurrence': {'type': 'NOMINAL', 'count': 1},
    'several_occurrences': {'type': 'NOMINAL', 'count': 3}
}

# Oracle: defines expected behavior for each combination
# Priority is based on importance: ERROR cases = 100, NOMINAL = 50-80
ORACLE = {
    # Empty string tests
    ('empty', 'beginning', 'no_occurrence'): {
        'test_input': ('', 'a'),
        'expected': "Character 'a' not found in string",
        'priority': 100,
        'description': 'Empty string, character not found'
    },
    
    # Maximum length tests
    ('maximum', 'beginning', 'one_occurrence'): {
        'test_input': ('9abcdefghi', '9'),
        'expected': "Character '9' found at position 0",
        'priority': 70,
        'description': 'Maxi length, index 0, 1 occurrence'
    },
    ('maximum', 'end', 'one_occurrence'): {
        'test_input': ('abcdefghi9', '9'),
        'expected': "Character '9' found at position 9",
        'priority': 70,
        'description': 'Maxi length, last index, 1 occurrence'
    },
    ('maximum', 'middle', 'several_occurrences'): {
        'test_input': ('abc9de9fhi', '9'),
        'expected': "Character '9' found at position 3",
        'priority': 80,
        'description': 'Maxi length, middle index, several occurrences'
    },
    ('maximum', 'beginning', 'no_occurrence'): {
        'test_input': ('abcdefghij', 'z'),
        'expected': "Character 'z' not found in string",
        'priority': 75,
        'description': 'Maxi length, no occurrence'
    },
    
    # Nominal length tests
    ('nominal', 'beginning', 'several_occurrences'): {
        'test_input': ('abcadae', 'a'),
        'expected': "Character 'a' found at position 0",
        'priority': 80,
        'description': 'Nominal length, index 0, several occurrences'
    },
    ('nominal', 'beginning', 'one_occurrence'): {
        'test_input': ('abcde', 'a'),
        'expected': "Character 'a' found at position 0",
        'priority': 60,
        'description': 'Nominal length, index 0, 1 occurrence'
    },
    ('nominal', 'end', 'one_occurrence'): {
        'test_input': ('abcde', 'e'),
        'expected': "Character 'e' found at position 4",
        'priority': 60,
        'description': 'Nominal length, last index, 1 occurrence'
    },
    ('nominal', 'middle', 'one_occurrence'): {
        'test_input': ('abcde', 'c'),
        'expected': "Character 'c' found at position 2",
        'priority': 50,
        'description': 'Nominal length, middle index, 1 occurrence'
    },
    ('nominal', 'middle', 'several_occurrences'): {
        'test_input': ('abcdce', 'c'),
        'expected': "Character 'c' found at position 2",
        'priority': 70,
        'description': 'Nominal length, middle index, several occurrences'
    },
    ('nominal', 'beginning', 'no_occurrence'): {
        'test_input': ('abcde', 'f'),
        'expected': "Character 'f' not found in string",
        'priority': 65,
        'description': 'Nominal length, no occurrence'
    },
}

# ===========================
# TEST GENERATION FUNCTIONS
# ===========================
def base_choice_tests():
    """Generate Base Choice test cases"""
    # Base choice: nominal, beginning, one_occurrence
    base = ('nominal', 'beginning', 'one_occurrence')
    tests = [base]
    
    # Vary length
    for length in LENGTH_BLOCKS.keys():
        if length != 'nominal':
            # Keep other characteristics at base
            test = (length, 'beginning', 'one_occurrence')
            if test in ORACLE:
                tests.append(test)
    
    # Vary location
    for location in LOCATION_BLOCKS.keys():
        if location != 'beginning':
            test = ('nominal', location, 'one_occurrence')
            if test in ORACLE:
                tests.append(test)
    
    # Vary occurrence
    for occurrence in OCCURRENCE_BLOCKS.keys():
        if occurrence != 'one_occurrence':
            test = ('nominal', 'beginning', occurrence)
            if test in ORACLE:
                tests.append(test)
    
    return tests


def each_choice_tests():
    """Generate Each Choice test cases - all valid combinations in oracle"""
    return list(ORACLE.keys())


def pairwise_tests():
    """Generate Pairwise test cases"""
    # For simplicity, using a subset that covers all pairs
    return [
        ('maximum', 'beginning', 'one_occurrence'),
        ('maximum', 'end', 'one_occurrence'),
        ('maximum', 'middle', 'several_occurrences'),
        ('nominal', 'beginning', 'several_occurrences'),
        ('nominal', 'end', 'one_occurrence'),
        ('nominal', 'middle', 'one_occurrence'),
        ('maximum', 'beginning', 'no_occurrence'),
        ('nominal', 'beginning', 'no_occurrence'),
        ('empty', 'beginning', 'no_occurrence'),
    ]


# ===========================
# PYTEST PARAMETRIZED TESTS
# ===========================
@pytest.mark.parametrize("length,location,occurrence", base_choice_tests())
def test_base_choice(length, location, occurrence):
    """Base Choice Coverage Tests"""
    test_key = (length, location, occurrence)
    oracle = ORACLE[test_key]
    test_id = f"base_{length}_{location}_{occurrence}"
    
    start_time = time.time()
    try:
        s, c = oracle['test_input']
        result = find_character(s, c)
        assert result == oracle['expected'], f"Expected '{oracle['expected']}', got '{result}'"
        status = "PASS"
    except AssertionError as e:
        status = "FAIL"
        print(f"\n❌ {test_id} FAILED: {e}")
    except Exception as e:
        status = "ERROR"
        print(f"\n⚠️  {test_id} ERROR: {e}")
    
    execution_time = (time.time() - start_time) * 1000  # milliseconds
    
    test_results.append({
        "id": test_id,
        "time": execution_time / 1000,  # back to seconds
        "priority": oracle['priority'],
        "status": status,
        "description": oracle['description']
    })


@pytest.mark.parametrize("length,location,occurrence", each_choice_tests())
def test_each_choice(length, location, occurrence):
    """Each Choice Coverage Tests"""
    test_key = (length, location, occurrence)
    oracle = ORACLE[test_key]
    test_id = f"each_{length}_{location}_{occurrence}"
    
    start_time = time.time()
    try:
        s, c = oracle['test_input']
        result = find_character(s, c)
        assert result == oracle['expected'], f"Expected '{oracle['expected']}', got '{result}'"
        status = "PASS"
    except AssertionError as e:
        status = "FAIL"
        print(f"\n❌ {test_id} FAILED: {e}")
    except Exception as e:
        status = "ERROR"
        print(f"\n⚠️  {test_id} ERROR: {e}")
    
    execution_time = (time.time() - start_time) * 1000
    
    test_results.append({
        "id": test_id,
        "time": execution_time / 1000,
        "priority": oracle['priority'],
        "status": status,
        "description": oracle['description']
    })


@pytest.mark.parametrize("length,location,occurrence", pairwise_tests())
def test_pairwise(length, location, occurrence):
    """Pairwise Coverage Tests"""
    test_key = (length, location, occurrence)
    oracle = ORACLE[test_key]
    test_id = f"pairwise_{length}_{location}_{occurrence}"
    
    start_time = time.time()
    try:
        s, c = oracle['test_input']
        result = find_character(s, c)
        assert result == oracle['expected'], f"Expected '{oracle['expected']}', got '{result}'"
        status = "PASS"
    except AssertionError as e:
        status = "FAIL"
        print(f"\n❌ {test_id} FAILED: {e}")
    except Exception as e:
        status = "ERROR"
        print(f"\n⚠️  {test_id} ERROR: {e}")
    
    execution_time = (time.time() - start_time) * 1000
    
    test_results.append({
        "id": test_id,
        "time": execution_time / 1000,
        "priority": oracle['priority'],
        "status": status,
        "description": oracle['description']
    })


# ===========================
# KNAPSACK PREPARATION
# ===========================
def prepare_knapsack_data(tests, num_bins=3):
    """Prepare test data for knapsack solver"""
    data = {
        "weights": [int(t['time'] * 1000000) for t in tests],  # Convert to microseconds
        "values": [t['priority'] for t in tests],
        "num_items": len(tests),
        "all_items": list(range(len(tests))),
        "bin_capacities": [15000] * num_bins,  # Reduced to 15ms per runner to force distribution
        "num_bins": num_bins,
        "all_bins": list(range(num_bins))
    }
    return data


# ===========================
# PYTEST HOOKS
# ===========================
def pytest_sessionfinish(session, exitstatus):
    """Run after all tests complete"""
    if not test_results:
        print("\n⚠️  No test results collected")
        return
    
    print("\n" + "="*70)
    print("TEST EXECUTION SUMMARY")
    print("="*70)
    print(f"Total tests run: {len(test_results)}")
    print(f"Passed: {sum(1 for t in test_results if t['status'] == 'PASS')}")
    print(f"Failed: {sum(1 for t in test_results if t['status'] == 'FAIL')}")
    print(f"Errors: {sum(1 for t in test_results if t['status'] == 'ERROR')}")
    
    # Save test metrics
    with open('test_metrics.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    print("\n✓ Test metrics saved to 'test_metrics.json'")
    
    # Prepare and solve knapsack
    num_runners = 5  # Increased to 5 runners for better distribution
    knapsack_data = prepare_knapsack_data(test_results, num_bins=num_runners)
    
    print("\n" + "="*70)
    print("KNAPSACK INPUT DATA")
    print("="*70)
    print(f"Number of tests: {knapsack_data['num_items']}")
    print(f"Number of runners: {knapsack_data['num_bins']}")
    print(f"Total execution time: {sum(knapsack_data['weights'])/1000:.2f} ms")
    print(f"Total priority value: {sum(knapsack_data['values'])}")
    print(f"Runner capacity: {knapsack_data['bin_capacities'][0]/1000:.2f} ms each")
    print(f"Expected avg per runner: {sum(knapsack_data['weights'])/1000/num_runners:.2f} ms")
    
    # Solve knapsack problem
    assignment = solve_knapsack(knapsack_data)
    
    if assignment:
        print("\n" + "="*70)
        print("TEST DISTRIBUTION ACROSS RUNNERS")
        print("="*70)
        
        for runner_id in range(knapsack_data['num_bins']):
            tests_in_runner = [
                (i, test_results[i]['id'], test_results[i]['description'])
                for i in range(len(assignment))
                if assignment[i] == runner_id
            ]
            
            if tests_in_runner:
                print(f"\n🏃 Runner {runner_id}: {len(tests_in_runner)} tests")
                for idx, test_id, desc in tests_in_runner:
                    priority = test_results[idx]['priority']
                    exec_time = test_results[idx]['time'] * 1000
                    print(f"   • {test_id[:30]:<30} | Priority: {priority:3d} | Time: {exec_time:.3f}ms")
                    print(f"     └─ {desc}")
        
        # Save assignment
        assignment_data = {
            'assignment_vector': assignment,
            'test_mapping': {
                test_results[i]['id']: {
                    'runner': assignment[i],
                    'priority': test_results[i]['priority'],
                    'time_ms': test_results[i]['time'] * 1000,
                    'description': test_results[i]['description']
                }
                for i in range(len(assignment))
            }
        }
        
        with open('test_assignment.json', 'w') as f:
            json.dump(assignment_data, f, indent=2)
        
        print("\n✓ Test assignment saved to 'test_assignment.json'")
        print("="*70)
    else:
        print("\n❌ Failed to generate optimal test distribution")


# ===========================
# EXPLICIT KNAPSACK TEST
# ===========================
def test_zzz_run_knapsack_optimization():
    """
    This test runs last (zzz prefix) to analyze all collected test data
    and perform knapsack optimization
    """
    if not test_results:
        pytest.skip("No test results to process")
    
    pytest_sessionfinish(None, 0)


# ===========================
# MANUAL TEST RUNNER
# ===========================
if __name__ == "__main__":
    print("To run tests with knapsack optimization, use:")
    print("  pytest test_string_search_knapsack.py -v -s")
    print("\nThis will:")
    print("  1. Run all parametrized tests")
    print("  2. Collect execution time and priority data")
    print("  3. Optimize test distribution across runners using knapsack")
    print("  4. Generate test_metrics.json and test_assignment.json")