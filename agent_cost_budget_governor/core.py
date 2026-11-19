"""Core Cost Budget Governor."""
from typing import Dict, Optional
import enum

class BudgetStatus(enum.Enum):
    HEALTHY = "healthy"
    THROTTLED = "throttled"
    EXHAUSTED = "exhausted"

class BudgetQuota:
    def __init__(self, max_budget_usd: float):
        self.max_budget_usd = max_budget_usd
        self.spent_usd = 0.0

    @property
    def remaining(self) -> float:
        return max(0.0, self.max_budget_usd - self.spent_usd)

class CostBudgetGovernor:
    def __init__(self, default_budget_usd: float = 10.0):
        self.quotas: Dict[str, BudgetQuota] = {}
        self.default_budget_usd = default_budget_usd

    def get_or_create_quota(self, tenant_id: str) -> BudgetQuota:
        if tenant_id not in self.quotas:
            self.quotas[tenant_id] = BudgetQuota(self.default_budget_usd)
        return self.quotas[tenant_id]

    def record_cost(self, tenant_id: str, cost_usd: float) -> BudgetStatus:
        quota = self.get_or_create_quota(tenant_id)
        quota.spent_usd += cost_usd
        if quota.spent_usd >= quota.max_budget_usd:
            return BudgetStatus.EXHAUSTED
        elif quota.spent_usd >= quota.max_budget_usd * 0.8:
            return BudgetStatus.THROTTLED
        return BudgetStatus.HEALTHY

    def get_recommended_model(self, tenant_id: str) -> str:
        quota = self.get_or_create_quota(tenant_id)
        if quota.spent_usd >= quota.max_budget_usd:
            return "none"
        elif quota.spent_usd >= quota.max_budget_usd * 0.8:
            return "flash_lite"
        return "frontier_pro"
