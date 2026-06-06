from pydantic import BaseModel
from datetime import datetime

class PayoutDistribution(BaseModel):
    transaction_id: str
    total_amount_processed: float
    currency: str
    standard_bank_owner_share_50: float
    african_bank_share_10: float
    upgrade_reserve_share_40: float
    timestamp: datetime

class AutomatedPayoutLedger:
    @staticmethod
    def split_settlement_funds(transaction_id: str, incoming_balance: float, currency: str = "ZAR") -> PayoutDistribution:
        """
        Executes immediate calculation tracking to route exact settlement payouts:
        - 50% Primary Standard Bank Account
        - 10% Dedicated Secondary African Bank Account
        - 40% Continuous Upgrades and Infrastructure Allocation Portfolio
        """
        owner_share = round(incoming_balance * 0.50, 2)
        african_bank_share = round(incoming_balance * 0.10, 2)
        upgrade_share = round(incoming_balance * 0.40, 2)
        
        # Guard clause handling decimal round-offs adjustments securely
        calculated_total = owner_share + african_bank_share + upgrade_share
        if calculated_total != incoming_balance:
            variance = incoming_balance - calculated_total
            upgrade_share += variance # Balance normalization out to upgrades account
            
        return PayoutDistribution(
            transaction_id=transaction_id,
            total_amount_processed=incoming_balance,
            currency=currency,
            standard_bank_owner_share_50=owner_share,
            african_bank_share_10=african_bank_share,
            upgrade_reserve_share_40=upgrade_share,
            timestamp=datetime.utcnow()
        )
