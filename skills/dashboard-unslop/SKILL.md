---
name: dashboard-unslop
description: Redesign an existing "vibecoded" or cluttered dashboard or app UI into a calm, structured one by measuring it, diffing it against measured rules, and rebuilding its structure before its colour. Use when given a busy dashboard, screenshots of one, or a before/after reference to learn from, with requests like "unslop this", "this looks AI-generated", "too many cards", "make it like this reference".
---

# Unslop a dashboard

Turn a cluttered UI into a calm one deterministically:

1. Measure it.
2. Compare it with numbers.
3. Change structure first.
4. Re-measure.

The rules live in `RULES.md` next to this file. The measuring tool is `${CLAUDE_SKILL_DIR}/tools/measure.py` (pure Python 3, no dependencies, any OS), with a macOS-native twin in `tools/measure.swift`.

**The lesson that cost a full round once:** recolouring a cluttered UI changes almost nothing visible. The clutter is **structure**:

- boxes inside boxes;
- a bordered button on every row;
- pills;
- a floating sidebar;
- many left edges.

Do the structural pass (phases 3–4) before any colour or type work.

## Phase 0: Gather

- **Get screenshots** of every main screen at one size (for example 1440×900), plus dark mode and the minimum window size. With app code, use the app's own screenshot harness. Never drive a user's live or production app to get them.
- **Reference input:** if the user supplies a reference (images, a video, a before/after), extract frames from a video with `ffmpeg -ss <t> -i video -frames:v 1 out.png`, then make a contact sheet (`fps=2,scale=480:-1,tile=4x5`).
- **Ask only** which decisions are genuinely the user's to make: sidebar treatment, brand-colour texture, default appearance, mono metadata. Recommend defaults from RULES.md.

## Phase 1: Measure (never eyeball)

Run `python3 "${CLAUDE_SKILL_DIR}/tools/measure.py" IMG <mode> …` (PNG input; convert other formats with ffmpeg first). On macOS you can instead build the faster Swift twin once, with `swiftc -O "${CLAUDE_SKILL_DIR}/tools/measure.swift" -o /tmp/measure`, which also reads JPEG and WebP. The modes are listed in the file header:

| Mode | Gives you |
|---|---|
| `color` | a colour at a point |
| `peak` | text colour on a background |
| `scan h\|v` | every edge along a line: box edges, hairlines, radii |
| `ink` | bounding box plus rows and columns: text size, row pitch, left edges |
| `mode` | a surface fill |

Steps:

1. Overlay a 100 px grid so you can choose clean measuring lines: `ffmpeg -i in.png -vf "drawgrid=w=100:h=100:t=1:c=red@0.55" grid.png`.
2. **Fix the scale.** Find a known element (a nav row is usually 32–36 pt; body text is 13–14 pt with a cap height ≈ 0.7 em) and derive px per pt. Convert everything to points.
3. **Fill in `templates/inventory.md`**, one row per element: surfaces, navigation (logo, search, every row, label columns, counts, groups), header, title, every card (size, gap, padding, label/value/delta sizes and colours), buttons, charts.
4. **Count the acceptance metrics** (RULES.md R9) for each screen: boxes, pills, filled or bordered buttons, nesting depth, left edges, row pitches and saturated elements. Use `scan` along a few horizontal and vertical lines to confirm box edges.

If there's a reference before/after, measure **both** its frames and the target app the same way. The diff between the reference's before and after is the lesson. The diff between the target app and the reference's after is the work.

## Phase 2: Diagnose

Write the diagnosis as a table: element, measured, rule, verdict. Name the **cause** of each violation, not just the symptom. For example: "floating sidebar = the system split view's glass style; restyling can't fix it."

Show the user the numbers, for example "Home: 19 boxes, 3 pills, 8 bordered buttons, nesting 4 → targets 8/0/1/2". This is what makes the change verifiable.

## Phase 3: Template

Turn RULES.md into the target app's concrete tokens and components:

- **Surfaces and type:** the surface levels, the ink ramp and the type scale.
- **Shell geometry:** navigation width, header height, icon and label columns, row pitch, content inset.
- **Kit components:**
  - `PageScaffold` / `PageTitle` (title, two-tone tail, grey line, one trailing primary);
  - `ListSection` (heading, mono count, hairline, rows: **no box**);
  - `ListRow` (the whole row is the button; trailing value, action word and chevron);
  - `MetricTile` (label, value, optional honest delta);
  - `Primary` (the only filled button);
  - `TextAction` (no resting chrome);
  - `StatusLine` (dot and words);
  - `FilterWords` (plain words, chosen on a soft square).
- **Box budget:** what may be boxed (R2), written into the plan.
- **Worked example:** the busiest screen, mapped box by box from "today" to "template".

Save it as the project's plan document. **Don't overwrite earlier plans**; supersede them by reference.

## Phase 4: Rebuild structure (in this order)

1. **Shell.** Make the navigation flush, add the hairline and the shared header line, and remove toolbar chrome. Search goes in the navigation column. Rows: 32 pitch, icon at 24, label at 50.
2. **Kit.** Strip resting chrome from every non-primary button style. Remove capsule backgrounds from chips and badges. Unbox empty states and hero call-outs. Add `ListSection` and `ListRow`.
3. **One proof screen** (the busiest). Rebuild it by hand, screenshot it, measure it against R9, and show the user before fanning out.
4. **All screens.** With many files, use parallel builders, each owning **distinct files**, each with its own build directory, and each with the same brief. The brief covers:
   - the rules;
   - the kit API;
   - converting panels that hold lists into `ListSection`;
   - turning row buttons into the row itself;
   - one primary per screen;
   - no pills;
   - no boxes in boxes;
   - one left edge;
   - keeping every callback, identifier and string meaning;
   - reporting the R9 counts before and after.

   **Builders must launch the app only through the isolated screenshot script**, never directly.
5. **Then colour and type** (R4, R5): the colour budget, the regular-weight title, mono meta, and no caps eyebrows.

## Phase 5: Verify

- **Re-measure** with the tool on the final build. Report the R9 counts per screen, before → after, plus the navigation pitch and columns.
- **Run the project's own checks and gates.** Builds alone aren't proof.
- **List the honest exceptions:** second columns in master/detail views, native tables, system forms.
- **Evidence:** before and after screenshots and the counts table go in the project's evidence folder.

## Anti-patterns to search for in code first

- **Fills and decoration:** capsule or `rounded-full` backgrounds; gradient fills; glows and shadows on resting elements.
- **Cards and buttons:** `Card`/`Panel` wrapping a `ForEach`/`map` of rows; bordered buttons inside list rows.
- **Text:** uppercase plus tracking labels; emoji in UI strings; "!!".
- **Navigation:** a sidebar or toolbar provided by a system component that floats; different row heights in one navigation group.
- **Greetings:** "Welcome back, X!" headlines.
