import io
import unittest
from unittest.mock import patch

from app.adapters.home import control_home_device


class _FakeResponse:
    def __init__(self, status: int = 200) -> None:
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return io.BytesIO(b"{}").read()


class HomeAdapterTests(unittest.TestCase):
    def test_configured_path_sends_handoff(self) -> None:
        with patch("app.adapters.home.request.urlopen", return_value=_FakeResponse(status=200)) as mock_urlopen:
            result = control_home_device(
                "bedroom light",
                "turn_on",
                bridge_url="https://example.com/home-bridge",
                bridge_token="secret",
                timeout_seconds=2,
            )

        self.assertIn("Home bridge handoff sent", result)
        self.assertEqual(1, mock_urlopen.call_count)

    def test_missing_configuration_fallback(self) -> None:
        with patch("app.adapters.home.HOME_BRIDGE_URL", None):
            result = control_home_device("bedroom light", "turn_on", bridge_url=None)
        self.assertIn("Home bridge unavailable", result)


if __name__ == "__main__":
    unittest.main()
