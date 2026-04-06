import 'package:flutter/material.dart';

class ChatInput extends StatefulWidget {
  const ChatInput({
    super.key,
    required this.onSend,
    required this.enabled,
    required this.onMicTap,
  });

  final ValueChanged<String> onSend;
  final bool enabled;
  final VoidCallback onMicTap;

  @override
  State<ChatInput> createState() => _ChatInputState();
}

class _ChatInputState extends State<ChatInput> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _submit() {
    if (!widget.enabled) return;
    final text = _controller.text.trim();
    if (text.isEmpty) return;
    widget.onSend(text);
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: TextField(
            controller: _controller,
            enabled: widget.enabled,
            decoration: const InputDecoration(
              hintText: 'Message Jarvis',
              border: OutlineInputBorder(),
            ),
            onSubmitted: (_) => _submit(),
          ),
        ),
        IconButton(
          onPressed: widget.enabled ? widget.onMicTap : null,
          icon: const Icon(Icons.mic_none),
        ),
        IconButton(
          onPressed: widget.enabled ? _submit : null,
          icon: const Icon(Icons.send),
        ),
      ],
    );
  }
}
