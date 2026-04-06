import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

import '../actions/assistant_action.dart';

class NativeActionBridge {
  static const MethodChannel _channel = MethodChannel('jarvis/actions');

  Future<void> startListening(ValueChanged<AssistantActionId> onAction) async {
    _channel.setMethodCallHandler((call) async {
      if (call.method != 'invokeAction') {
        return null;
      }

      final args = call.arguments;
      if (args is! Map) {
        return null;
      }

      final rawActionId = args['actionId']?.toString();
      if (rawActionId == null) {
        return null;
      }

      final action = AssistantActionCatalog.byRawId(rawActionId);
      if (action != null) {
        onAction(action.id);
      }
      return null;
    });
  }
}
