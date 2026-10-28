# Calm dashboard rules

These rules are distilled from a measured teardown of an "unslopped" dashboard: a frame-by-frame, pixel-measured before and after. They were then applied to a full production app and verified with counts. They are **structure first, then colour**. Colour changes alone don't make an interface calm: a redesign that only recoloured 19 boxes looked unchanged, and only removing the boxes worked.

This file is shipped identically in both skills (`dashboard-unslop` and `dashboard-blueprint`), so either works on its own.

Units are points (pt). Web: 1 pt = 1 CSS px at 1×.

---

## R1. Surfaces: three levels, no more

| Level | What it is | Dark example | Light example |
|---|---|---|---|
| 0 | Navigation column (the darkest or most recessive) | `#0D0D0D` | `#F2F2F0`, or a deliberate charcoal |
| 1 | Canvas (the page) | `#141414` | `#FAFAF9` |
| 2 | Card: canvas + one step, 1 px border about 6% stronger, radius 8–10 | `#191919`, border `#262626` | `#FFFFFF`, border `#E6E6E3` |

- **No fourth level.** No tinted washes behind sections, no gradient panels, no glows, no drop shadows except on things that float (popovers, menus, toasts, sheets).
- **The navigation column is part of the window, not a card.** It is flush to the window edges and separated from the content by a **1 px full-height hairline**.
- **No floating, inset or rounded sidebar.** (macOS 26 `NavigationSplitView` does this by default; see the platform notes.)

## R2. Box budget (the most important rule)

A **box** is anything with a fill different from its parent, or a visible border.

- **Allowed boxes:**
  - metric tiles;
  - one chart or one preview surface per region;
  - text inputs;
  - the selected navigation row;
  - the page's single primary button;
  - floating layers (sheets, popovers, menus).
- **Never a box:**
  - lists and list rows;
  - sections and their headings;
  - status lines;
  - counts and badges;
  - secondary and row buttons;
  - label chips;
  - "connection diagrams";
  - empty states;
  - hero call-outs.
- **Lists:** a section heading, a hairline, then rows separated by hairlines, directly on the canvas.
- **Rows:** the **whole row is the button**. Its action word is grey text before a chevron.

## R3. Buttons

- **One filled button per screen:** the primary. 28 pt tall (32 in hero or wizard footers), 12–14 pt horizontal padding, radius 7, 13.5 pt medium text. It is the only saturated, filled thing.
- **Every other action is a text action.** No resting border or fill, a 28 pt hit area, and a soft wash on hover. Destructive is red text.
- **No pills or capsules anywhere.** Counts are mono grey text. A state is a 6 pt dot plus words. A filter is plain words, with the chosen one on a soft square wash.

## R4. Colour budget

Saturated colour may appear only for:

1. the single primary action;
2. status, always a dot plus words: green ok, amber warning, red problem;
3. data: chart series, deltas, category dots;
4. the brand mark.

Everything else is neutral: selection, tabs, links, icons, secondary buttons, counts and switches. **Target: ≤ 3 saturated elements per screen, ≤ 1 filled.**

## R5. Type

| Role | Size and weight | Colour |
|---|---|---|
| Page title | 28–32 **regular**, tracking −0.5; optional two-tone tail ("October **2026**", with the tail in grey) | ink / ink3 |
| Section title | 15 semibold | ink |
| Row title, body | 14 medium / 14 regular | ink |
| Detail, card label | 13 regular | ink3 |
| Card value | 28 semibold | ink |
| Meta: counts, deltas, section labels, axis labels | 12.5 **monospaced**, sentence case | ink3 |

- **No ALL-CAPS tracked eyebrows.**
- **No bold for decoration.**
- **No exclamation marks or emoji.**
- **No greeting headlines.** A heading states the place or the period.

Ink ramp on dark: `#EDEDED` / `#A7A7A7` / `#737373`. On light: `#141414` / `#3D3D40` / `#6B6B70`.

## R6. Geometry and rhythm

| Item | Value |
|---|---|
| Navigation width | 240–248 |
| Header line | 44 tall, shared across the navigation column and the content: one line, not two toolbars |
| Navigation insets | boxes inset 12 from each edge; **icon column at 24**, **label column at 50**; counts right-aligned 24 from the hairline |
| Navigation rows | **32 pitch, no gaps**; selected = a 32-tall box, radius 7, fill +1 step, white text, filled glyph; unselected = grey text, outline glyph, no box |
| Navigation groups | full-width hairline, then a mono label 24 below it, then rows |
| Content | **one left edge**, 28 from the hairline; max width about 1080–1180 |
| Vertical rhythm | title → content 28; **between sections 32**; between tiles 16 |
| Card padding | 20 |
| List rows | ≥ 52 tall, 16 pt glyph column, hairline under each |
| Spacing scale | 4 / 8 / 12 / 16 / 20 / 24 / 28 / 32, nothing else |

## R7. Numbers

- **A metric tile** has a label, a value, and an **optional honest comparison**: "+12%" (green or red) followed by " vs last month" (mono grey).
- **Never invent a comparison.** No delta is better than a fake one.

## R8. Charts

- **Lines and marks:** thin lines (1.5–2 pt), one colour per series, an optional glow on the line only.
- **Axes and grid:** mono axis labels, faint gridlines.
- **Not allowed:** fat rounded bars, gradient-filled bars, unlabelled axes.

## R9. Acceptance metrics (measured per screen, not judged by eye)

| Metric | Target |
|---|---|
| (a) Boxed shapes | ≤ 8 |
| (b) Pills / capsules | 0 |
| (c) Filled or bordered buttons | ≤ 1 |
| (d) Box nesting depth (window → box → box…) | ≤ 2 |
| (e) Distinct content left edges | 1 (2 when there's a master/detail split) |
| (f) Navigation row pitch | one value (32); a secondary list may use a second value (30) |
| (g) Saturated-colour elements | ≤ 3 |

Reference counts from the original teardown:

| | (a) | (b) | (c) | (d) | (e) |
|---|---|---|---|---|---|
| Vibecoded "before" | 17 | 9 | — | 3 | 3 |
| Calm "after" | 9 | 0 | 0 | 2 | 1 |

## Platform notes

**SwiftUI / macOS 26.**
- `NavigationSplitView` draws its sidebar as a floating glass card, and toolbar items get glass capsules. Neither can be restyled away.
- **Window:** use `.windowStyle(.hiddenTitleBar)`; the root is `HStack(spacing: 0) { Sidebar.frame(width:); Hairline; Content }`; use your own 44 pt header line, with an NSView `performDrag` area for window dragging.
- **Commands:** replace `SidebarCommands` with your own show/hide command.
- **API availability:** `Group(subviews:)` needs macOS 15. On 14, let each row draw its own bottom hairline.
- **Controls:** tint native switches with a neutral slate.

**Web (React, Tailwind, CSS).**
- **Layout:** `grid-template-columns: 244px 1px 1fr` on a full-height root. No `rounded-*` or `shadow-*` on the sidebar or sections.
- **Lists:** use `divide-y` rows, never cards.
- **Classes to delete:** `rounded-full` (pills), `bg-gradient-*`, `shadow-*`, `ring-*` on resting elements, emoji in strings, and `uppercase tracking-wider` labels.
- **Type:** mono via `font-mono text-[12.5px]`.
- **Code audit:** grep for `rounded-full`, `gradient`, `shadow`, `ring-`, `uppercase`, `!!` and emoji ranges as a first pass.
