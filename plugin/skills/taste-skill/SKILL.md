---
name: design-taste-frontend
description: >-
  tasteskill v2, the anti-slop frontend skill. Art direction for websites, distilled from a study of
  247 curated gallery sites (One Page Love, Awwwards Sites of the Day). Deals researched directions
  (idea, composition, type, palette, photographs, section blueprints) from a library, enforces a strict
  no-slop house style with a real-browser inspector, and runs a look-and-fix loop on screenshots. Use
  this whenever you build, design, redesign, restyle, polish or review a landing page, marketing site,
  portfolio, product page, one-pager, hero or any public-facing web page, in any stack (HTML/CSS, React,
  Next.js, Vue, Svelte, Astro, Tailwind) — also when the user says a page looks generic, templated,
  "AI-made", sloppy, or asks to make it look designed, premium, award-level or less like every other
  site. Also for app screens: dashboards, admin and analytics views, settings, inboxes and other screens
  people work in, with their own run and rules.
---

# Taste — scoped entry

First read the shared [UI task policy](../devflow/references/ui-task-policy.md). Use the same policy for direct invocation and router use; it scopes all longer Taste references and house-style defaults.

## Small fix or existing component

Follow the policy's focused route: inspect the affected component and state, preserve accepted brand/stack, implement the requested correction, and verify the affected interaction, keyboard focus/accessibility and relevant viewport. Do not read the full app/site chapters, draw a new direction, generate images or restyle unrelated components for this route. Read a specific reference section only if needed to solve the actual defect. A purple sidebar or floating label is not itself a reason to replace approved design. Style lint is advisory where it conflicts with accepted aesthetics; actual behavior and accessibility checks remain required.

## New screen in an existing system

Reuse the accepted direction and components. Load relevant sections of [app-screen guidance](references/app-screens.md) for working interfaces or [site guidance](references/full-workflow.md) for public pages. A new screen does not require a new palette, typeface or draw.

## New direction or authorized redesign

Read [the full workflow](references/full-workflow.md). For dashboards, admin, tables, inboxes or settings, use [app screens](references/app-screens.md) and `--app`; for marketing pages use the site run. Reconcile candidates with one design record and the user's constraints. Use `--keep palette,type` when drawing around an existing identity. House preferences cannot override the shared policy.

## Review and tools

For audit-only requests, report findings without editing. Inspect actual rendered output when possible; missing browser/native capabilities stay pending. A lint result is not proof of interaction, accessibility, visual quality or owner acceptance.

Resolve `<skill>` to this directory. Run helpers from the project working directory and store outputs in private project artifacts. Node 22+ is required for the complete toolset; browser inspection also needs an available Chrome/Edge/Chromium environment. Load script-specific usage only when using that helper. No full inspector or image workflow is mandatory for a focused fix; use the project's appropriate targeted checks.
