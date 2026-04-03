from google import genai


class GeminiClient:
    def __init__(self, api_key: str | None, model: str = "gemini-2.5-flash") -> None:
        self.api_key = api_key
        self.model = model
        self.enabled = bool(api_key)

    def generate_reply(self, user_message: str) -> str | None:
        if not self.enabled:
            return None

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=user_message,
            )
            text = getattr(response, "text", None)
            if text:
                return text.strip()
            return None
        except Exception:
            return None