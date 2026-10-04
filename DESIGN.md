---
name: "Agentic Skills / Security Proof"
description: "An evidence-first security research interface staged as a print-production proof sheet"
colors:
  proof-paper: "#f3f0e7"
  rail-paper: "#e9e4d8"
  evidence-white: "#fffdf7"
  canvas-gray: "#d8d6cf"
  register-ink: "#101c2d"
  annotation-ink: "#4d5968"
  hairline: "#aeb5b8"
  registration-cyan: "#00637c"
  warning-orange: "#ad3515"
  verification-green: "#087a50"
  threshold-amber: "#9a6500"
  terminal-cyan: "#a8e1ef"
  decoded-coral: "#ffd0c2"
typography:
  display:
    fontFamily: '"Arial Narrow", "Aptos Narrow", "Roboto Condensed", Arial, sans-serif'
    fontSize: "clamp(2.5rem, 5.8vw, 5.5rem)"
    fontWeight: 900
    lineHeight: 0.86
    letterSpacing: "-0.04em"
  headline:
    fontFamily: '"Arial Narrow", "Aptos Narrow", "Roboto Condensed", Arial, sans-serif'
    fontSize: "clamp(2rem, 4vw, 4rem)"
    fontWeight: 900
    lineHeight: 0.92
    letterSpacing: "-0.035em"
  title:
    fontFamily: '"Arial Narrow", "Aptos Narrow", "Roboto Condensed", Arial, sans-serif'
    fontSize: "2rem"
    fontWeight: 900
    lineHeight: 0.95
  body:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif'
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "0.68rem"
    fontWeight: 900
    lineHeight: 1.5
    letterSpacing: "0.08em"
rounded:
  square: "0px"
spacing:
  tight: "8px"
  control: "14px"
  content: "20px"
  panel: "24px"
  section: "28px"
  frame: "42px"
components:
  stage-button:
    backgroundColor: "transparent"
    textColor: "{colors.register-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "7px 8px 7px 0"
    height: "56px"
  stage-button-active:
    backgroundColor: "{colors.warning-orange}"
    textColor: "{colors.evidence-white}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    size: "34px"
  proof-action:
    backgroundColor: "transparent"
    textColor: "{colors.evidence-white}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "0.6rem 1rem"
    height: "42px"
  nav-button:
    backgroundColor: "transparent"
    textColor: "{colors.register-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "0.45rem 0.7rem"
    height: "38px"
  evidence-card:
    backgroundColor: "{colors.evidence-white}"
    textColor: "{colors.register-ink}"
    rounded: "{rounded.square}"
    padding: "24px"
  status-pass:
    backgroundColor: "transparent"
    textColor: "{colors.verification-green}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "0.35rem 0.5rem"
---

# Design System: Agentic Skills / Security Proof

## Overview

**Creative North Star: "The Security Proof Sheet"**

The interface behaves like a print-production proof sheet prepared for technical review: warm paper, crop marks, registration color, measured rules, editorial annotations, and stamped outcomes. It feels investigative and handmade enough to be memorable, but never theatrical; the visual authority comes from visible evidence, explicit boundaries, and a disciplined sequence rather than from a generic dark security-dashboard aesthetic.

The system is built for explanation. Condensed headlines announce the current claim, monospace labels expose its provenance and state, and a neutral reading face carries the reasoning. Cyan registers structure, green verifies observed outcomes, and orange marks failures, warnings, active steps, and unresolved boundaries. Every visual state must remain legible without color and every factual claim stays adjacent to the evidence that supports it.

**Key Characteristics:**

- Warm, physical proof-sheet surfaces framed by crop marks, rules, ticks, ledgers, and stamps.
- A three-voice type system: condensed display, neutral body, and monospace evidence labels.
- Flat, square geometry with one deliberately offset sheet shadow and no decorative rounding.
- Sparse semantic color: cyan for registration, green for verification, and orange for attention or failure.
- Sequential evidence presentation that keeps navigation, stage, and claim status visible together.

## Colors

The palette combines near-navy technical ink with warm paper stock and three tightly governed production colors.

### Primary

- **Registration Cyan:** Registers labels, evidence codes, focus outlines, and technical accents. It signals structure and traceability rather than success.

### Secondary

