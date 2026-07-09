from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from workflow.activity.sample_activity import HelloActivity, SampleInput


@workflow.defn
class SampleWorkflow:
    @workflow.run
    async def run(self, args: SampleInput) -> str:
        return await workflow.execute_activity(
            HelloActivity.say_hello,
            args,
            start_to_close_timeout=timedelta(seconds=10),
        )
