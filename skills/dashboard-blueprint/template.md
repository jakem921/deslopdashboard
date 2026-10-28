# <Product> UI blueprint

Status: <date>. This is the controlling UI spec. Rules: `RULES.md` (R1–R9), shipped with the dashboard-blueprint skill.

## Decisions

| Decision | Choice | Default if unanswered |
|---|---|---|
| Appearance | | light and dark, both designed |
| Brand hue | | |
| Navigation treatment | | recessive column, flush, hairline |
| Canvas texture | | none |
| Mono metadata | | yes |
| Audience | | |

## 1. Shell

| Item | Value |
|---|---|
| Root layout | nav column \| 1 px hairline \| content (no floating sidebar, no toolbar chrome) |
| Navigation width | 244 |
| Header line | 44 tall, shared; contents: |
| Search | in the navigation column under the logo, 32 tall, inset 12 |
| Navigation rows | 32 pitch; icon at 24; label at 50; counts right at 24 from the hairline |
| Groups | full-width hairline, mono label 24 below, rows |
| Content | left edge 28 from the hairline; max width ____ |

## 2. Surfaces

| Level | Light | Dark |
|---|---|---|
| Navigation | | |
| Canvas | | |
| Card (+1 step, 1 px border, radius 8–10) | | |
| Hairline, strong / soft | | |
| Ink 1 / 2 / 3 | | |

## 3. Type

| Role | Font, size, weight | Colour |
|---|---|---|
| Page title (+ grey tail) | | |
| Section title | | |
| Row title / body | | |
| Detail / label | | |
| Card value | | |
| Mono meta | | |

## 4. Colour budget

| Saturated may be | Neutral must be |
|---|---|
| primary action, status dots, data, brand mark | selection, tabs, links, icons, secondary actions, counts, switches |

## 5. Kit

| Component | API | Rules |
|---|---|---|
| PageScaffold / PageTitle | | one trailing primary |
| ListSection | | never boxed |
| ListRow | | whole row is the button |
| MetricTile | | honest delta only |
| Panel | | charts, previews, tiles only |
| Primary | | the only filled button, 28 tall |
| TextAction | | no resting chrome |
| StatusLine | | dot and words |
| FilterWords | | no pills |
| EmptyState | | unboxed |
| Sheet | | Cancel text plus one primary |

## 6. Page templates

| Template | Structure | Screens using it |
|---|---|---|
| Dashboard | | |
| List | | |
| Master/detail | | |
| Settings | | |
| Wizard | | |
| Empty / intro | | |

## 7. Box budget

| Allowed boxes in this product | Never boxed |
|---|---|
| | |

## 8. Acceptance (per screen, measured)

| Metric | Target |
|---|---|
| Boxes | ≤ 8 |
| Pills | 0 |
| Filled / bordered buttons | ≤ 1 |
| Nesting | ≤ 2 |
| Left edges | 1 (2 for master/detail) |
| Navigation pitch | 32 |
| Saturated elements | ≤ 3 |

- **Sizes checked:** default ____, minimum ____, dark.
- **Tool:** `python3 "${CLAUDE_SKILL_DIR}/tools/measure.py" IMG <mode> …`
