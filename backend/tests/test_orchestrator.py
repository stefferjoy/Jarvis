import tempfile
from pathlib import Path
import unittest

from app.core.orchestrator import JarvisOrchestrator


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)

        memory_file = base / "memory.json"
        devices_file = base / "devices.json"

        from app.core import orchestrator as orchestrator_module

        orchestrator_module.MEMORY_FILE = memory_file
        orchestrator_module.DEVICES_FILE = devices_file
        self.orchestrator = JarvisOrchestrator()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_normal_reply(self) -> None:
        result = self.orchestrator.handle_message("hello jarvis")
        self.assertIn("Jarvis MVP reply", result)

    def test_memory_store_and_recall(self) -> None:
        self.orchestrator.handle_message("remember coffee at 8am")
        result = self.orchestrator.handle_message("what do you remember")
        self.assertIn("coffee at 8am", result)

    def test_alias_resolution(self) -> None:
        result = self.orchestrator.handle_message("switch on my room light")
        self.assertIn("bedroom light", result)

    def test_room_resolution_and_disambiguation(self) -> None:
        result = self.orchestrator.handle_message("turn on bedroom light")
        self.assertIn("bedroom light", result)

        ambiguous = self.orchestrator.handle_message("turn on light")
        self.assertIn("multiple matching devices", ambiguous)

    def test_camera_tool_execution(self) -> None:
        result = self.orchestrator.handle_message("show front door camera")
        self.assertIn("Camera stub", result)

    def test_shortcut_tool_execution(self) -> None:
        result = self.orchestrator.handle_message("run shortcut morning routine")
        self.assertIn("Shortcut 'morning routine'", result)


if __name__ == "__main__":
    unittest.main()
