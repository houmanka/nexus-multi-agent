import nexusrpc.handler
from temporalio import nexus

from qualification_service.const import QUALIFICATION_TASK_QUEUE
from qualification_service.workflow import QualificationServiceWorkflow
from shared.service import QualificationService, QualificationInput, QualificationResult


@nexusrpc.handler.service_handler(service=QualificationService)
class QualificationServiceHandler:
    @nexus.workflow_run_operation
    async def qualify(
            self, ctx: nexus.WorkflowRunOperationContext, input: QualificationInput
) -> nexus.WorkflowHandle[QualificationResult]:
        return await ctx.start_workflow(
            QualificationServiceWorkflow.run,
            input,
            id=f"qualification-{input.application_id}",
            task_queue=QUALIFICATION_TASK_QUEUE
        )