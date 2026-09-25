from .base import ApplicationAdapter, PreparedApplication


class LeverAdapter(ApplicationAdapter):
    platform_name = "lever"

    def matches(self, job_url: str) -> bool:
        return "lever.co" in (job_url or "").lower()

    def prepare_application(
        self,
        job_url: str,
        profile: dict,
    ) -> PreparedApplication:
        fields = {}
        missing = []
        notes = []

        field_map = [
            ("name", "name"),
            ("email", "email"),
            ("phone", "phone"),
            ("linkedin_url", "linkedin_url"),
            ("resume_text", "resume_text"),
        ]

        for target_field, profile_key in field_map:
            value = (profile or {}).get(profile_key)

            if value and not (
                target_field == "name" and value == "Unknown"
            ):
                fields[target_field] = value
            else:
                missing.append(profile_key)

        notes.append(
            "Lever's 'Additional Information' box is usually where a "
            "short pitch or cover letter goes - none is generated "
            "here automatically, so write one before submitting."
        )

        return PreparedApplication(
            platform=self.platform_name,
            job_url=job_url,
            fields=fields,
            missing_fields=missing,
            notes=notes,
        )
