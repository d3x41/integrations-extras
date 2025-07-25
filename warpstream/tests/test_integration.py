import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.warpstream import WarpstreamCheck


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = WarpstreamCheck('warpstream', {}, [instance])

    # the check should send OK
    c.check(instance)
