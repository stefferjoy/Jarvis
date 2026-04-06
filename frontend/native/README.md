# Native Assistant Integration Scaffold

This folder contains production-minded scaffolding notes/files for native action integration.

## Unified native -> Flutter action channel

- Method channel: `jarvis/actions`
- Method name: `invokeAction`
- Payload schema:

```json
{ "actionId": "runMorningRoutine" }
```

Supported `actionId` values map to `AssistantActionId` in Flutter:
- `runMorningRoutine`
- `runBedtimeRoutine`
- `turnOnBedroomLight`
- `showFrontDoorCamera`
- `openJarvisChat`

Flutter receiver implementation is in:
- `frontend/lib/services/native_action_bridge.dart`
- `frontend/lib/actions/assistant_action.dart`

## Voice scaffolding channel

- Method channel: `jarvis/voice`
- Suggested methods:
  - `startListening` -> returns recognized command text
  - `speak` with payload `{ "text": "..." }`

Flutter voice scaffold implementation:
- `frontend/lib/services/voice_assistant_service.dart`

## iOS scaffold
- See `ios/AppIntentsBridge.swift` for placeholder App Intents/App Shortcuts wiring points.

## Android scaffold
- See `android/AppActionsBridge.kt` and `android/shortcuts.xml` for placeholder App Shortcuts/App Actions wiring points.