- **Warning Orange:** Marks the active stage, failed experiments, risk thresholds, correlations, and blocked or cautionary states.
- **Verification Green:** Marks observed passes, verified results, and successful evidence states.

### Neutral

- **Register Ink:** Supplies headlines, primary text, hard rules, terminal surfaces, and selected controls.
- **Annotation Ink:** Carries secondary explanation, boundaries, and low-emphasis metadata.
- **Proof Paper:** The primary sheet surface; its warmer companion separates the stage rail from the evidence field.
- **Evidence White:** Lifts contained evidence blocks just enough to read as pasted proof or a clean worksheet.
- **Canvas Gray:** Sits outside the proof sheet so the artifact reads as a physical object.
- **Hairline:** Supports table rows, internal dividers, tracks, and quiet measurement structure.

### Named Rules

**The Evidence Color Rule.** Cyan means registration, green means verified, and orange means attention; never interchange these roles for decoration.

**The Ink Before Accent Rule.** Structural lines and headings use register ink first. Accent color appears only where it adds state, provenance, or navigation meaning.

## Typography

**Display Font:** Arial Narrow, with Aptos Narrow, Roboto Condensed, Arial, and sans-serif fallbacks  
**Body Font:** Platform system UI, with Segoe UI and Arial fallbacks  
**Label/Mono Font:** UI monospace, with SFMono-Regular, Menlo, Consolas, and monospace fallbacks

**Character:** The condensed display face makes the artifact feel like a labeled technical plate. The body face keeps explanations calm and readable, while the monospace voice turns metadata, scores, commands, and controls into inspectable evidence.

### Hierarchy

- **Display** (900, responsive 2.5–5.5rem, line-height 0.86): The artifact title only; uppercase, tightly tracked, and allowed to dominate the masthead.
- **Headline** (900, responsive 2–4rem, line-height 0.92): One stage claim at a time, uppercase and separated from evidence by a heavy rule.
- **Title** (900, typically 1.4–2rem, line-height about 0.95): Evidence-block titles, platform names, and signature component headings.
- **Body** (400, 16px, line-height 1.5): Explanations and claim boundaries, normally constrained to 48–72 characters per line.
- **Label** (800–900, 0.62–0.76rem, letter-spacing 0.08em where used): Stages, metadata, statuses, scores, commands, and controls; generally uppercase.

### Named Rules

**The Three Voices Rule.** Condensed type states the claim, body type explains it, and monospace type proves or operates it.

**The One Claim Rule.** Each evidence panel opens with one large headline; supporting labels stay small enough that they cannot compete with it.

## Layout

The artifact is a centered sheet up to 1520px wide, inset 16px from the desktop canvas. Its masthead and four-cell result strip establish context before the main workspace splits into a fixed 300px trace rail and a flexible evidence field. The evidence field uses 24–58px responsive side padding and reserves its lower edge for persistent previous/next controls.

Inside a stage, grids compare two definitions, three limit columns, a technique selector with its proof, or a source payload with its verdict. Spacing follows the observed 8px, 14px, 20px, 24px, 28px, and 42px rhythm; compact metadata sits close to its evidence, while stage changes receive the largest gaps.

At 940px and below, the vertical rail becomes a horizontally scrollable stage strip, the sheet fills the viewport, and multi-column proof layouts collapse. At 600px and below, paired evidence becomes a single column, event arrows rotate, low-priority table detail hides, and progress moves above the navigation buttons. Print mode removes navigation and interactions, expands every stage, and page-breaks the complete trace into an auditable document.

**The Claim Beside Proof Rule.** A conclusion and its supporting artifact share the same panel; do not force the reader to remember evidence from another screen.

**The Trace Survives Rule.** Responsive changes may rotate or stack the route, but they must preserve all eight stages and their reading order.

## Elevation & Depth

The system is flat inside the artifact. Borders, one-pixel gaps, paper-tone changes, and dark reversed surfaces create hierarchy. The only ambient elevation belongs to the proof sheet itself (`8px 10px 24px rgba(16, 28, 45, .14)`), making it read as a physical review object resting on a neutral desk.

### Shadow Vocabulary

- **Offset Sheet:** A single directional shadow under the outer proof sheet. It establishes the artifact boundary and is removed in print.

### Named Rules

**The One Sheet Shadow Rule.** Never add drop shadows to evidence cards, controls, stamps, or rows; use rules, tone, or reversed ink instead.

