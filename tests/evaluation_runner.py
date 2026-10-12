from tests.evaluation_cases import EVALUATION_CASES
from app.tools.products import find_products


def evaluate_case(case):
    """Run one evaluation case and compare actual vs expected products."""

    actual_products = find_products(
        category=case["category"],
        budget=case["budget"],
        requirements=case["requirements"],
        use_case=case["use_case"],
    )

    actual_names = [
        product["name"]
        for product in actual_products
    ]

    expected_names = case["expected_products"]

    passed = set(actual_names) == set(expected_names)

    return {
        "case_id": case["case_id"],
        "expected": expected_names,
        "actual": actual_names,
        "passed": passed,
    }


def run_evaluation():
    """Evaluate all cases and print a summary."""

    results = []

    for case in EVALUATION_CASES:
        result = evaluate_case(case)
        results.append(result)

        status = "PASS" if result["passed"] else "FAIL"

        print(f"\n[{status}] {result['case_id']}")
        print(f"Expected: {result['expected']}")
        print(f"Actual:   {result['actual']}")

    total = len(results)
    passed_count = sum(
        1 for result in results
        if result["passed"]
    )

    accuracy = (
        passed_count / total * 100
        if total
        else 0
    )

    print("\n--- Evaluation Summary ---")
    print(f"Total cases: {total}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total - passed_count}")
    print(f"Exact-match rate: {accuracy:.2f}%")


if __name__ == "__main__":
    run_evaluation()