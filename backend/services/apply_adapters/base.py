from abc import ABC, abstractmethod


class PreparedApplication:
    """
    A filled-out but NOT submitted application.

    Nothing in this class sends a network request to the job
    platform. It only maps the candidate profile onto that
    platform's known fields, so a human (or a later, explicitly
    triggered submission step) can review exactly what would be
    sent before anything actually goes out.
    """

    def __init__(
        self,
        platform,
        job_url,
        fields,
        missing_fields=None,
        notes=None,
    ):
        self.platform = platform
        self.job_url = job_url
        self.fields = fields
        self.missing_fields = missing_fields or []
        self.notes = notes or []

    @property
    def ready_to_submit(self):
        # Anything missing means a human needs to fill a gap
        # before this could honestly be submitted.
        return len(self.missing_fields) == 0

    def to_dict(self):
        return {
            "platform": self.platform,
            "job_url": self.job_url,
            "fields": self.fields,
            "missing_fields": self.missing_fields,
            "notes": self.notes,
            "ready_to_submit": self.ready_to_submit,
        }


class ApplicationAdapter(ABC):
    platform_name = "unknown"

    @abstractmethod
    def matches(self, job_url: str) -> bool:
        """Return True if this adapter handles the given job URL."""
        ...

    @abstractmethod
    def prepare_application(
        self,
        job_url: str,
        profile: dict,
    ) -> PreparedApplication:
        """
        Map the candidate profile onto this platform's typical
        application fields. Must not perform any network request
        to the job platform itself - preparation only.
        """
        ...
