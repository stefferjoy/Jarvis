class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final bool failed;

  ChatMessage({
    required this.text,
    required this.isUser,
    DateTime? timestamp,
    this.failed = false,
  }) : timestamp = timestamp ?? DateTime.now();

  Map<String, dynamic> toJson() => {
    'text': text,
    'isUser': isUser,
    'timestamp': timestamp.toIso8601String(),
    'failed': failed,
  };

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      text: (json['text'] as String?) ?? '',
      isUser: (json['isUser'] as bool?) ?? false,
      timestamp: DateTime.tryParse((json['timestamp'] as String?) ?? ''),
      failed: (json['failed'] as bool?) ?? false,
    );
  }
}
