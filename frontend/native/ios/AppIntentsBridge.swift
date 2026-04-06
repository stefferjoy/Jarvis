// Placeholder scaffold for iOS App Intents / App Shortcuts integration.
// Manual Apple-side setup is still required in a full Flutter iOS project.
//
// Intended flow:
// 1) Siri/App Shortcut invokes an app intent.
// 2) Intent passes `actionId` to Flutter via method channel `jarvis/actions`.
// 3) Flutter handles the action via NativeActionBridge + ActionDispatcher.
//
// Suggested payload:
// { "actionId": "runMorningRoutine" }
