# Electric Machinery Fundamentals — Interactive Course

A single-page, fully client-side course website built around Chapman's *Electric Machinery Fundamentals* (4th ed.):
eight chapters of live simulations, animated phasor diagrams, step-by-step derivations and worked examples.

**Author:** Dr. Muhammad Salim Butt · University of Engineering & Technology · salimbutt@uet.edu.pk

## Live site

Deployed with GitHub Pages — the homepage is `index.html` at the repository root.

## Project structure

```
index.html            ← the complete single-page site (generated — do not edit by hand)
chapters/
  chapter0.html       ← Introduction: AC systems & reactive components
  chapter1.html       ← Chapter 1: Introduction to machinery principles
  chapter2.html       ← Chapter 2: Transformers
  chapter3.html       ← Chapter 3: AC machinery fundamentals
  chapter4.html       ← Chapter 4: Synchronous machines
  chapter5.html       ← Chapter 5: Induction motors
  chapter6.html       ← Chapter 6: DC machines
  chapter7.html       ← Chapter 7: Single-phase & special motors
build.py              ← regenerates index.html from chapters/
.nojekyll             ← tells GitHub Pages to serve the files exactly as they are
```

Each file in `chapters/` is a complete, self-contained interactive app (its own styles, scripts and
section navigation) and also works stand-alone — the site links to them with "Open full screen ↗".

## How `index.html` is assembled

`index.html` contains **every chapter in full**: `build.py` copies each `chapters/chapterN.html`
verbatim into an inert `<template>` inside `index.html` and the page renders it in its own isolated
frame within a `<section id="chapterN">`. This is what lets eight independent apps — which share
helper names, element ids and section ids — live on one page without interfering with each other,
while preserving all of their behaviour exactly. The shell adds:

- a fixed navigation bar (collapsible on mobile) with smooth scrolling,
- a landing section, chapter cards and a complete table of contents that deep-links to individual
  topics inside each chapter,
- a "Back to top" button, lazy loading of chapters as you scroll, and "Reset chapter".

## Editing content

1. Edit the relevant `chapters/chapterN.html`.
2. Run `python build.py` (Python 3, no dependencies).
3. Commit both the chapter file and the regenerated `index.html`.

## Deploying to GitHub Pages

1. Push the repository to GitHub.
2. *Settings → Pages → Build and deployment*: Source **Deploy from a branch**, branch **main**, folder **/ (root)**.
3. The site appears at `https://<user>.github.io/<repo>/`. No build step is required on GitHub.

## Licence

Teaching material © Dr. Muhammad Salim Butt. Figures, derivations and simulations are original;
equation numbers follow Chapman's text for ease of cross-reference.
