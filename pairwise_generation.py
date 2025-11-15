from testflows.combinatorics import Covering

#generating pairwise pairs given the parameters
parameters = ({
  "num_knapsacks": [1, 2, 5, 10],
  "capacity_pattern": ["uniform", "varied", "tight", "loose"],
  "num_items": [10, 50, 100, 500],
  "item_weights": ["small", "large", "mixed", "skewed"],
  "item_values": ["low", "high", "mixed", "skewed"],
})

pairwise_tests = (Covering(parameters,strength=2))
print(pairwise_tests)

#checking if the coverage array covers all possible interactions atleast once

print(pairwise_tests.check())


#extended to  higher order interactions

third_order_tests = (Covering(parameters,strength=3))
print(third_order_tests)
