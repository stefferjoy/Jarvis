import 'package:flutter/material.dart';

import '../actions/assistant_action.dart';

class RoutinesScreen extends StatelessWidget {
  const RoutinesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final routines = AssistantActionCatalog.actions
        .where((a) => a.id == AssistantActionId.runMorningRoutine || a.id == AssistantActionId.runBedtimeRoutine)
        .toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Routines')),
      body: ListView(
        children: routines
            .map(
              (routine) => ListTile(
                leading: const Icon(Icons.auto_awesome),
                title: Text(routine.title),
                subtitle: Text(routine.description),
              ),
            )
            .toList(),
      ),
    );
  }
}
