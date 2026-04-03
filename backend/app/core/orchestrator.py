from app.adapters.camera import show_camera
from app.adapters.home import control_home_device
from app.adapters.shortcuts import run_shortcut
from app.config import DEVICES_FILE, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, MEMORY_FILE
from app.devices.registry import DeviceRegistry
from app.devices.understanding import DeviceUnderstanding
from app.llm.client import LLMClient
from app.memory.store import MemoryStore


class JarvisOrchestrator:
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.memory = MemoryStore(MEMORY_FILE)
        self.devices = DeviceRegistry(DEVICES_FILE)
        self.device_understanding = DeviceUnderstanding(self.devices)
        self.llm_client = llm_client or LLMClient(
            api_key=LLM_API_KEY,
            model=LLM_MODEL,
            base_url=LLM_BASE_URL,
        )

    def handle_message(self, message: str) -> str:
        message = message.strip()
        normalized = message.lower()
        self.memory.append_recent_message(message)

        if normalized.startswith("remember "):
            fact = message[9:].strip()
            if not fact:
                return "Tell me what to remember."
            self.memory.remember_fact(fact)
            return f"Got it — I will remember: {fact}"

        if "what do you remember" in normalized or "recall memory" in normalized:
            facts = self.memory.list_facts()
            if not facts:
                return "I don't have any saved facts yet."
            return "I remember: " + "; ".join(facts)

        if normalized.startswith("run shortcut ") or normalized.startswith("run automation "):
            return self._handle_shortcut(message)

        if (any(phrase in normalized for phrase in ["show", "open"])) and (
            "cam" in normalized or "camera" in normalized
        ):
            return self._handle_camera(message)

        if any(token in normalized for token in ["turn on", "switch on", "turn off", "switch off"]):
            return self._handle_home_control(message)

        llm_reply = self.llm_client.generate_reply(message)
        if llm_reply:
            return llm_reply

        if not self.llm_client.enabled:
            return (
                "Jarvis fallback: LLM is not configured. "
                "Set JARVIS_LLM_API_KEY to enable conversational replies."
            )

        return "Jarvis fallback: LLM is currently unavailable. Please try again shortly."

    def _handle_shortcut(self, message: str) -> str:
        normalized = message.lower()
        prefix = "run shortcut " if normalized.startswith("run shortcut ") else "run automation "
        shortcut_name = message[len(prefix):].strip()
        if not shortcut_name:
            return "Please tell me which shortcut to run."
        return run_shortcut(shortcut_name)

    def _handle_home_control(self, message: str) -> str:
        normalized = message.lower()
        action = "turn_on" if ("turn on" in normalized or "switch on" in normalized) else "turn_off"
        match_result = self.device_understanding.resolve(message, device_type="light")

        if match_result.status == "none":
            return "I couldn't find a matching light device."

        if match_result.status == "ambiguous":
            choices = ", ".join(device["canonical_name"] for device in match_result.matches)
            return f"I found multiple matching devices: {choices}. Which one do you mean?"

        target = match_result.matches[0]["canonical_name"]
        return control_home_device(target, action)

    def _handle_camera(self, message: str) -> str:
        match_result = self.device_understanding.resolve(message, device_type="camera")

        if match_result.status == "none":
            return "I couldn't find a matching camera."

        if match_result.status == "ambiguous":
            choices = ", ".join(device["canonical_name"] for device in match_result.matches)
            return f"I found multiple cameras: {choices}. Which camera should I show?"

        return show_camera(match_result.matches[0]["canonical_name"])
