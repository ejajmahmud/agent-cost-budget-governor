"""Tests for Cost Governor."""
import unittest
from agent_cost_budget_governor.core import CostBudgetGovernor, BudgetStatus

class TestCostBudgetGovernor(unittest.TestCase):
    def test_budget_transitions(self):
        g = CostBudgetGovernor(default_budget_usd=10.0)
        s1 = g.record_cost("t1", 5.0)
        self.assertEqual(s1, BudgetStatus.HEALTHY)
        self.assertEqual(g.get_recommended_model("t1"), "frontier_pro")

        s2 = g.record_cost("t1", 3.5) # spent 8.5 (85%)
        self.assertEqual(s2, BudgetStatus.THROTTLED)
        self.assertEqual(g.get_recommended_model("t1"), "flash_lite")
