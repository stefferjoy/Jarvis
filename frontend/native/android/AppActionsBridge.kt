// Placeholder scaffold for Android App Actions / App Shortcuts integration.
// Manual Android project wiring is still required in a full Flutter Android project.
//
// Intended flow:
// 1) Launcher shortcut or Assistant action resolves to actionId.
// 2) Native Android side invokes Flutter method channel `jarvis/actions`.
// 3) Flutter handles action via NativeActionBridge + ActionDispatcher.
