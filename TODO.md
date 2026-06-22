
## Core Event Bus

- [ ] Implement the passive global Event Bus in `Core/` (e.g. `Core/EventBus.cs` + event structs) so inter-domain communication is possible without cross-domain references.

## Verification

- [ ] Grep all domain scripts for cross-domain `using` statements; confirm zero violations.
- [ ] Confirm every domain folder has a `.asmdef` referencing only Core via GUID.
- [ ] Confirm every conditional route in `.opencode/config.json` resolves to an existing doc file.
