# How it works: the teardown behind the rules

The rules weren't written from taste. They come from measuring, pixel by pixel, a well-known kind of redesign: a "vibecoded" dashboard turned into a calm one. The redesign kept the same content and numbers, but changed the structure, colour, type and spacing. This page explains what was measured and why the method is built the way it is.

## The eight moves (in the order that works)

1. **Fix the rhythm.**
   - Before: sidebar gaps measured 26, 44, 46, 30 and 38 px, with no system.
   - After: one scale. Rows sit on an exact 32-pt pitch with no gaps.
2. **Share one left edge.**
   - Before: label columns drifted by 4 pt from row to row.
   - After: every icon starts on one column and every label on another.
3. **Take the colour out.**
   - Before: gradient backdrop, gradient headline, gradient selected row, red badge pills, violet count pills, glowing bars.
   - After: neutral greys. Colour survives only where it means something: data series, status dots, a positive delta.
4. **One icon language.**
   - Before: 23 emoji.
   - After: thin monochrome line icons; the selected row gets the filled variant. Category emoji became small coloured dots.
5. **Calm the words.**
   - Before: "Welcome back, <name>! 👋", "+12%!!", "NAVIGATION".
   - After: "October 2026", "+12% vs last month", "Navigation". Sentence case, no exclamation marks, and every number gets a comparison that gives it meaning.
6. **Hierarchy from weight and grey, not hue.**
   - The title becomes large and regular weight, with a two-tone grey tail.
   - Values are semibold; labels are regular grey.
   - Metadata is small monospaced grey.
7. **Quieter containers.**
   - Before: glassy panels with glowing borders.
   - After: flat surfaces one step lighter than the page, with 1 px borders.
   - The sidebar stops being a separate card: it becomes a column of the window, behind a hairline.
8. **Honest data visuals.**
   - Before: fat rounded gradient bars without axes.
   - After: thin lines, labelled axes, one colour per series.

## The counts that matter

| | Boxed shapes | Pills | Nesting depth | Left edges | Emoji |
|---|---|---|---|---|---|
| Before | 17 | 9 | 3 | 3 | 23 |
| After | **9** | **0** | **2** | **1** | 0 |

Information density barely changes: same items, same numbers. What changes is where the eye goes. It goes to numbers, status and the current place, instead of bouncing between decorations.

## The mistake the method is built to prevent

The obvious first attempt is to recolour everything: neutral greys, one accent, calmer type. We did exactly that on a real app, and the result was judged as looking "like nothing changed".

Measured, the screen still had 19 boxed shapes, 3 pills, 8 bordered buttons and nesting four levels deep:

- a floating sidebar card;
- toolbar pills;
- every section in a panel;
- a bordered button on every row.

Recolouring changed none of those.

That's why both skills:

1. **measure** before changing anything, so the problem is a number and not an impression;
2. **change structure before colour**: shell, kit, one proof screen, then every screen, and only then colour and type;
3. **accept a screen by counts** (R9 in `RULES.md`), not by eye.

After the structural pass, the same screens measured 3–7 boxes, 0 pills, at most 1 filled button, nesting 2 and one left edge. Then the redesign finally looked different.

## The measuring tool

`tools/measure.py` is about 200 lines of dependency-free Python. It reads a PNG and answers five questions precisely:

| Question | Command |
|---|---|
| What colour is this surface? | `mode` |
| What colour is this text? | `peak` |
| Where are the edges along this line? (boxes, hairlines, radii) | `scan` |
| What's the bounding box, row pitch and left edge of this region? | `ink` |
| What colour is this exact point? | `color` |

To turn pixels into design units, find one known element (a navigation row is usually 32–36 pt; body text has a cap height of about 0.7 × its size), derive the scale, and convert everything to points.
