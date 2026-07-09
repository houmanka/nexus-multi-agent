from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from shared.service import QualificationInput, QualificationResult
    from qualification_service.activity import calculate_ltv, LTVInput


@workflow.defn
class QualificationServiceWorkflow:
    @workflow.run
    async def run(self, args: QualificationInput) -> QualificationResult:
        result = await workflow.execute_activity(
            calculate_ltv,
            LTVInput(
                loan_amount=args.loan_amount,
                property_value=args.property_value
            ),
            start_to_close_timeout=timedelta(seconds=10),
        )
        if result > 80:
            return QualificationResult(
                is_qualified=False,
                reason=f"LTV is {result}%, should be less than 80%"
            )
        return QualificationResult(
            is_qualified=True,
            reason=f"LTV is {result}%"
        )
