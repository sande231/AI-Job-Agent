from .base import ApplicationAdapter, PreparedApplication


class GreenhouseAdapter(ApplicationAdapter):
    platform_name = "greenhouse"

    def matches(self, job_url: str) -> bool:
        return "greenhouse.io" in (job_url or "").lower()

    def prepare_application(
        self,
        job_url: str,
        profile: dict,
    ) -> PreparedApplication:
        fields = {}
        missing = []
        notes = []

        full_name = (profile or {}).get("name")

        if full_name and full_name != "Unknown":
            parts = full_name.strip().split(" ", 1)
            fields["first_name"] = parts[0]
            fields["last_name"] = parts[1] if len(parts) > 1 else ""
        else:
            missing.append("name")

        field_map = [
            ("email", "email"),
            ("phone", "phone"),
            ("linkedin_url", "linkedin_url"),
            ("resume_text", "resume_text"),
        ]

        for target_field, profile_key in field_map:
            value = (profile or {}).get(profile_key)

            if value:
                fields[target_field] = value
            else:
                missing.append(profile_key)

        notes.append(
            "Greenhouse postings often add custom screening questions "
            "(work authorization, sponsorship, years of experience) "
            "that are unique per job and can't be pre-filled reliably "
            "- these need a manual check before submitting."
        )

        return PreparedApplication(
            platform=self.platform_name,
            job_url=job_url,
            fields=fields,
            missing_fields=missing,
            notes=notes,
        )
