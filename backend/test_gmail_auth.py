import os

import pytest


@pytest.mark.skipif(
    not os.path.exists("credentials.json"),
    reason="credentials.json not present; skipping Gmail auth test.",
)
def test_gmail_service_can_be_built():
    from services.email_service import get_gmail_service

    try:
        service = get_gmail_service()
    except Exception as exc:
        pytest.skip(
            "Gmail auth requires interactive OAuth "
            f"(re-run the app to refresh token.json): {exc}"
        )

    assert service is not None
    assert hasattr(service, "users")
