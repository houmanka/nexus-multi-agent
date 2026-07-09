import pytest
from temporalio.testing import ActivityEnvironment

from workflow.activity.sample_activity import HelloActivity, SampleInput


@pytest.fixture
def activity_env():
    return ActivityEnvironment()


async def test_say_hello(activity_env: ActivityEnvironment):
    activity = HelloActivity()
    result = await activity_env.run(activity.say_hello, SampleInput(name="World"))
    assert result == "Hello, World!"
