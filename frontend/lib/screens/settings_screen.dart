import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: const [
          ListTile(
            leading: Icon(Icons.devices),
            title: Text('Devices (placeholder)'),
            subtitle: Text('Manage aliases and room mappings'),
          ),
          ListTile(
            leading: Icon(Icons.repeat),
            title: Text('Routines (placeholder)'),
            subtitle: Text('Routine builder will be added later'),
          ),
        ],
      ),
    );
  }
}
