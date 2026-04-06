import 'package:flutter/material.dart';

import '../models/chat_message.dart';

class MemoryScreen extends StatelessWidget {
  const MemoryScreen({super.key, required this.messages});

  final List<ChatMessage> messages;

  @override
  Widget build(BuildContext context) {
    final memoryFacts = messages
        .where((m) => m.isUser && m.text.toLowerCase().startsWith('remember '))
        .map((m) => m.text.substring(9).trim())
        .where((m) => m.isNotEmpty)
        .toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Memory')),
      body: memoryFacts.isEmpty
          ? const Center(child: Text('No remembered facts yet.'))
          : ListView.builder(
              itemCount: memoryFacts.length,
              itemBuilder: (context, index) => ListTile(
                leading: const Icon(Icons.memory),
                title: Text(memoryFacts[index]),
              ),
            ),
    );
  }
}
