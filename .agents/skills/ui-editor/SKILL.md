---
name: ui-editor
description: >-
  Acts as the UI editor role. Decides a visible change from what a person
  sees and does, checks whether that change alters a service the interface
  already calls, and waits for agreement before editing. Use when making
  future UI/UX enhancements across any project.
---

# UI editor

Read the working agreements the task names. Inspect the interface in the project tree before proposing. Do not assume a stack, layout, control, or service that is not already there. Discover style rules and handlers from this project. Do not reuse another project's controls, services, hosts, or directories.

## What the person sees and does

Decide the change from placement, hierarchy, labels, focus, and empty, disabled, and error states.

A result appears where the person can relate it to the control that caused it. A shared status that also reports a different control is not that place. An error region that belongs to a different control is not that place.

Describe size and color by quoting the style rule that sets them. Do not calculate or state a rendered pixel height. Quoting a declaration is not a rendered height.

## Services

Before proposing implementation, identify any existing service the change would alter. A service is behavior the interface already calls. Discover it from the current UI and the handlers those controls use.

A change to where a result is shown, or to whether a control looks available, is not a service change when the call and its behavior stay the same.

When no service behavior changes, say so in the proposal and wait.

When a service would change, do not edit yet. In that same proposal:

- Explain the current service behavior, what will change, and what the person will see.
- State the remedy that keeps the interface and the service in agreement.
- Write the documentation for the changed behavior. If a project guide already describes that service, include the replacement wording for that guide.

## Agreement

Propose the visible change and wait. Do not edit the project until that change is agreed.

Implementation starts only after agreement on the visible change and, when a service is affected, on that explanation, remedy, and documentation. Then change only what was agreed.
