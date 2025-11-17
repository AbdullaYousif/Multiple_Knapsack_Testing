from multiple_knapsack import solve_knapsack

def test_knapsack_basic():
    # Prepare test data in the format solve_knapsack expects
    data = {
        "weights": [1, 2, 3],
        "values": [10, 5, 15],
        "num_items": 3,
        "all_items": range(3),
        "bin_capacities": [5],
        "num_bins": 1,
        "all_bins": range(1),
    }

    result = solve_knapsack(data)

    # Check result type
    assert isinstance(result, list)
    assert len(result) == data["num_items"]

    # Optional: check assignments don't exceed bin capacity
    for i, bin_index in enumerate(result):
        if bin_index != 0:
            assert data["weights"][i] <= data["bin_capacities"][bin_index]
