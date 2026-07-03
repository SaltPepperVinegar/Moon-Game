# ADR-0001: Player Controller Architecture

Status: Accepted
Date: 2026-06-26

## Context

The current whitebox scene uses Unity Starter Assets:

- Scene: `MoonGame/Assets/Scenes/SampleScene.unity`
- Player prefab: Starter Assets `PlayerArmature`
- Camera prefab: Starter Assets `PlayerFollowCamera`
- Input asset in current prefab: `MoonGame/Assets/StarterAssets/InputSystem/StarterAssets.inputactions`
- Project-owned future input asset: `MoonGame/Assets/InputSystem_Actions.inputactions`

Starter Assets are useful for fast traversal testing, but they should not become the permanent gameplay-facing player architecture. The project also needs a future runtime switch between third-person and full-body first-person presentation.

## Decision

Keep the current Starter Assets controller untouched for whitebox. Do not deeply wrap `ThirdPersonController`.

Replace it later with project-owned player components that define stable gameplay boundaries:

- `PlayerRoot` owns position, `CharacterController`, velocity, collision, and gameplay identity.
- `PlayerInputReader` owns Input System access and exposes logical input.
- `CharacterControllerMotor` owns movement, grounding, gravity, jumping, and motion truth.
- `PlayerViewCoordinator` owns perspective switching and exposes the active aim origin.
- `ThirdPersonView` owns third-person camera presentation only.
- `FirstPersonView` owns first-person camera presentation only.
- `PlayerAnimationDriver` reads motor state; it never determines movement.
- `PlayerInteractor` uses the coordinator's aim origin, never a concrete camera.
- `ModelRoot` remains visual and replaceable.

Target prefab shape:

```text
PlayerRoot
├── CharacterController
├── PlayerInput
├── PlayerInputReader
├── CharacterControllerMotor
├── PlayerViewCoordinator
├── PlayerInteractor
├── PlayerState
├── CameraRig
│   ├── ThirdPersonView
│   └── FirstPersonView
└── ModelRoot
    └── FullBodyCharacterMesh
```

## Invariants

- Gameplay systems must not import or depend on `StarterAssets`.
- Starter Assets classes disappear from the production player prefab after the movement replacement phase.
- Camera rigs are controlled by code. Animated head bones never drive gameplay cameras.
- Third-person facing: body faces movement direction.
- First-person facing: body yaw follows camera yaw.
- Switching view preserves root position, velocity, camera heading, and gameplay state.
- Exactly one gameplay camera and one audio listener are active after a view switch.
- Interaction and aiming use the active aim origin exposed by `PlayerViewCoordinator`.
- Motor behavior remains unchanged when the camera mode changes.

## Input contract

Planned gameplay actions:

```text
Move, Look, Jump, Sprint, Crouch, Interact,
Fire, Aim, TogglePerspective, Pause, Previous, Next
```

`MoonGame/Assets/InputSystem_Actions.inputactions` already has most of these actions. Rename the existing `Attack` action to `Fire` when input migration begins, and add any missing actions at that time.

## Rejected alternatives

### Build full-body first-person immediately

Rejected because it would front-load camera clipping, animation, IK, weapon alignment, head-bone visibility, and body-shadow problems before the core gameplay space is proven.

### Deeply wrap `ThirdPersonController`

Rejected because it preserves Starter Assets assumptions in the project API. The safer path is to keep Starter Assets untouched for whitebox, then replace them once with project-owned components.

### Rigidbody-first movement

Rejected for the current phase. `CharacterController` gives more predictable traversal, slope, stair, and collision behavior for a whitebox character.

### Camera parented to animated head bone

Rejected because animation-driven camera motion causes jitter and view instability. The camera should drive aim; the body should follow the camera through animation/IK.

### Separate movement motors per perspective

Rejected because camera mode should not change movement truth. Perspective is presentation; the motor is gameplay.

## Consequences

- Whitebox remains fast because the current Starter Assets setup can stay in place.
- Player-facing gameplay code has a clear destination architecture.
- First-person can start as a bodyless camera presentation before full-body complexity is introduced.
- Documentation must be updated as phases complete, especially the live roadmap.

## Supersession rule

This ADR is historical once accepted. If the player architecture changes, create a new ADR that supersedes this one instead of rewriting the decision history.
