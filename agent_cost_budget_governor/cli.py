"""CLI for Cost Governor."""
import argparse
from .core import CostBudgetGovernor

def main():
    parser = argparse.ArgumentParser(description="Agent Cost Budget Governor CLI")
    parser.add_argument("--demo", action="store_true", help="Run governor demo")
    args = parser.parse_args()

    gov = CostBudgetGovernor(default_budget_usd=1.0)
    gov.record_cost("session-1", 0.5)
    print(f"Model recommended at 50%: {gov.get_recommended_model('session-1')}")
    gov.record_cost("session-1", 0.4)
    print(f"Model recommended at 90%: {gov.get_recommended_model('session-1')}")

if __name__ == "__main__":
    main()
