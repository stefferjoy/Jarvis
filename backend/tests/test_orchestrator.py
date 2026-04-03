import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from app.core.orchestrator import JarvisOrchestrator


class FakeLLMClient:
    def __init__(self, enabled: bool, response: str | None = None) -> None:
        self.enabled = enabled
        self.response = response
        self.calls = 0

    def generate_reply(self, user_message: str) -> str | None:
        self.calls += 1
        return self.response


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)

        memory_file = base / "memory.json"
        devices_file = base / "devices.json"

        from app.core import orchestrator as orchestrator_module

        orchestrator_module.MEMORY_FILE = memory_file
        orchestrator_module.DEVICES_FILE = devices_file

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_normal_reply_uses_llm_when_available(self) -> None:
        llm = FakeLLMClient(enabled=True, response="Hello from model")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        result = orchestrator.handle_message("hello jarvis")
        self.assertEqual("Hello from model", result)
        self.assertEqual(1, llm.calls)

    def test_model_unavailable_fallback(self) -> None:
        llm = FakeLLMClient(enabled=True, response=None)
        orchestrator = JarvisOrchestrator(llm_client=llm)

        result = orchestrator.handle_message("hello jarvis")
        self.assertIn("LLM is currently unavailable", result)
        self.assertEqual(1, llm.calls)

    def test_missing_api_key_fallback(self) -> None:
        llm = FakeLLMClient(enabled=False, response=None)
        orchestrator = JarvisOrchestrator(llm_client=llm)

        result = orchestrator.handle_message("hello jarvis")
        self.assertIn("LLM is not configured", result)
        self.assertEqual(1, llm.calls)

    def test_deterministic_commands_bypass_llm(self) -> None:
        llm = FakeLLMClient(enabled=True, response="model should not be used")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        home = orchestrator.handle_message("switch on my room light")
        camera = orchestrator.handle_message("show front door camera")
        shortcut = orchestrator.handle_message("run shortcut morning routine")
        ambiguous = orchestrator.handle_message("turn on light")

        self.assertIn("bedroom light", home)
        self.assertIn("Camera stub", camera)
        self.assertIn("Shortcut handoff", shortcut)
        self.assertIn("multiple matching devices", ambiguous)
        self.assertEqual(0, llm.calls)

    def test_expanded_light_phrases(self) -> None:
        llm = FakeLLMClient(enabled=True, response="model should not be used")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        result_on = orchestrator.handle_message("please switch on the bedside lamp")
        result_off = orchestrator.handle_message("turn off bedroom lights")

        self.assertIn("bed lamp", result_on)
        self.assertIn("bedroom light", result_off)
        self.assertEqual(0, llm.calls)

    def test_expanded_camera_phrases(self) -> None:
        llm = FakeLLMClient(enabled=True, response="model should not be used")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        result = orchestrator.handle_message("can you view the front door feed")

        self.assertIn("front door cam", result)
        self.assertEqual(0, llm.calls)

    def test_expanded_shortcut_phrases(self) -> None:
        llm = FakeLLMClient(enabled=True, response="model should not be used")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        result = orchestrator.handle_message("start bedtime automation")

        self.assertIn("Shortcut handoff", result)
        self.assertEqual(0, llm.calls)

    def test_clarification_response_includes_room_and_type(self) -> None:
        llm = FakeLLMClient(enabled=True, response="model should not be used")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        result = orchestrator.handle_message("lights on")

        self.assertIn("bedroom light (bedroom light)", result)
        self.assertIn("bed lamp (bedroom light)", result)
        self.assertEqual(0, llm.calls)

    def test_memory_behavior_still_working(self) -> None:
        llm = FakeLLMClient(enabled=True, response="model")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        write_result = orchestrator.handle_message("remember coffee at 8am")
        read_result = orchestrator.handle_message("what do you remember")

        self.assertIn("I will remember", write_result)
        self.assertIn("coffee at 8am", read_result)
        self.assertEqual(0, llm.calls)

    def test_orchestrator_home_control_remains_deterministic(self) -> None:
        llm = FakeLLMClient(enabled=True, response="model should not be used")
        orchestrator = JarvisOrchestrator(llm_client=llm)

        with patch("app.core.orchestrator.control_home_device", return_value="home bridge ok") as mock_home:
            result = orchestrator.handle_message("switch on my room light")

        self.assertEqual("home bridge ok", result)
        self.assertEqual(1, mock_home.call_count)
        self.assertEqual(0, llm.calls)


if __name__ == "__main__":
    unittest.main()
