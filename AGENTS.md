# Jarvis

Build Jarvis as a unified AI assistant platform.

## Product direction
Jarvis is one assistant across multiple capabilities:
- natural language conversation
- memory
- routines
- device control
- camera access
- future voice support

## Stack
- Flutter frontend
- Python FastAPI backend
- local persistence first
- adapter-based integrations

## Architecture rules
- frontend is UI-first
- backend is the brain
- use one orchestrator agent first
- avoid unnecessary multi-agent complexity
- keep integrations behind adapters
- fail gracefully when external services are missing
- keep code modular and easy to test

## MVP priorities
1. Flutter chat app
2. FastAPI backend
3. orchestrator loop
4. persistent memory
5. device registry and aliases
6. stub tools for shortcuts, home devices, and cameras

## Coding rules
- make small safe changes
- do not refactor unrelated code
- explain architecture before major changes
- include run steps
- include review and verification notes

## Review standard
Check for:
- correctness
- regressions
- edge cases
- graceful failure paths
- overengineering

## Test standard
Verify:
- app starts
- frontend talks to backend
- memory persists
- device alias mapping works
- ambiguous device requests trigger clarification
