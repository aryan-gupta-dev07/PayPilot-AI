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

    expected_top = case.get("expected_top_product")

    top_product_passed = (
        actual_names[0] == expected_top
        if expected_top is not None and actual_names
        else expected_top is None
    )

    return {
        "case_id": case["case_id"],
        "expected": expected_names,
        "actual": actual_names,
        "passed": passed,
        "expected_top": expected_top,
        "top_product_passed": top_product_passed,
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

        if result["expected_top"] is not None:
            print(
                f"Expected top product: "
                f"{result['expected_top']}"
            )
            status = (
                "PASS"
                if result["top_product_passed"]
                else "FAIL"
            )
            print(f"Top product check: {status}")

    total = len(results)
    passed_count = sum(
        1 for result in results
        if result["passed"]
    )

    ranking_results = [
        result
        for result in results
        if result["expected_top"] is not None
    ]

    ranking_passed = sum(
        1
        for result in ranking_results
        if result["top_product_passed"]
    )

    ranking_accuracy = (
        ranking_passed / len(ranking_results) * 100
        if ranking_results
        else 0
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
    print(f"Top product accuracy: {ranking_accuracy:.2f}%")

    print(f"Ranking cases: {len(ranking_results)}")
    print(f"Ranking passed: {ranking_passed}")
    print(f"Ranking accuracy: {ranking_accuracy:.2f}%")

    report = {
        "total_cases": total,
        "passed": passed_count,
        "failed": total - passed_count,
        "exact_match_rate": round(accuracy, 2),
        "ranking_cases": len(ranking_results),
        "ranking_passed": ranking_passed,
        "ranking_accuracy": round(ranking_accuracy, 2),
    }

    import json

    with open("evaluation_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("Report saved to evaluation_report.json")


if __name__ == "__main__":
    run_evaluation()
