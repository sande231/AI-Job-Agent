from .base import ApplicationAdapter, PreparedApplication
from .greenhouse import GreenhouseAdapter
from .lever import LeverAdapter


# Add new adapters here as they're built.
ADAPTERS = [
    GreenhouseAdapter(),
    LeverAdapter(),
]


def get_adapter_for_url(job_url):
    for adapter in ADAPTERS:
        if adapter.matches(job_url):
            return adapter

    return None
