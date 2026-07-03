# Player Controller Roadmap

Current phase: Phase 1 — Document and baseline
Last updated: 2026-06-26

## Summary

The project will keep Unity Starter Assets for whitebox traversal, then replace the player with project-owned input, motor, view, interaction, and animation components. The final production path supports runtime switching between third-person and full-body first-person presentation.

The architectural decision is recorded in `docs/architecture/decisions/ADR-0001-player-controller.md`.

## Current implementation inventory

- Scene: `MoonGame/Assets/Scenes/SampleScene.unity`
- Current whitebox player: Starter Assets `PlayerArmature`
- Current whitebox camera: Starter Assets `PlayerFollowCamera`
- Current controller script: `StarterAssets.ThirdPersonController`
- Current input bridge: `StarterAssetsInputs`
- Current prefab input asset: `MoonGame/Assets/StarterAssets/InputSystem/StarterAssets.inputactions`
- Future project input asset: `MoonGame/Assets/InputSystem_Actions.inputactions`

Observed current movement settings:

- CharacterController height: `1.8`
- CharacterController radius: `0.28`
- Slope limit: `45`
- Step offset: `0.25`
- Walk speed: `2`
- Sprint speed: `5.335`
- Rotation smoothing: `0.12`
- Speed change rate: `10`
- Jump height: `1.2`
- Gravity: `-15`
- Jump timeout: `0.3`
- Fall timeout: `0.15`

## Phase 1: Document and baseline

Goal: keep Starter Assets untouched and record the traversal baseline.

Checklist:

- [x] Record current Starter prefab, camera, input asset, and movement settings.
- [x] Record the accepted player architecture decision.
- [ ] Test flat movement.
- [ ] Test slopes.
- [ ] Test stairs.
- [ ] Test jumping.
- [ ] Test sprinting.
- [ ] Test collision and wall sliding.
- [ ] Test camera readability in whitebox spaces.
- [ ] Test interaction distance once a simple interact target exists.

Completion evidence:

- Traversal notes are added to this roadmap.
- No Starter Assets files are modified.

## Phase 2: Own input

Goal: move gameplay input ownership into project code while keeping Starter movement temporarily.

Checklist:

- [ ] Rename `Attack` to `Fire` in `MoonGame/Assets/InputSystem_Actions.inputactions`.
- [ ] Add missing actions: `Aim`, `TogglePerspective`, and `Pause`.
- [ ] Add `PlayerInputReader`.
- [ ] Switch the player prefab to `InputSystem_Actions.inputactions`.
- [ ] Verify keyboard/mouse and gamepad parity.
- [ ] Keep Starter Assets movement working during this phase.

Completion evidence:

- Gameplay code reads logical input from `PlayerInputReader`.
- No new gameplay code reads devices directly, such as `Keyboard.current` or `Mouse.current`.

## Phase 3: Own movement

Goal: replace Starter movement with a project-owned `CharacterControllerMotor`.

Checklist:

- [ ] Add `CharacterControllerMotor`.
- [ ] Preserve validated movement tuning from Phase 1.
- [ ] Expose a readonly motor snapshot containing velocity, planar speed, grounded state, vertical speed, and facing.
- [ ] Remove `ThirdPersonController` from the production player prefab.
- [ ] Remove `StarterAssetsInputs` from the production player prefab.
- [ ] Keep animation and camera outside the motor.

Completion evidence:

- No production player prefab depends on `StarterAssets` scripts.
- Motor behavior remains stable with camera code disabled or replaced.

## Phase 4: Switchable camera presentation

Goal: support runtime switching between third-person and a bodyless first-person camera.

Checklist:

- [ ] Add `PlayerViewCoordinator`.
- [ ] Add `ThirdPersonView`.
- [ ] Add bodyless `FirstPersonView`.
- [ ] Add `TogglePerspective`.
- [ ] Ensure exactly one active camera and one active audio listener.
- [ ] Preserve root position, velocity, camera heading, and gameplay state during switching.
- [ ] Test switching while idle.
- [ ] Test switching while moving.
- [ ] Test switching while jumping.
- [ ] Test switching while falling.
- [ ] Route interaction and aiming through the active aim origin.

Completion evidence:

- Perspective switching causes no teleport, velocity reset, duplicate camera, duplicate audio listener, or input loss.
- Interaction targets remain consistent across views.

## Phase 5: Full-body first-person presentation

Goal: add full-body first-person visuals without changing movement truth.

Checklist:

- [ ] Add the shared full-body model under `ModelRoot`.
- [ ] Hide or mask local head geometry when needed.
- [ ] Preserve external model visibility, shadows, and reflections.
- [ ] Add upper-body aim offset.
- [ ] Add arm IK and weapon targets when weapons require it.
- [ ] Keep camera motion independent from animation.
- [ ] Validate clipping.
- [ ] Validate look-down body visibility.
- [ ] Validate weapon alignment.
- [ ] Validate animation jitter.

Completion evidence:

- Camera drives aim.
- Body follows camera.
- Body does not drive camera.

## Test and completion gates

- No project gameplay system imports `StarterAssets`.
- Starter classes disappear from the production player prefab after Phase 3.
- Motor behavior remains unchanged when camera mode changes.
- Perspective switching causes no teleport, velocity reset, duplicate camera, or input loss.
- Interaction targets remain consistent across views.
- Automated tests cover input edge semantics and motor state transitions once project-owned systems exist.
- Play Mode tests cover enable/disable, view switching, jumping, and scene reload once project-owned systems exist.
- Manual first-playable support targets keyboard/mouse and gamepad.
- Touch, XR, networking, IK polish, and weapon animation remain deferred until required.

## Continuation rule

Keep this roadmap live. Update the current phase, checklist state, completion evidence, and date whenever implementation progresses. Keep `TODO.md` focused only on the next incomplete milestone, not the full roadmap.
