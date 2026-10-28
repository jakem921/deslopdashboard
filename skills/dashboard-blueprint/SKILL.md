---
name: dashboard-blueprint
description: Set up the rule structure for a NEW dashboard or app UI before any screens are built, covering shell, surfaces, type, kit components, page templates, box and colour budgets, and measurable acceptance, so it starts calm instead of needing to be "unslopped" later. Use when starting a dashboard, admin panel, SaaS app or desktop app UI, or when asked for a design system or layout rules for one.
---

# Dashboard blueprint (new builds)

Decide the structure first, encode it in a small kit, and accept screens by measurement. The rules are in `RULES.md` next to this file. Read them first; this skill turns them into a project. The measuring tool is `${CLAUDE_SKILL_DIR}/tools/measure.py` (pure Python 3, no dependencies).

## Step 1: Ask only what's the user's to decide

Ask in one round, with a recommended default for each:

- **Product feel:** light, dark, or both (design both regardless).
- **Brand colour:** one hue. It's used only for the primary action, the brand mark and data (R4).
- **Navigation treatment:** a recessive column (the default), or a deliberately branded one (charcoal, or a whisper of brand colour at the foot, but never a floating card).
- **Brand texture,** if any: a faint grid or glow on the canvas at very low strength, never a solid brand field.
- **Mono metadata:** yes by default.
- **Audience:** with lay users, also require plain words and one obvious next step per screen.

## Step 2: Write the blueprint document

Use `template.md` in this folder, saved as the project's design spec. Fill in each section; nothing is left as "TBD".

1. **Shell:** window or root layout, navigation width, the header line, where search and back/forward live, and navigation geometry (icon column 24, label column 50, 32 pt rows, groups with hairlines and mono labels).
2. **Surfaces:** exactly three levels, with hex values for light and dark, and the border and radius of cards.
3. **Type scale:** from R5, in the project's font.
4. **Colour budget:** which elements may be saturated, and what is neutral (R4).
5. **Kit:** the components that every screen must be built from. Screens never style ad hoc.
   - `PageScaffold` / `PageTitle`
   - `ListSection` + `ListRow` (unboxed, the whole row is the button)
   - `MetricTile` (label, value, optional honest delta)
   - `Panel` (restricted: charts, previews and tiles only)
   - `Primary` (the only filled button)
   - `TextAction`
   - `StatusLine`
   - `FilterWords`
   - `EmptyState` (unboxed)
   - `Sheet` (header, content, footer with Cancel text and one primary)
6. **Page templates:** a small set, named in the spec:
   - Dashboard (title, tiles, one chart, lists);
   - List (title with primary, filter words, ListSection);
   - Master/detail (bare list column plus one preview surface);
   - Settings (labelled rows separated by hairlines);
   - Wizard (one card, step line, question, fields, footer);
   - Empty / intro (unboxed: symbol, title, one line, up to 3 benefits, primary).
7. **Box budget:** R2, copied in with the project's own names for each allowed box.
8. **Acceptance:** the R9 targets, how they're measured (`${CLAUDE_SKILL_DIR}/tools/measure.py`), and the screen sizes to check (default, minimum, and dark).

## Step 3: Build the shell and kit before any screen

- Implement the shell and kit, then one proof screen (the busiest dashboard).
- Screenshot it and measure R9 with the tool. Show the user the image and the counts.
- Only then build other screens, each strictly from the kit.
- **Platform pitfalls** are in RULES.md. Above all: on macOS 26, don't use the system split view for the shell.

## Step 4: Keep it calm as it grows

Every new screen or feature PR answers four questions:

1. Which page template does it use?
2. What are its R9 counts?
3. Does it add any new box, pill, filled button or saturated colour?
4. If so, which rule allows it?

A new component goes into the kit first, never inline. When a screen needs a second action, it's a text action. When a list appears, it's a `ListSection`, not a card.

## Smells to block in review

- **Wrapping:** a card around a list; a bordered button in a row.
- **Decoration:** pills; gradients or glows; uppercase eyebrows; emoji or "!!".
- **Hierarchy:** two filled buttons; a fourth surface level.
- **Alignment:** a second left edge without a master/detail reason; mixed row heights in navigation.
- **Content:** a greeting headline; invented comparisons on metrics.
