import 'package:flutter/material.dart';

import '../actions/assistant_action.dart';
import '../models/chat_message.dart';
import '../services/action_dispatcher.dart';
import '../services/api_client.dart';
import '../services/chat_history_store.dart';
import '../services/native_action_bridge.dart';
import '../services/voice_assistant_service.dart';
import '../widgets/chat_input.dart';
import '../widgets/quick_actions.dart';
import 'devices_screen.dart';
import 'memory_screen.dart';
import 'routines_screen.dart';
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
  final _dispatcher = const ActionDispatcher();
  final _nativeBridge = NativeActionBridge();
  final _voiceService = VoiceAssistantService();
  final _scrollController = ScrollController();

  bool _loading = false;
  String? _errorText;
  String? _warningText;
  String? _lastFailedUserMessage;

  @override
  void initState() {
    super.initState();
    _loadHistory();
    _nativeBridge.startListening(_handleNativeAction);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _loadHistory() async {
    final history = await _historyStore.load();
    if (!mounted) return;
    setState(() {
      _messages
        ..clear()
        ..addAll(history);
    });
    _autoScroll();
  }

  Future<void> _persistHistory() async {
    await _historyStore.save(_messages);
  }

  void _handleNativeAction(AssistantActionId actionId) {
    final result = _dispatcher.dispatchById(actionId);
    if (!result.success) {
      setState(() {
        _errorText = 'Could not dispatch native action.';
      });
      return;
    }
    if (result.userMessage != null) {
      _send(result.userMessage!);
    }
  }

  Future<void> _runAction(AssistantAction action) async {
    final result = _dispatcher.dispatch(action);
    if (!result.success) {
      setState(() {
        _errorText = 'Could not dispatch action: ${action.title}';
      });
      return;
    }
    if (result.userMessage != null) {
      await _send(result.userMessage!);
    }
  }

  Future<void> _send(String text) async {
    if (_loading) return;

    setState(() {
      _errorText = null;
      _warningText = null;
      _messages.add(ChatMessage(text: text, isUser: true));
      _loading = true;
    });
    await _persistHistory();
    _autoScroll();

    try {
      final reply = await _client.sendChat(text);
      setState(() {
        _messages.add(ChatMessage(text: reply, isUser: false));
        _lastFailedUserMessage = null;
        final lowered = reply.toLowerCase();
        if (lowered.contains('unavailable') || lowered.contains('failed')) {
          _warningText = reply;
        }
      });
      await _voiceService.speak(reply);
    } catch (e) {
      setState(() {
        _errorText = e.toString();
        _lastFailedUserMessage = text;
        _messages.add(
          ChatMessage(
            text: 'I hit an error talking to backend.',
            isUser: false,
            failed: true,
          ),
        );
      });
    } finally {
      setState(() {
        _loading = false;
      });
      await _persistHistory();
      _autoScroll();
    }
  }

  Future<void> _retryLastFailed() async {
    final retryMessage = _lastFailedUserMessage;
    if (retryMessage == null || _loading) return;
    await _send(retryMessage);
  }

  Future<void> _clearChat() async {
    setState(() {
      _messages.clear();
      _errorText = null;
      _warningText = null;
      _lastFailedUserMessage = null;
    });
    await _persistHistory();
  }

  Future<void> _onMicTap() async {
    final spoken = await _voiceService.captureVoiceCommand();
    if (spoken == null) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Voice capture not configured yet.')),
      );
      return;
    }
    await _send(spoken);
  }

  void _openDevices() {
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => const DevicesScreen()));
  }

  void _openRoutines() {
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => const RoutinesScreen()));
  }

  void _openMemory() {
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => MemoryScreen(messages: _messages)));
  }

  void _autoScroll() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_scrollController.hasClients) return;
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 220),
        curve: Curves.easeOut,
      );
    });
  }

  String _formatTimestamp(DateTime timestamp) {
    final time = TimeOfDay.fromDateTime(timestamp);
    return time.format(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Jarvis'),
        actions: [
          IconButton(
            onPressed: _clearChat,
            icon: const Icon(Icons.delete_outline),
            tooltip: 'Clear chat',
          ),
          IconButton(
            onPressed: _openDevices,
            icon: const Icon(Icons.devices_other),
            tooltip: 'Devices',
          ),
          IconButton(
            onPressed: _openRoutines,
            icon: const Icon(Icons.auto_awesome),
            tooltip: 'Routines',
          ),
          IconButton(
            onPressed: _openMemory,
            icon: const Icon(Icons.memory),
            tooltip: 'Memory',
          ),
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
            child: QuickActions(onTap: _runAction),
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
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    _errorText!,
                    style: TextStyle(color: Colors.red.shade900),
                  ),
                  if (_lastFailedUserMessage != null)
                    TextButton.icon(
                      onPressed: _loading ? null : _retryLastFailed,
                      icon: const Icon(Icons.refresh),
                      label: const Text('Retry last message'),
                    ),
                ],
              ),
            ),
          if (_warningText != null)
            Container(
              width: double.infinity,
              margin: const EdgeInsets.fromLTRB(12, 0, 12, 8),
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.amber.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.amber.shade200),
              ),
              child: Text(
                _warningText!,
                style: TextStyle(color: Colors.amber.shade900),
              ),
            ),
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
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
                      border: message.failed ? Border.all(color: Colors.red.shade300) : null,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(message.text),
                        const SizedBox(height: 4),
                        Text(
                          _formatTimestamp(message.timestamp),
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
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
            child: ChatInput(onSend: _send, enabled: !_loading, onMicTap: _onMicTap),
          ),
        ],
      ),
    );
  }
}
