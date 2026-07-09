import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from workflow.activity.sample_activity import HelloActivity, SampleInput
from workflow.sample_workflow import SampleWorkflow


async def test_sample_workflow(workflow_env: WorkflowEnvironment):
    activity_instance = HelloActivity()
    async with Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[SampleWorkflow],
        activities=[activity_instance.say_hello],
    ):
        result = await workflow_env.client.execute_workflow(
            SampleWorkflow.run,
            SampleInput(name="World"),
            id="test-sample-workflow",
            task_queue="test-queue",
        )
    assert result == "Hello, World!"
