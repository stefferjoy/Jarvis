import 'package:flutter/material.dart';

import '../actions/assistant_action.dart';

class QuickActions extends StatelessWidget {
  const QuickActions({super.key, required this.onTap});

  final ValueChanged<AssistantAction> onTap;

  @override
  Widget build(BuildContext context) {
    final actions = [
      AssistantActionCatalog.byId(AssistantActionId.turnOnBedroomLight),
      AssistantActionCatalog.byId(AssistantActionId.showFrontDoorCamera),
      AssistantActionCatalog.byId(AssistantActionId.runMorningRoutine),
      AssistantActionCatalog.byId(AssistantActionId.runBedtimeRoutine),
    ].whereType<AssistantAction>().toList();

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: actions
            .map(
              (action) => Padding(
                padding: const EdgeInsets.only(right: 8),
                child: ActionChip(
                  label: Text(action.title),
                  onPressed: () => onTap(action),
                ),
              ),
            )
            .toList(),
      ),
    );
  }
}
