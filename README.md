# deslopdashboard

**Make dashboards calm by measuring them, not by vibes.**

Two [Claude](https://claude.com) skills for anyone building a dashboard, admin panel, SaaS app or desktop app UI:

| Skill | Use it when | What it does |
|---|---|---|
| **`dashboard-unslop`** | You have a cluttered, "AI-looking", vibecoded UI, or a before/after reference you want to learn from | Measures every element, diagnoses it with numbers, writes a template, then rebuilds the **structure first** and the colour last. Re-measures to prove the change. |
| **`dashboard-blueprint`** | You're starting a new dashboard or app | Writes a complete UI rule structure up front (shell, surfaces, type, components, page templates, box and colour budgets), so the app starts calm. |

Both share one set of measured rules ([`RULES.md`](skills/dashboard-unslop/RULES.md)) and a small measuring tool ([`measure.py`](skills/dashboard-unslop/tools/measure.py): pure Python, no dependencies, any OS).

## Why this exists

The usual way to "clean up" a cluttered dashboard is to recolour it. **It doesn't work.** A recoloured UI still has the same boxes inside boxes, pills, floating panels and a bordered button on every row, and people see no difference.

These skills come from a real redesign that went through exactly that failure. A teardown of a calm dashboard was then measured pixel by pixel, and its structure rebuilt. The structural pass is what changed the result:

| One screen, measured | Boxed shapes | Pills | Filled/bordered buttons | Nesting | Left edges |
|---|---|---|---|---|---|
| Before | 19 | 3 | 8 | 4 | 3 |
| After the structure pass | 5 | 0 | 0 | 2 | 1 |

The full story is in [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md).

## Install

Pick **one** of these.

### 1. Claude Code, as a plugin (recommended)

In any Claude Code session:

```text
/plugin marketplace add jakem921/deslopdashboard
/plugin install deslopdashboard@deslopdashboard
```

Or from your shell:

```bash
claude plugin marketplace add jakem921/deslopdashboard
claude plugin install deslopdashboard@deslopdashboard
```

Then use `/deslopdashboard:dashboard-unslop` or `/deslopdashboard:dashboard-blueprint`, or just describe what you want; see [Use](#use).

### 2. Claude Code, copy the skills (personal, every project)

```bash
git clone https://github.com/jakem921/deslopdashboard.git
mkdir -p ~/.claude/skills
cp -R deslopdashboard/skills/dashboard-unslop deslopdashboard/skills/dashboard-blueprint ~/.claude/skills/
```

Invoke them as `/dashboard-unslop` and `/dashboard-blueprint`.

### 3. Claude Code, one project only (shared with your team through git)

From your project's root:

```bash
mkdir -p .claude/skills
cp -R /path/to/deslopdashboard/skills/dashboard-* .claude/skills/
git add .claude/skills && git commit -m "Add dashboard design skills"
```

### 4. Claude.ai and the Claude desktop or mobile apps

Two ways:

- **Whole plugin.** Open **Customize → Plugins → Add → Add marketplace** and enter `jakem921/deslopdashboard`.
- **Single skills.** Build upload-ready zips, then upload each one under **Customize → Skills**:

  ```bash
  ./scripts/package-for-claude-ai.sh
  # creates dist/dashboard-unslop.zip and dist/dashboard-blueprint.zip
  ```

  Skills in the apps need a plan with code execution enabled. Menu names can change, so check Claude's help centre if you can't find them.

## Use

You don't need to name the skill; describe the job:

> Unslop this dashboard. Here are screenshots of every screen.

> This admin panel looks AI-generated. Too many cards and pills. Fix it.

> Here's a before/after reference I like. Learn its rules and apply them to my app.

> I'm starting a new SaaS dashboard in Next.js. Set up a dashboard blueprint first.

**What happens with `dashboard-unslop`:**

1. **Gather.** Claude asks for screenshots, or takes them itself if it can run your app, plus any reference images or video. It asks only the few design decisions that are yours to make.
2. **Measure.** Every element goes into an inventory: surfaces, navigation rows and columns, cards, buttons, type. It also counts boxes, pills, buttons, nesting depth and left edges per screen.
3. **Diagnose.** A table of measured value → rule → verdict, naming the *cause* of each problem.
4. **Template.** Your app's own tokens and kit components, plus a worked example of your busiest screen.
5. **Rebuild, structure first.** The order is shell, kit, one proof screen (shown to you), all screens, then colour and type.
6. **Verify.** Re-measure every screen against the targets and run your project's own checks.

**What happens with `dashboard-blueprint`:** Claude asks a handful of decisions, each with a recommended default. It fills in [a UI spec template](skills/dashboard-blueprint/template.md), builds the shell and kit before any screen, proves one screen by measurement, and sets review rules so new screens stay calm.

## The rules in one minute

From [`RULES.md`](skills/dashboard-unslop/RULES.md):

- **Three surface levels:** navigation, canvas, card. The sidebar is a column of the window, not a floating card.
- **Box budget:** only metric tiles, one chart or preview, inputs, the selected nav row, the primary button and floating layers are boxed. Lists are hairline rows on the canvas, and **the row is the button**.
- **One filled button per screen.** Every other action is text.
- **No pills.** Counts are mono grey text; states are a dot plus words.
- **Colour only for meaning:** the primary action, status, data and the brand mark.
- **Type:** a regular-weight title with a grey tail, mono metadata, no caps eyebrows, no emoji, no "Welcome back!".
- **Geometry:** one left edge; 32 pt nav rows (icon column 24, label column 50); 32 pt between sections.
- **Accept a screen by numbers:**
  - ≤ 8 boxes;
  - 0 pills;
  - ≤ 1 filled button;
  - nesting ≤ 2;
  - 1 left edge.

Platform notes cover SwiftUI (including macOS 26's floating sidebar) and web/Tailwind.

## The measuring tool on its own

```bash
python3 skills/dashboard-unslop/tools/measure.py screenshot.png size
python3 skills/dashboard-unslop/tools/measure.py screenshot.png scan h 400 0 1440   # every edge along y=400
python3 skills/dashboard-unslop/tools/measure.py screenshot.png ink 20 100 260 700   # row pitch and left edges in the nav
python3 skills/dashboard-unslop/tools/measure.py screenshot.png peak 300 80 600 110  # text colour
```

It reads PNG; convert other formats with `ffmpeg -i in.webp out.png`. On macOS, `tools/measure.swift` is a faster twin that also reads JPEG and WebP.

## Using it with other AI coding tools

The skills are plain Markdown plus one Python script. With Cursor, Codex, Windsurf or similar, add `skills/dashboard-unslop/RULES.md` to your project rules and point the agent at `SKILL.md` as the procedure.

## Contributing

Issues and PRs are welcome, especially:

- platform notes for more stacks (Flutter, Android, Electron);
- more measured before/after case studies, as numbers rather than copyrighted images.

Keep the skills self-contained: each skill folder must work on its own. `RULES.md` and `tools/` are duplicated on purpose, so edit both copies.

## License

[MIT](LICENSE)
