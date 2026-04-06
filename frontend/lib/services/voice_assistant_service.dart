import 'package:flutter/services.dart';

class VoiceAssistantService {
  static const MethodChannel _channel = MethodChannel('jarvis/voice');

  Future<String?> captureVoiceCommand() async {
    try {
      final result = await _channel.invokeMethod<String>('startListening');
      if (result == null || result.trim().isEmpty) {
        return null;
      }
      return result.trim();
    } catch (_) {
      return null;
    }
  }

  Future<void> speak(String text) async {
    try {
      await _channel.invokeMethod<void>('speak', {'text': text});
    } catch (_) {
      // Scaffolding only: no-op when not configured.
    }
  }
}
