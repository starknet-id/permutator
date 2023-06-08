import random
import copy
import itertools
import json
import time
from typing import Dict, List, Iterator

# Problem parameters
traits = ["head", "fur", "makeup", "makeup_c", "body", "ears", "back"]
trait_amounts = {
    "head": 9,
    "fur": 18,
    "makeup": 6,
    "makeup_c": 7,
    "body": 8,
    "ears": 13,
    "back": 9,
}
trait_score = {
    "head": 4,
    "fur": 8,
    "makeup": 2,
    "makeup_c": 1,
    "body": 2,
    "ears": 1,
    "back": 3,
}


def get_trait_iter(trait: str) -> Iterator[int]:
    """Generates an iterator for a given trait."""
    for i in range(trait_amounts[trait]):
        yield i


def create_random_iter(array, num_items: int) -> Iterator:
    """Creates a random iterator for a given array and number of items."""
    random.shuffle(array)
    selected = set()
    count = 0

    while count < num_items:
        for item in array:
            if item not in selected:
                yield item
                selected.add(item)
                count += 1
                if count == num_items:
                    return


def generate_smart_combinations(num_combinations: int) -> List[Dict[str, int]]:
    """Generates initial combinations for the traits."""
    sorted_traits = sorted(trait_score, key=lambda x: trait_score[x], reverse=True)

    combinations = []
    acc = 1
    stop = 0
    for i, trait in enumerate(sorted_traits):
        stop = i
        if acc > num_combinations:
            break
        acc *= trait_amounts[trait]

    for basis in create_random_iter(
        list(itertools.product(*map(get_trait_iter, sorted_traits[:stop]))),
        num_combinations,
    ):
        combination = {trait: basis[i] for i, trait in enumerate(sorted_traits[:stop])}
        for trait in sorted_traits[stop:]:
            combination[trait] = random.randrange(trait_amounts[trait])
        combinations.append(combination)

    return combinations


def generate_random_combinations(num_combinations: int) -> List[Dict[str, int]]:
    """Generates initial combinations for the traits."""
    return [
        {trait: random.randrange(trait_amounts[trait]) for trait in traits}
        for _ in range(num_combinations)
    ]


def difference_score(combination1: Dict[str, int], combination2: Dict[str, int]) -> int:
    """Calculates the difference score between two combinations."""
    return sum(
        trait_score[trait]
        for trait in combination1
        if combination1[trait] != combination2[trait]
    )


def calculate_min_difference_score(combinations: List[Dict[str, int]]) -> int:
    """Calculates the minimum difference score among the combinations."""
    smallest_diff = 2**64 - 1
    for i, combi in enumerate(combinations):
        for j, combj in enumerate(combinations):
            if i != j:
                smallest_diff = min(difference_score(combi, combj), smallest_diff)
    return smallest_diff


def generate_neighbour(combination: Dict[str, int]) -> Dict[str, int]:
    """Generates a neighboring combination by changing one trait."""
    new_combination = copy.deepcopy(combination)
    trait_to_change = random.choice(traits)
    new_combination[trait_to_change] = (
        new_combination[trait_to_change] + 1
    ) % trait_amounts[trait_to_change]
    return new_combination


def optimize_combinations(
    initial_combinations: List[Dict[str, int]],
    iterations: int,
) -> List[Dict[str, int]]:
    """Optimizes the combinations through a specified number of iterations."""
    combinations = copy.deepcopy(initial_combinations)
    for _ in range(iterations):
        for i, combination in enumerate(combinations):
            new_combination = generate_neighbour(combination)
            potential_new_score = min(
                difference_score(new_combination, combj)
                for j, combj in enumerate(combinations)
                if i != j
            )
            current_score = min(
                difference_score(combination, combj)
                for j, combj in enumerate(combinations)
                if i != j
            )
            if potential_new_score > current_score:
                combinations[i] = new_combination

    return combinations


def print_elapsed_time(start_time: float, message: str):
    """Prints a message along with the elapsed time since the start time."""
    elapsed_time = time.time() - start_time
    print(f"{message}, {elapsed_time:.2f}s")


def save_combinations(combinations: List[Dict[str, int]], filename: str):
    """Saves combinations to a file in JSON format."""
    output = json.dumps(combinations)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output)


def execute_algorithm(
    generation_algo,
    num_combinations: int,
    iterations: int,
    algorithm_name: str,
    opti: bool,
):
    """Executes the specified algorithm and outputs the results."""
    print(algorithm_name)

    start = time.time()
    initial_combinations = generation_algo(num_combinations)
    print_elapsed_time(start, "Found initial combinations")

    start = time.time()
    score = calculate_min_difference_score(initial_combinations)
    print_elapsed_time(start, f"Min difference score: {score}")

    if opti:
        start = time.time()
        best_combinations = optimize_combinations(initial_combinations, iterations)
        print_elapsed_time(start, "Optimized combinations")

        save_combinations(best_combinations, "combinations.json")

        start = time.time()
        score = calculate_min_difference_score(best_combinations)
        print_elapsed_time(start, f"Min difference score: {score}")


def main():
    """Main function to run the algorithms and print their results."""
    num_combinations = 1000
    iterations = 10
    execute_algorithm(
        generate_smart_combinations,
        num_combinations,
        iterations,
        "OPTIMIZED ALGORITHM",
        True,
    )
    print()
    execute_algorithm(
        generate_random_combinations,
        num_combinations,
        iterations,
        "RANDOMIZED ALGORITHM (for comparison)",
        False,
    )


if __name__ == "__main__":
    main()
