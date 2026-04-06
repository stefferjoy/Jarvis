enum AssistantActionId {
  runMorningRoutine,
  runBedtimeRoutine,
  turnOnBedroomLight,
  showFrontDoorCamera,
  openJarvisChat,
}

class AssistantAction {
  final AssistantActionId id;
  final String title;
  final String chatCommand;
  final String description;

  const AssistantAction({
    required this.id,
    required this.title,
    required this.chatCommand,
    required this.description,
  });
}

class AssistantActionCatalog {
  static const actions = <AssistantAction>[
    AssistantAction(
      id: AssistantActionId.runMorningRoutine,
      title: 'Run Morning Routine',
      chatCommand: 'run morning routine shortcut',
      description: 'Kick off your morning shortcut routine.',
    ),
    AssistantAction(
      id: AssistantActionId.runBedtimeRoutine,
      title: 'Run Bedtime Routine',
      chatCommand: 'run bedtime shortcut',
      description: 'Kick off your bedtime shortcut routine.',
    ),
    AssistantAction(
      id: AssistantActionId.turnOnBedroomLight,
      title: 'Turn On Bedroom Light',
      chatCommand: 'turn on bedroom light',
      description: 'Turn on the main bedroom light.',
    ),
    AssistantAction(
      id: AssistantActionId.showFrontDoorCamera,
      title: 'Show Front Door Camera',
      chatCommand: 'show front door camera',
      description: 'Open the front door camera feed.',
    ),
    AssistantAction(
      id: AssistantActionId.openJarvisChat,
      title: 'Open Jarvis Chat',
      chatCommand: 'hello jarvis',
      description: 'Open and focus chat with Jarvis.',
    ),
  ];

  static AssistantAction? byId(AssistantActionId id) {
    for (final action in actions) {
      if (action.id == id) {
        return action;
      }
    }
    return null;
  }

  static AssistantAction? byRawId(String rawId) {
    final normalized = rawId.trim().toLowerCase();
    for (final action in actions) {
      if (action.id.name.toLowerCase() == normalized) {
        return action;
      }
    }
    return null;
  }
}