## Shapes

The form language is square, ruled, and mechanical. Panels, controls, status labels, table tracks, and stage markers use zero radius. One-pixel hairlines define ordinary divisions; two-pixel ink rules establish section boundaries; four-pixel rules terminate major panel headers. Crop-mark corners and the slightly rotated double-line proof stamp provide the only expressive silhouettes.

**The No Soft Corners Rule.** Rounded cards and pill badges break the proof-sheet metaphor; keep components square, including compact status labels.

## Components

### Stage Trace

The signature navigation is a numbered production route: a vertical ruled rail on desktop and a horizontal strip on smaller screens.

- **Shape:** Square 34px numbered markers on desktop and 30px markers below 940px.
- **Default:** Transparent control, ink border, rail-paper marker, and condensed uppercase stage name.
- **Current:** Orange-filled marker with white number; the stage name also turns orange, preserving a text cue beyond fill color.
- **Behavior:** Click, previous/next buttons, and global left/right arrow keys all move through the same eight-stage sequence.

### Buttons

Buttons look like labeled proofing controls rather than product UI chrome.

- **Shape:** Square corners, ink or white 1–2px borders, and compact monospace uppercase labels.
- **Primary Action:** Transparent on a register-ink bar with a white 2px border; hover reverses to evidence white with ink text.
- **Navigation:** Transparent on paper with a 1px ink border; hover reverses to ink with white text.
- **Focus:** A 3px registration-cyan outline with a 3px offset is mandatory on every button and link.
- **Disabled:** Navigation remains in place at 35% opacity so the trace geometry does not jump.

### Cards / Containers

- **Corner Style:** Square with no radius.
- **Background:** Proof paper for the main field, rail paper for route navigation, evidence white for contained proofs, and register ink for terminal or telemetry surfaces.
- **Shadow Strategy:** No local card shadows; see the One Sheet Shadow Rule.
- **Border:** One-pixel register-ink frames and dividers, with two- or four-pixel rules only at hierarchy changes.
- **Internal Padding:** Usually 20–24px, expanding responsively to 36–38px for major paired definitions.

### Tabs and Comparison Switches

- **Style:** Square, border-built controls with condensed or monospace uppercase labels.
- **Selected:** Register-ink fill with evidence-white text; technique tabs keep their orange numeric index visible.
- **Behavior:** Technique tabs implement roving keyboard focus. Binary V1/V2 controls expose pressed state and change both the payload representation and verdict.

### Proof Stamps and Status Labels

- **Proof Stamp:** Green or orange text inside a 3px double border, rotated by -2 degrees to evoke manual verification.
- **Status Label:** Unrotated, centered, and framed by a 2px border in the same semantic color as its text.
- **Meaning:** Green is observed/verified; orange is warning, blocked, synthetic, failed, or bounded.

### Evidence Ledgers

Tables, score ledgers, runtime lanes, and platform rows all use horizontal rules rather than detached cards. Numeric scores and event names use monospace type; totals and correlations move to orange; verified verdicts move to green. Hover may lift a row from proof paper to evidence white, but it must not create a floating surface.

### Progress and Motion

Stage changes settle upward over 340ms; the route progress line scales over 280ms; runtime evidence nodes enter over 400ms with one short stagger. Motion explains state transition or correlation and is disabled to near-zero under reduced-motion preferences.

## Do's and Don'ts

### Do:

- **Do** attach every claim to a visible score, code sample, ledger row, boundary statement, or reproduction command.
- **Do** use the condensed/body/monospace hierarchy consistently so claims, reasoning, and evidence remain distinguishable.
- **Do** reserve cyan, green, and orange for their named semantic roles and reinforce every color state with text or shape.
- **Do** preserve the eight-stage trace, visible focus, keyboard operation, reduced motion, and the complete print view.
- **Do** use rules, paper tones, and reversed ink to create hierarchy inside the sheet.

### Don't:

- **Don't** convert the interface into a dark, glowing, metric-card security dashboard.
- **Don't** use rounded cards, pill badges, gradients, glass effects, or decorative shadows.
- **Don't** present a Benign label, score, or platform result without its explicit claim boundary.
- **Don't** detach failure from improvement; the V1 miss and V2 decoded-layer change belong in the same comparison.
- **Don't** animate for spectacle or leave hidden stages unavailable in the print artifact.
