import 'package:flutter/material.dart';

class DevicesScreen extends StatelessWidget {
  const DevicesScreen({super.key});

  static const _devices = [
    ('Bedroom Light', 'Light • Bedroom', 'Available'),
    ('Bed Lamp', 'Light • Bedroom', 'Available'),
    ('Front Door Cam', 'Camera • Entry', 'Available'),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Devices')),
      body: ListView.builder(
        itemCount: _devices.length,
        itemBuilder: (context, index) {
          final item = _devices[index];
          return ListTile(
            leading: const Icon(Icons.devices_other),
            title: Text(item.$1),
            subtitle: Text(item.$2),
            trailing: Text(item.$3, style: const TextStyle(color: Colors.green)),
          );
        },
      ),
    );
  }
}
