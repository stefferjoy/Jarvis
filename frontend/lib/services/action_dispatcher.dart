import '../actions/assistant_action.dart';

class ActionDispatchResult {
  final bool success;
  final String? userMessage;

  const ActionDispatchResult({required this.success, this.userMessage});
}

class ActionDispatcher {
  const ActionDispatcher();

  ActionDispatchResult dispatch(AssistantAction action) {
    if (action.id == AssistantActionId.openJarvisChat) {
      return const ActionDispatchResult(success: true, userMessage: null);
    }

    // Deterministic path: convert known actions into existing chat commands.
    return ActionDispatchResult(success: true, userMessage: action.chatCommand);
  }

  ActionDispatchResult dispatchById(AssistantActionId actionId) {
    final action = AssistantActionCatalog.byId(actionId);
    if (action == null) {
      return const ActionDispatchResult(success: false, userMessage: null);
    }
    return dispatch(action);
  }
}
