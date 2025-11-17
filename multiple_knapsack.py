"""
Multiple Knapsack Problem Solver
Distributes test cases across multiple runners (bins) to maximize priority value
while respecting time constraints.
"""

from ortools.linear_solver import pywraplp


def solve_knapsack(data):
    """
    Solve the multiple knapsack problem for test distribution.
    
    Args:
        data (dict): Dictionary containing:
            - weights: list of test execution times (in microseconds)
            - values: list of test priorities
            - num_items: number of tests
            - all_items: list of test indices
            - bin_capacities: list of capacity for each runner
            - num_bins: number of runners/bins
            - all_bins: list of bin indices
    
    Returns:
        list: Assignment vector where assignment[i] = bin_id for test i
              Returns None if no solution found
    """
    # Create the MIP solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("ERROR: Could not create solver")
        return None

    # Variables
    # x[i, j] = 1 if item i is packed in bin j
    x = {}
    for i in data['all_items']:
        for j in data['all_bins']:
            x[(i, j)] = solver.IntVar(0, 1, f'x_{i}_{j}')

    # Constraints
    # Each item is assigned to at most one bin
    for i in data['all_items']:
        solver.Add(sum(x[i, j] for j in data['all_bins']) <= 1)

    # The amount packed in each bin cannot exceed its capacity
    for j in data['all_bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i] for i in data['all_items']) 
            <= data['bin_capacities'][j]
        )

    # Objective: maximize total value of packed items
    objective = solver.Objective()
    for i in data['all_items']:
        for j in data['all_bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    # Solve
    print('\n' + '='*60)
    print('SOLVING MULTIPLE KNAPSACK PROBLEM')
    print('='*60)
    status = solver.Solve()

    # Process results
    if status == pywraplp.Solver.OPTIMAL:
        print(f'✓ Optimal solution found!')
        print(f'Total priority value = {objective.Value()}')
        print()
        
        # Create assignment vector
        assignment = [-1] * data['num_items']  # -1 means not assigned
        
        # Track bin statistics
        bin_weights = [0] * data['num_bins']
        bin_values = [0] * data['num_bins']
        bin_counts = [0] * data['num_bins']
        
        for j in data['all_bins']:
            print(f'Runner {j}:')
            bin_weight = 0
            bin_value = 0
            items_in_bin = []
            
            for i in data['all_items']:
                if x[i, j].solution_value() > 0:
                    items_in_bin.append(i)
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]
                    assignment[i] = j
            
            bin_weights[j] = bin_weight
            bin_values[j] = bin_value
            bin_counts[j] = len(items_in_bin)
            
            print(f'  Tests assigned: {len(items_in_bin)}')
            print(f'  Total time: {bin_weight/1000:.2f} ms (capacity: {data["bin_capacities"][j]/1000:.2f} ms)')
            print(f'  Total priority value: {bin_value}')
            print(f'  Utilization: {(bin_weight/data["bin_capacities"][j])*100:.1f}%')
            print()
        
        # Summary statistics
        print('='*60)
        print('DISTRIBUTION SUMMARY:')
        print(f'  Total tests: {data["num_items"]}')
        print(f'  Tests assigned: {sum(1 for a in assignment if a != -1)}')
        print(f'  Tests not assigned: {sum(1 for a in assignment if a == -1)}')
        print(f'  Average tests per runner: {sum(bin_counts)/data["num_bins"]:.1f}')
        print(f'  Average utilization: {sum(bin_weights[j]/data["bin_capacities"][j] for j in data["all_bins"])/data["num_bins"]*100:.1f}%')
        print('='*60)
        
        return assignment
    
    elif status == pywraplp.Solver.FEASIBLE:
        print('⚠ Feasible solution found (not optimal)')
        print(f'Total priority value = {objective.Value()}')
        
        assignment = [-1] * data['num_items']
        for j in data['all_bins']:
            for i in data['all_items']:
                if x[i, j].solution_value() > 0:
                    assignment[i] = j
        
        return assignment
    
    else:
        print('✗ No solution found.')
        print(f'Solver status: {status}')
        return None


def solve_knapsack_greedy(data):
    """
    Greedy approximation algorithm for multiple knapsack.
    Useful as a fallback if OR-Tools is not available.
    
    Sorts items by value/weight ratio and assigns to bins with available capacity.
    """
    # Calculate value-to-weight ratio
    items_with_ratio = []
    for i in data['all_items']:
        if data['weights'][i] > 0:
            ratio = data['values'][i] / data['weights'][i]
        else:
            ratio = float('inf')
        items_with_ratio.append((i, ratio, data['weights'][i], data['values'][i]))
    
    # Sort by ratio (descending)
    items_with_ratio.sort(key=lambda x: x[1], reverse=True)
    
    # Initialize bins
    assignment = [-1] * data['num_items']
    bin_remaining = data['bin_capacities'].copy()
    
    print('\n' + '='*60)
    print('SOLVING WITH GREEDY ALGORITHM')
    print('='*60)
    
    # Assign items to bins
    for item_id, ratio, weight, value in items_with_ratio:
        # Find bin with enough capacity
        for bin_id in data['all_bins']:
            if bin_remaining[bin_id] >= weight:
                assignment[item_id] = bin_id
                bin_remaining[bin_id] -= weight
                break
    
    # Print results
    assigned_count = sum(1 for a in assignment if a != -1)
    total_value = sum(data['values'][i] for i in data['all_items'] if assignment[i] != -1)
    
    print(f'✓ Greedy solution completed')
    print(f'Tests assigned: {assigned_count}/{data["num_items"]}')
    print(f'Total priority value: {total_value}')
    print('='*60)
    
    return assignment


if __name__ == "__main__":
    # Example usage
    test_data = {
        "weights": [20, 30, 10, 40, 25],  # microseconds
        "values": [60, 10, 40, 12, 80],      # priority
        "num_items": 5,
        "all_items": list(range(5)),
        "bin_capacities": [50, 50, 50],     # 3 runners
        "num_bins": 3,
        "all_bins": list(range(3))
    }
    
    assignment = solve_knapsack(test_data)
    
    if assignment:
        print("\nFinal Assignment:")
        for i, bin_id in enumerate(assignment):
            if bin_id != -1:
                print(f"  Test {i} → Runner {bin_id}")
            else:
                print(f"  Test {i} → NOT ASSIGNED")