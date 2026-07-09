from dataclasses import dataclass

from temporalio import activity


@dataclass
class LTVInput:
    loan_amount: float
    property_value: float

@activity.defn
async def calculate_ltv(input: LTVInput) -> float:
    return (input.loan_amount / input.property_value) * 100

