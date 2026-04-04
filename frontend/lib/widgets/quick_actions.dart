import 'package:flutter/material.dart';

class QuickActions extends StatelessWidget {
  const QuickActions({super.key, required this.onTap});

  final ValueChanged<String> onTap;

  static const _actions = <String>[
    'Turn on bedroom light',
    'Show front door camera',
    'Run morning routine',
    'Run bedtime routine',
  ];

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: _actions
            .map(
              (label) => Padding(
                padding: const EdgeInsets.only(right: 8),
                child: ActionChip(
                  label: Text(label),
                  onPressed: () => onTap(label),
                ),
              ),
            )
            .toList(),
      ),
    );
  }
}
