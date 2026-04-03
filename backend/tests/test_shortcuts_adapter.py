import io
import unittest
from unittest.mock import patch

from app.adapters.shortcuts import run_shortcut


class _FakeResponse:
    def __init__(self, status: int = 200) -> None:
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return io.BytesIO(b"{}").read()


class ShortcutsAdapterTests(unittest.TestCase):
    def test_configured_path_sends_handoff(self) -> None:
        with patch("app.adapters.shortcuts.request.urlopen", return_value=_FakeResponse(status=202)) as mock_urlopen:
            result = run_shortcut(
                "morning routine",
                params={"scene": "kitchen"},
                bridge_url="https://example.com/shortcut-bridge",
                bridge_token="secret",
                timeout_seconds=2,
            )

        self.assertIn("Shortcut handoff sent", result)
        self.assertEqual(1, mock_urlopen.call_count)

    def test_missing_configuration_fallback(self) -> None:
        with patch("app.adapters.shortcuts.SHORTCUTS_BRIDGE_URL", None):
            result = run_shortcut("morning routine", bridge_url=None)
        self.assertIn("Shortcut handoff unavailable", result)


if __name__ == "__main__":
    unittest.main()
