def control_home_device(device_name: str, action: str, value: str | None = None) -> str:
    value_suffix = f" with value '{value}'" if value else ""
    return f"Home control stub: {action} '{device_name}'{value_suffix}."
