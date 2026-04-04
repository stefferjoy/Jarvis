import 'package:flutter/material.dart';

import '../models/chat_message.dart';
import '../services/api_client.dart';
import '../services/chat_history_store.dart';
import '../widgets/chat_input.dart';
import '../widgets/quick_actions.dart';
import 'settings_screen.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _messages = <ChatMessage>[];
  final _client = ApiClient();
  final _historyStore = ChatHistoryStore();
  bool _loading = false;
  String? _errorText;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final history = await _historyStore.load();
    if (!mounted) return;
    setState(() {
      _messages
        ..clear()
        ..addAll(history);
    });
  }

  Future<void> _persistHistory() async {
    await _historyStore.save(_messages);
  }

  Future<void> _send(String text) async {
    setState(() {
      _errorText = null;
      _messages.add(ChatMessage(text: text, isUser: true));
      _loading = true;
    });
    await _persistHistory();

    try {
      final reply = await _client.sendChat(text);
      setState(() {
        _messages.add(ChatMessage(text: reply, isUser: false));
      });
    } catch (e) {
      setState(() {
        _errorText = e.toString();
        _messages.add(ChatMessage(text: 'I hit an error talking to backend.', isUser: false));
      });
    } finally {
      setState(() {
        _loading = false;
      });
      await _persistHistory();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Jarvis'),
        actions: [
          IconButton(
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => const SettingsScreen()),
            ),
            icon: const Icon(Icons.settings),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(12, 12, 12, 4),
            child: QuickActions(onTap: _send),
          ),
          if (_errorText != null)
            Container(
              width: double.infinity,
              margin: const EdgeInsets.fromLTRB(12, 4, 12, 8),
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.red.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.red.shade200),
              ),
              child: Text(
                _errorText!,
                style: TextStyle(color: Colors.red.shade900),
              ),
            ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                return Align(
                  alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: message.isUser ? Colors.blue.shade100 : Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(message.text),
                  ),
                );
              },
            ),
          ),
          if (_loading)
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 12),
              child: LinearProgressIndicator(),
            ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: ChatInput(onSend: _send, enabled: !_loading),
          ),
        ],
      ),
    );
  }
}
