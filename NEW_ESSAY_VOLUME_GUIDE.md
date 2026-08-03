# Future-Agent Manual: Adding a New Essay or Volume

This document is the operating manual for extending the Faith essay library with a new long-form essay or volume.

It is written for an agent who has been handed a new essay and needs to turn it into a finished reader experience that belongs beside Goodness and Resurrection. The goal is not merely to make the Markdown render. The goal is to make the argument feel authored as a visual book: readable, paced, navigable, beautiful, and faithful to the canonical source.

The intended input is deliberately simple: a future agent should be able to receive only the complete new essay and produce the rest of the volume from it. The agent should not require the user to provide a slug, chapter map, quote list, image list, CSS plan, or manifest. Those are implementation outputs that the agent should derive from the essay and the existing site.

The project has three layers:

1. **Canonical source**: the complete essay in `content/<slug>/essay.md`, including any source material needed for later auditing.
2. **Editorial configuration**: `content/<slug>/manifest.json`, which tells the renderer where and how to place images, pulls, diagrams, and other visual interventions.
3. **Published reader**: generated HTML and copied assets, produced by `build.py` and styled by `style.css`.

Treat those layers differently. The Markdown is the authority for the essay. The manifest is the authority for visual placement. The generated HTML is an output and should not become a second hand-edited source of truth.

## 0. Essay-only autopilot: the shortest reliable path

This is the primary procedure. Use it when the user gives the agent a full essay and asks for a new illustrated volume.

### Input contract

The user may provide any of the following:

- a Markdown file;
- pasted Markdown;
- a plain-text essay;
- a document whose text can be extracted;
- an essay plus an optional title or desired title.

The minimum required input is the complete essay text. In practice, the supplied `.md` may be a complete source package rather than a bare manuscript. It may contain the essay followed by research notes and a website handoff with chapter titles, visual ideas, glossary entries, biographies, objection-card passages, pull quotations, and visual atmosphere. The agent must use those sections as structured implementation input instead of treating the whole file as reader-facing prose.

If the essay has no obvious title, derive a provisional title from its first meaningful heading or opening thesis and record that assumption. If the user has supplied a title, use it exactly for reader-facing display unless it conflicts with an existing volume.

### Source-package interpretation

When the input contains notes after the essay, divide it into three conceptual layers immediately:

| Layer | Typical labels in the input | How to use it | Public-reader treatment |
| --- | --- | --- | --- |
| Reader manuscript | Title, chapters, section headings, paragraphs, quotations, conclusion | Preserve as the canonical essay and render in order | Visible, unless an explicit reader-only exclusion applies |
| Evidence notebook | `Sources and Notes`, numbered research notes, `Principal theological and philosophical works`, `Sacred Scripture` | Use for factual grounding, attribution, nuance, and verification | Hidden from the reader; never render as an appendix by accident |
| Website handoff | `Website Handoff`, `Chapter titles`, `Visual ideas`, `Glossary`, `Thinkers needing short biographies`, `Strongest objection-card passages`, `Possible pull quotations`, `Visual atmosphere` | Use as the design and editorial implementation brief | Hidden as a handoff document, except that selected glossary/bio material becomes contextual UI and selected quotes become reader-facing pulls/cards |

The supplied file is therefore both content and production specification. Do not throw away the notes after extracting them, and do not render them wholesale.

### Source-package parsing procedure

Run this procedure before creating the new volume:

1. Preserve the supplied input unchanged in the working context. If the repository supports an archive or source-input file, retain a verbatim copy there; if not, preserve the original sections in the canonical source with deterministic reader exclusions.
2. Find the boundary between the reader manuscript and the source package. Usually this is the first `Sources and Notes` label, but use the actual structure rather than assuming a fixed line number.
3. Identify the `Website Handoff` boundary and every subsection beneath it.
4. Convert informal labels into an internal inventory. The example may use plain labels rather than Markdown headings, so do not rely only on heading syntax.
5. Extract each subsection into a structured working table before implementation.
6. Keep research notes and handoff material out of the reader projection.
7. Use the handoff to accelerate implementation, but compare it against the actual essay before making assumptions about placement or emphasis.

Useful discovery search:

```bash
rg -n "Sources and Notes|Website Handoff|Chapter titles|Visual ideas|Glossary|Thinkers needing short biographies|Strongest objection-card passages|Possible pull quotations|Visual atmosphere" <input>.md
```

If labels are not exact, identify equivalent sections by their content and position. A future input may say `Research`, `Design Notes`, `Key Terms`, `People`, `Pulls`, or `Art Direction` instead.

### Conflict-resolution order

When the essay and the handoff do not line up perfectly, use this priority order:

1. Explicit current user instructions.
2. The essay's actual wording and intended reader-facing argument.
3. The supplied website handoff's structural and visual instructions.
4. Source notes and cited works as factual/contextual support.
5. Existing site conventions and this guide's defaults.

Do not silently rewrite the essay to match a handoff label. If a handoff proposes eight chapters but the manuscript clearly has seven movements, preserve the manuscript's logic and map the handoff titles to it where possible. Record the mismatch and the chosen mapping.


### Agent output contract

The agent must produce all of the following without requiring the user to specify each one:

1. A permanent URL slug.
2. A complete source file at `content/<slug>/essay.md`.
3. A volume manifest at `content/<slug>/manifest.json`.
4. A volume-specific asset directory at `assets/<slug>/`.
5. A root landing card.
6. A volume route at `/<slug>/index.html`.
7. A tab in the shared volume switcher.
8. A chapter rail derived from the essay's structure.
9. A coherent visual art direction inferred from the essay.
10. A set of illustrations, diagrams, pulls, and shaded breaks placed at meaningful argumentative turns.
11. Floating definitions for important terms and compact biographies for important people, following the Goodness reader pattern.
12. Responsive and accessible presentation for the new visual elements and contextual notes.
13. A rebuilt site with existing volumes preserved.
14. A committed and pushed GitHub change containing the completed volume.
15. A concise handoff describing assumptions, files, commit, branch, push result, and any limitations.

### Agent decision defaults

Unless the user says otherwise, use these defaults:

| Decision | Default |
| --- | --- |
| Slug | Lowercase hyphenated form of the title, made permanent before implementation |
| Visual style | The existing Goodness editorial language, adapted to the new essay's subject and emotional temperature |
| Image art direction | Surrealist oil-painting language inspired by Rene Magritte: lucid impossible juxtapositions, quiet symbolic objects, theatrical skies, soft dream logic, and mystical luminous atmosphere |
| Image count | At least one opening composition, one closing composition, and one meaningful visual intervention per major argumentative movement; reduce the count when the essay is short |
| Illustration mix | Mostly atmospheric/conceptual illustrations, supplemented by diagrams when the essay explains a sequence, comparison, hierarchy, or evidence structure |
| Pull quote count | A selective set of the strongest independent sentences, not every quotable sentence |
| Shaded sections | Used to mark changes in argumentative function, not inserted at mechanical intervals |
| Contextual notes | Add a floating definition for important terms and a short bio for important people at their first meaningful use |
| Typography | Preserve the existing reader system; create a volume-specific palette before replacing shared type rules |
| Internal notes | Keep in canonical source only when useful, then exclude them structurally from public output |
| Missing image tool | Use code-native diagrams, CSS compositions, or existing assets rather than blocking the volume |
| Ambiguity | Make the least destructive assumption, record it, and continue |
| GitHub publication | Commit the complete scoped change and push the active branch; never claim completion if the push did not succeed |

### Eight-pass autopilot workflow

Run these passes in order. Do not bounce randomly between content, CSS, and assets.

#### Pass 1: ingest

1. Identify the complete essay input.
2. Confirm that it is complete enough to publish; if it ends abruptly, preserve it and note the limitation rather than inventing an ending.
3. Extract or preserve the title, headings, paragraphs, quotations, lists, and notes.
4. Create `content/<slug>/essay.md` without summarizing the essay.

#### Pass 2: understand

1. Read the essay from beginning to end.
2. Identify the central question, central claim, major movements, tensions, objections, evidence, images, and conclusion.
3. Make a chapter map with one sentence per major unit.
4. Mark passages that can become pulls, pressure cards, answer cards, diagrams, or illustrations.
5. Identify important terms, doctrines, places, institutions, authors, historical figures, and other people who deserve a floating definition or short bio.
6. Parse any `Sources and Notes` section into evidence notes and named works.
7. Parse any `Website Handoff` section into chapter titles, visual ideas, glossary entries, biographies, objection cards, pull candidates, and atmosphere guidance.
8. Map each handoff item to an essay section, or mark it as unresolved instead of silently dropping it.
9. Mark all material that is source-only and must not reach the reader.

#### Pass 3: establish the volume identity

1. Choose the slug.
2. Choose a short theme name.
3. Choose a restrained palette based on the essay's subject.
4. Choose a visual vocabulary: stone, paper, water, night, glass, architecture, landscape, linework, archival fragments, or another coherent family.
5. Write a one-sentence art direction that can guide every image. Unless the essay clearly demands another direction, use the house image language: Magritte-inspired surrealist oil painting blended with mystical, beautiful, dreamy imagery.

#### Pass 4: wire the library

1. Register the volume in `build.py`.
2. Add the root card metadata.
3. Add the volume tab.
4. Add the route to generation.
5. Add scoped reader exclusions if required.
6. Keep every existing volume route and tab intact.

#### Pass 5: author the visual plan

1. Assign a visual role to each major essay movement.
2. Select the strongest pull quote candidates.
3. Decide which concepts need diagrams instead of images.
4. Decide where shaded background breaks should reset the reading rhythm.
5. Design the contextual-note set: terms, people, definition text, bio text, and first-use anchors.
6. Give each visual and contextual note a stable ID before creating its asset or markup.

#### Pass 6: make the assets

1. Create the hero or opening composition.
2. Create the major illustrations and diagrams.
3. Create the closing composition.
4. Keep filenames descriptive and stable.
5. Add alt text and captions while the visual's meaning is still fresh.

#### Pass 7: assemble and build

1. Add manifest entries and placements.
2. Add custom renderer branches only where needed.
3. Add CSS for visual classes and responsive states.
4. Run `python3 build.py`.
5. Inspect the generated route, root card, tabs, and representative visual sections.

#### Pass 8: polish and hand off

1. Read the generated volume as a continuous essay.
2. Remove visible AI/process language.
3. Fix weak, repetitive, or unrelated visual treatments.
4. Check narrow-width behavior and accessibility.
5. Confirm existing volumes still work.
6. Commit the scoped changes and push them to GitHub.
7. Write the handoff summary with the commit and push result.

### Copy-paste brief for a future agent

When delegating this work, the user should be able to use a brief as short as this:

```text
Use the complete essay I provided as the only content input. Add it as a new full volume to the Faith essay library. Infer the permanent slug, chapter structure, visual art direction, pull quotes, pressure/answer moments, shaded reading breaks, floating definitions, short biographies, illustrations, diagrams, responsive behavior, accessibility text, manifest, assets, root card, tab, and route from the essay and the existing Goodness/Resurrection implementation. For raster imagery, use the house direction of lucid Magritte-inspired surrealist oil painting blended with mystical, beautiful, dreamy symbolism, adapted to the essay's actual ideas. Preserve the essay in full, keep internal production language out of the public reader, preserve all existing volumes and links, build the site, commit the scoped changes, push them to GitHub, and report the files changed, commit, branch, push result, and assumptions.
```

Add this sentence when the contextual layer needs to be explicit:

```text
Also identify important terms and people in the essay and add Goodness-style floating definitions and short bios at their first meaningful appearances, with accessible mobile and keyboard behavior.
```

The rest of this guide explains how to execute that brief correctly and what to do when the essay requires a judgment call.

## 1. Definition of done

A new volume is complete only when all of the following are true.

### Content

- The complete essay is present in `content/<slug>/essay.md`.
- The original order, wording, headings, quotations, and paragraph boundaries are preserved unless the user explicitly authorizes editorial changes.
- Every major section is identifiable as a chapter or meaningful reading unit.
- Reader-only process notes, drafting instructions, audit notes, and AI/pipeline language do not appear in the public reader.
- The text has been checked for accidental truncation, duplicated passages, broken headings, and malformed Markdown.

### Navigation

- The volume has a stable URL at `/<slug>/index.html`.
- The root page links to the new volume.
- The shared volume switcher can move between every published volume without losing the current reading context unexpectedly.
- The chapter rail contains useful labels, fits at the intended width, and points to real anchors.
- Existing Goodness and Resurrection links still work.

### Visual composition

- The new essay has a cover or opening composition appropriate to its argument.
- Long stretches of prose are broken up with a deliberate rhythm of shaded sections, support pulls, diagrams, illustrations, or other visual pauses.
- Important quotations are surfaced as pull quotes without turning every paragraph into a callout.
- Illustrations are conceptually tied to the essay rather than used as decoration with no relationship to the text.
- Pressure points, objections, transitions, and answers have distinct visual treatment where the argument benefits from it.
- No visual overflows horizontally on a narrow viewport.

### Technical quality

- `python3 build.py` completes successfully.
- The build emits the new route and updates the expected generated artifacts.
- Every manifest-referenced asset exists at the expected path.
- The integrity report is generated or updated according to the repository's existing behavior.
- Images have useful alt text and decorative images are explicitly marked as decorative where supported.
- Public HTML contains no visible process language that makes the site feel like an internal AI-generated draft.

### Handoff

- The work is described by file and purpose.
- New visual IDs and assets are documented well enough for a future agent to find them.
- Any intentional assumptions, unresolved visual decisions, or known limitations are recorded.

Do not call the task finished merely because the page loads. A page can load while the essay is incomplete, the tab route is broken, the manifest is ignored, or the visual rhythm is poor.

## 2. Project architecture

Before changing anything, understand the path a piece of content takes through the system.

```text
content/<slug>/essay.md
        |
        | Markdown parsing, reader filtering, chapter detection,
        | cards, support pulls, and integrity accounting
        v
build.py
        |
        | visual manifest data     | shared reader shell and routes
        v                         v
content/<slug>/manifest.json     generated HTML
        |                         |
        v                         v
assets/<slug>/*              style.css + browser assets
        |
        v
published visual reader at /<slug>/index.html
```

The principal files are:

| File or directory | Responsibility | Edit policy |
| --- | --- | --- |
| `build.py` | Discovers volumes, parses Markdown, filters reader-only material, renders HTML, emits routes and reports | Edit when adding a route, volume metadata, filtering rule, or renderer behavior |
| `style.css` | Shared visual language, layout, responsive behavior, cards, rails, diagrams, and image treatment | Edit when adding a visual class or tuning a shared component |
| `src/visuals.py` | Code-native diagrams and visual render branches | Edit only when the visual cannot be represented by an existing kind |
| `content/<slug>/essay.md` | Canonical essay text | Add the full source; do not replace it with a summary |
| `content/<slug>/manifest.json` | Visual placements and volume-specific visual data | Add stable IDs and intentional placements |
| `assets/<slug>/` | Volume-specific raster/vector assets | Keep names stable and descriptive |
| `index.html` | Generated root landing page | Do not hand-edit; regenerate |
| `<slug>/index.html` | Generated volume reader page | Do not hand-edit; regenerate |
| `reports/` | Generated integrity or build reports | Regenerate through the build process |

The existing Goodness and Resurrection implementations are references, not templates to copy blindly. Goodness establishes the visual language. Resurrection demonstrates how a full essay can receive denser visual editorial treatment, including cards, shaded breaks, illustrations, and custom diagrams.

## 3. First response to a new essay

When a new essay arrives, do not begin by writing CSS. First make an inventory of the material and of the existing system.

### 3.1 Gather the intake information

Record the following before implementation:

- Working title.
- Final title, if known.
- Author or attribution line, if the site displays one.
- Intended URL slug.
- Whether the essay is a standalone essay, a volume in a series, or a companion to an existing volume.
- Whether the essay includes an introduction, preface, conclusion, appendices, notes, or bibliography.
- Whether quotations are original, cited, paraphrased, or unattributed.
- Whether source material includes internal drafting notes or production instructions that must remain canonical but hidden from readers.
- Desired tone: contemplative, argumentative, scholarly, pastoral, urgent, or another clear direction.
- Any supplied image references, rights restrictions, or visual motifs.
- Any sections the author already considers especially important.

If information is missing, make a conservative assumption and record it in the handoff notes. Do not silently invent factual citations, author names, dates, or claims.

### 3.2 Inspect the existing implementation

Use targeted searches rather than reading the entire repository indiscriminately.

Useful commands:

```bash
rg -n "goodness|resurrection|volume_tabs|reader_excluded_ids" build.py
rg -n "support-pull|resurrection-card|rail|diagram|visual" style.css src/visuals.py
rg --files content assets | sort
```

Inspect the current Goodness and Resurrection manifest files and compare them with the matching source and assets. The purpose is to learn the actual schema in this repository, including field names, defaults, and placement conventions. Do not assume that a plausible-looking field will be honored merely because it is easy to add.

The inspection should answer these questions:

- How are volumes registered?
- Where are root cards defined?
- How are tab links constructed?
- How are chapter IDs generated?
- How are reader-only blocks excluded?
- What manifest keys are actually consumed?
- Which visual kinds already exist?
- Which classes are shared and which are volume-specific?
- Are generated artifacts expected to be committed?

### 3.3 Make a content map

Before choosing visuals, create a one-page map of the essay. For each major unit, note:

| Unit | Main claim | Emotional or argumentative function | Candidate visual treatment |
| --- | --- | --- | --- |
| Opening | What question or tension begins the essay | Invitation, provocation, orientation | Hero image, opening illustration, short pull |
| Chapter 1 | First major movement | Establishes terms or problem | Diagram, shaded definition block |
| Chapter 2 | Development or evidence | Builds confidence or pressure | Source visual, comparison, image |
| Middle turn | Objection, fracture, or reversal | Raises stakes | Pressure card, darker shaded break |
| Final movement | Resolution or synthesis | Gives the reader somewhere to land | Answer card, closing illustration |

This map prevents the common failure mode in which visuals are sprinkled at regular intervals without following the argument.

## 4. Choose the slug and route before writing files

The slug is part of the public URL and should be treated as permanent.

### 4.1 Slug rules

Use:

- lowercase ASCII characters;
- hyphens between words;
- no spaces;
- no punctuation that needs URL encoding;
- no dates unless the date is genuinely part of the title;
- no temporary words such as `new`, `final`, `draft`, or `v2`.

Good examples:

```text
resurrection
goodness
the-living-word
hope-after-loss
```

Bad examples:

```text
Resurrection Essay
resurrection-final-v3
essay_2
new-volume
```

If the essay title changes later, preserve the slug unless the user explicitly wants a migration. A slug change is a link-breaking change, not a cosmetic rename.

### 4.2 Required volume paths

For a slug `foo`, the minimum source structure is:

```text
content/foo/essay.md
content/foo/manifest.json
assets/foo/
```

The generated route should be:

```text
foo/index.html
```

Do not create a second source copy under `foo/index.html`. Generated HTML is disposable output.

## 5. Prepare the canonical Markdown

The essay source is the most important artifact. Visual work must never become an excuse to shorten, paraphrase, or selectively omit the essay.

### 5.1 Preserve the complete essay

Keep all intended reader-facing prose in `essay.md`, including:

- title and subtitle;
- opening note or epigraph;
- all chapters and sections;
- quotations;
- lists;
- transitions;
- conclusion;
- appendices or notes that are intended for readers.

Preserve the author's paragraph boundaries where possible. Paragraph boundaries affect visual rhythm, card detection, spacing, and quotation placement.

### 5.2 Use stable Markdown structure

Prefer predictable heading levels. A typical long essay might use:

```markdown
# Essay Title

Subtitle or opening line.

## Chapter One: The Question

Opening paragraph.

### The first distinction

Development paragraphs.

## Chapter Two: The Evidence

More text.
```

Use headings to express actual intellectual structure, not to create visual spacing. Spacing belongs in CSS and renderer components.

Avoid:

- headings that are only decorative punctuation;
- a heading level that jumps unpredictably without a reason;
- giant all-caps headings that will wrap badly in the rail;
- manual HTML inserted into the essay unless the renderer genuinely requires it;
- repeated title text that will produce duplicate hero headings.

### 5.3 Headings and chapter navigation

The reader rail needs labels that are short enough to scan while the body can retain the full heading.

Use the full, meaningful heading in the Markdown. Let the existing chapter-label helper shorten the rail label where appropriate. If a heading is still too long or ambiguous, improve the heading itself rather than hiding essential meaning behind a bad truncation.

A good rail label identifies the intellectual movement:

```text
The Question
The Witnesses
The Objection
The Answer
```

A poor rail label is only a fragment:

```text
Chapter 3: Regarding the matter of...
```

If two chapters would receive the same shortened label, add a meaningful distinguishing phrase.

### 5.4 Source-only material and reader filtering

Some source files contain material that is useful for an agent or author but should not be shown to a reader. Examples include:

- drafting instructions;
- editorial audit notes;
- build instructions;
- verification summaries;
- AI-generation prompts;
- production checklists;
- internal decision logs;
- notes addressed to a future agent.

Preserve such material in the canonical source only if it is genuinely needed for the project record. Then exclude it at render time using the existing deterministic reader filtering mechanism in `build.py`, such as `reader_excluded_ids` or the project’s equivalent.

Do not hide public prose by using vague keyword filtering. A keyword can occur naturally in a theological or philosophical essay. Prefer stable structural markers or exact section IDs.

Recommended approach:

1. Give the internal section a deterministic heading or source marker.
2. Add that exact identifier to the new volume's exclusion configuration.
3. Keep the filter scoped to the new volume.
4. Confirm that neighboring reader-facing prose remains in the output.

Avoid exposing phrases such as:

```text
AI-generated
generated by an agent
verification pass
pipeline output
source integrity audit
drafting charter
prompt
```

The public reader should feel like a finished essay, not a transcript of its production process.

### 5.5 Bold-leading paragraphs and semantic cards

The current renderer recognizes certain bold-leading paragraphs as special essay cards, especially in the Resurrection treatment. This is a semantic convention, not merely a typography trick.

Use a leading bold phrase when the paragraph is genuinely one of these things:

- a compact claim;
- a direct objection;
- a pressure point the reader should pause over;
- a concise answer to a prior pressure point;
- a transition that deserves visual emphasis.

Do not bold the first words of ordinary prose merely to increase density. Too many cards flatten the hierarchy and make every paragraph compete for attention.

When a new volume needs a new card category, update the classification logic deliberately and document the new class. Do not overload an existing `pressure-card` class with contradictory meaning.

## 6. Use the source notes and website handoff as an implementation brief

The source package is valuable because it often contains the editorial decisions a future agent would otherwise have to rediscover. Use it as a design brief, but do not confuse a brief with reader-facing content.

### 6.1 `Sources and Notes`

Treat a `Sources and Notes` section as an evidence notebook. It can contain:

- numbered research notes;
- claims about empirical findings;
- qualifications and limits on those findings;
- primary theological or philosophical works;
- Scripture references;
- historical context;
- distinctions the author wants preserved.

Use it to:

1. understand what claims require nuance;
2. keep bios and definitions accurate;
3. preserve source attributions where the essay uses them;
4. avoid turning association into proof or a cited position into the author's own conclusion;
5. identify terms, people, texts, and traditions that deserve contextual notes;
6. build a source visual or diagram when the evidence structure is central to the essay.

Do not:

- render the research notes as a public bibliography unless the user explicitly requests one;
- insert every source into the essay body;
- promote a source note into a claim the essay does not make;
- expand a short supplied bio with invented details;
- use a research note to silently rewrite the author's argument.

If a source note qualifies a claim, preserve that qualification in any reader-facing definition, bio, card, caption, or pull derived from the claim.

### 6.2 `Website Handoff`

Treat a `Website Handoff` section as an explicit implementation brief. Extract each subsection and use it as follows:

| Handoff subsection | Required agent action |
| --- | --- |
| `Chapter titles` | Map proposed titles to actual essay movements and use them for headings or rail labels where they fit |
| `Visual ideas` | Turn the strongest ideas into original illustrations or diagrams tied to the corresponding section |
| `Glossary` | Use entries as the seed list for floating definitions; keep only terms used or clearly needed by the essay |
| `Thinkers needing short biographies` | Create compact bio notes at first meaningful use, using the supplied descriptions as the starting point |
| `Strongest objection-card passages` | Find exact matches in the essay and render them as pressure cards or objection cards |
| `Possible pull quotations` | Verify each candidate against the manuscript before rendering; do not present invented copy as a quotation from the essay |
| `Visual atmosphere` | Use it to establish palette, light, pacing, materiality, and image prompts for the whole volume |

The handoff is not a list of optional ideas to ignore. It is the author's intended direction and should be implemented unless it conflicts with the actual manuscript, the existing component system, or a user instruction.

### 6.3 Chapter-title mapping

When the handoff supplies chapter titles, create a mapping table before changing the source:

| Handoff title | Matching manuscript section | Action | Notes |
| --- | --- | --- | --- |
| `<title>` | `<heading or opening phrase>` | Use as heading / rail label / metadata | `<assumption>` |

If the manuscript already contains clear headings, preserve them unless the handoff explicitly requests replacement. If the manuscript has no headings but the handoff clearly provides the intended chapter structure, add the supplied titles as structural headings without changing the prose. Record that the titles were supplied by the handoff.

If one handoff title cannot be mapped, do not force it into an unrelated section. Either combine it with the nearest movement, represent it as a visual transition, or record it as unused with a reason.

### 6.4 Visual-idea mapping

For every supplied visual idea:

1. Identify the exact essay idea it represents.
2. Assign it to a chapter or transition.
3. Decide whether it should be an illustration, diagram, pull, card, or shaded break.
4. Rewrite it into the volume's image art direction without losing its conceptual core.
5. Give it a stable ID and descriptive filename.
6. Add alt text that describes what is visible.
7. Record it as implemented, adapted, combined, or intentionally omitted.

Do not use the visual list as a prompt to produce a gallery detached from the reading order. The visual should appear where the reader has enough context to understand why it is there.

### 6.5 Glossary-to-floating-definition mapping

The supplied glossary is a high-value shortcut. It gives the agent the intended vocabulary and often the author's preferred definitions.

For each glossary entry:

1. Confirm that the term appears in the essay or is necessary to understand it.
2. Preserve the supplied meaning unless it is too long, unclear, or contradicted by the essay.
3. Edit for floating-panel length and plain-language clarity without changing the concept.
4. Place the note at the first meaningful use.
5. Give it a stable contextual-note ID.
6. Avoid adding a second definition if Goodness's existing note system already handles the term globally.
7. Record glossary entries that were intentionally not surfaced and why.

If a glossary definition is interpretive rather than neutral, label it in a way that does not make the author's interpretation look like an uncontested dictionary fact.

### 6.6 Biography mapping

The supplied `Thinkers needing short biographies` section should be treated as a curated list, not as permission to create long profiles.

For each named person:

1. Find the first meaningful mention in the essay.
2. Attach a compact biography using the supplied text as the base.
3. State why the person matters to this essay.
4. Avoid adding unsupported dates, titles, or claims.
5. Preserve qualifiers such as “the essay's chief literary influence” or “provides the strongest objection” as editorial framing, not objective biography.
6. Check that the note opens and closes using the Goodness interaction pattern.

If the essay names a person who is not in the handoff, evaluate them using the normal contextual-note criteria. If the handoff names someone who never appears in the essay, do not add a floating bio merely to use every line of the handoff.

### 6.7 Objection-card and pull-quote mapping

The handoff may distinguish between strongest objections and possible pulls. Preserve that distinction:

- objection-card passages create pressure, resistance, or a serious counterargument;
- pull quotations create reflection, orientation, or memorable synthesis;
- answer cards should respond to pressure only when the essay actually provides an answer;
- a quote must not be presented as a direct quotation from the essay unless it exactly matches the manuscript or is clearly marked as editorial copy.

For every candidate, record:

```text
candidate text
exact manuscript match: yes/no
essay section
visual role: pressure / answer / pull
tone
placement
```

If a supplied candidate is not an exact match, search for the intended passage. If no match exists, either omit it or render it as clearly labeled editorial copy; never silently attribute invented wording to the author.

### 6.8 Visual-atmosphere mapping

Treat `Visual atmosphere` as a volume-level art-direction paragraph. Extract:

- starting palette;
- ending palette;
- lighting progression;
- emotional progression;
- material or texture language;
- visual motifs that should recur;
- restraint rules for the conclusion.

Use it to make the page evolve. For example, an instruction to begin in midnight blue and move toward restrained dawn light means the volume should have a visual arc, not merely a collection of blue and gold images. Do not make the final chapter brightly sentimental if the handoff explicitly calls for credible, restrained light.

### 6.9 Handoff coverage ledger

Before building, make a ledger with one row for every supplied handoff item:

| Item | Section | Intended use | Implemented as | Location | Status |
| --- | --- | --- | --- | --- | --- |
| `<text>` | Visual ideas | Opening image | `FOO-HERO-01` | Chapter 1 | implemented |
| `<term>` | Glossary | Floating definition | `FOO-TERM-01` | First use | implemented |
| `<person>` | Thinkers | Short bio | `FOO-BIO-01` | First use | implemented |

Use statuses such as `implemented`, `adapted`, `combined`, `not applicable`, or `omitted with reason`. This prevents a future agent from accidentally dropping the author's supplied direction while also preventing the page from becoming overloaded.

## 7. Design the visual grammar before creating assets

The visual reader works best when every visual has a job. Before generating or coding images, define a small grammar for the new volume.

### 6.1 Suggested visual roles

Use these roles as a menu, not as a quota:

| Role | What it does | Best placement |
| --- | --- | --- |
| Opening image | Establishes mood and central question | Hero or first major transition |
| Section illustration | Gives a chapter a memorable visual identity | Near the chapter opening or turn |
| Concept diagram | Makes a relationship or sequence visible | Immediately after the text that explains it |
| Source visual | Shows layers, witnesses, paths, or evidence | Near source/evidence discussion |
| Pressure pull | Makes an objection or difficult question linger | Just before or inside a tension section |
| Answer pull | Gives the reader a concise synthesis | After a sustained argument |
| Shaded break | Resets attention without adding new content | Between major movements |
| Closing image | Leaves the reader with the essay's final image | Conclusion or postscript |

### 6.2 Visual rhythm

Long-form prose needs variation, but variation must be paced.

A useful initial rhythm for a substantial essay is:

1. Opening composition.
2. Several readable prose paragraphs.
3. One modest visual pause.
4. A denser argument section.
5. A pull quote or shaded answer/pressure card.
6. A diagram or illustration at a genuine conceptual turn.
7. A return to uninterrupted prose.

Repeat this rhythm according to the essay's length and structure. Do not insert an illustration after every paragraph. Do not leave six screens of unbroken prose around the only visual.

### 6.3 How to decide whether something should be an image or a diagram

Use an illustration when the goal is atmosphere, metaphor, memory, place, gesture, or emotional resonance.

Use a diagram when the goal is comparison, sequence, hierarchy, evidence, causation, categories, or a relationship that should be understood at a glance.

Use a shaded text block when the idea is already clear in language but needs pacing or emphasis.

Use a pull quote when a sentence is independently memorable and can still be understood when removed from its paragraph context.

### 6.4 Floating definitions and short biographies

Every new volume should include the Goodness-style contextual layer when the essay introduces specialized terms, theological concepts, historical references, institutions, authors, or people who may not be immediately familiar to a thoughtful general reader.

This layer is not a glossary dumped at the end of the page. It is contextual help attached to the essay at the moment the reader needs it. The reader should be able to encounter a term or person in the prose, open a small floating definition or bio, understand the reference, and return to the same sentence without losing their place.

#### What deserves a floating definition

Add a definition when at least one of these is true:

- the term has a specialized theological, philosophical, historical, or literary meaning;
- the essay uses a familiar word in a more precise or unusual sense;
- the term is essential to understanding a later argument;
- the term is likely to be known by specialists but not by general readers;
- the term is a named doctrine, movement, practice, text, place, institution, or object;
- a short clarification would prevent the reader from having to leave the essay to search.

Do not define every ordinary noun. Too many annotations create visual noise and make the reader feel as if the essay is grading their knowledge.

#### What deserves a short bio

Add a short bio when a person is:

- cited as evidence or authority;
- part of the historical setting;
- a named author, theologian, philosopher, artist, ruler, witness, or critic;
- important to the essay's lineage of ideas;
- likely to be unfamiliar to a general reader;
- introduced without enough surrounding context to understand why they matter.

Do not turn a passing name into a full encyclopedia entry. The bio should answer: who is this person, why are they relevant here, and what is the minimum context needed to keep reading?

#### Content length defaults

Use these defaults unless the existing Goodness component clearly establishes a different limit:

| Context note | Target length | Content |
| --- | --- | --- |
| Term definition | One to three sentences | Plain-language meaning, then the essay-specific significance |
| Person bio | Two to four sentences | Identity or period, principal relevance, and connection to this essay |
| Place or institution | One to three sentences | What it is, where/when it belongs, and why it matters here |
| Scripture or named text | One to three sentences | What the text is and the precise role it plays in the current argument |

Write for the reader who is intelligent, interested, and moving through the essay quickly. Avoid academic throat-clearing, unsupported superlatives, and a biography's entire life story.

#### Placement rules

1. Place the note at the first meaningful use, not necessarily the first incidental mention.
2. If the first mention is inside a quotation, attach the note to the first surrounding prose mention when possible.
3. Do not attach the same note repeatedly throughout a short section.
4. If the term returns after a long gap, use the existing note behavior or a subtle re-open affordance rather than duplicating the full definition.
5. Keep the trigger close enough to the relevant word that the reader understands the relationship.
6. Do not place a floating note over a heading, pull quote, image focal point, or essential interactive control.
7. Ensure the note does not cover the very sentence the reader is trying to understand on a narrow viewport.

#### Writing rules for definitions and bios

Good contextual copy is:

- accurate enough for the essay's level of seriousness;
- neutral in tone unless the essay explicitly argues for an interpretation;
- concise;
- written in the site's voice;
- useful even when read without the surrounding paragraph;
- clear about uncertainty when historical or interpretive facts are disputed.

Avoid:

- repeating the sentence that triggered the note;
- writing “this is important” without explaining why;
- smuggling in a new argument that the essay never makes;
- pretending contested scholarship is settled;
- using vague labels such as “a famous thinker”;
- exposing source notes, prompts, generation instructions, or agent commentary;
- adding facts that were not checked when the fact is central to the note.

#### Implementation rules

Before inventing a new annotation system, inspect the Goodness implementation and reuse its existing markup, classes, behavior, and data shape. The goal is to extend the established reader pattern, not create a second tooltip language.

Trace one existing Goodness note through the entire system:

```text
source or manifest entry
        -> note lookup and placement
        -> trigger markup
        -> floating panel markup
        -> CSS positioning and visual style
        -> mobile behavior
        -> keyboard/focus behavior
```

For the new volume:

1. Add a stable ID for every term or person note.
2. Store the definition or bio in the same data location and shape used by Goodness.
3. Attach the trigger to a stable text anchor rather than a brittle screen coordinate.
4. Reuse the established open/close interaction.
5. Preserve the reader's place when the note opens and closes.
6. Add a visible label such as “Definition” or “Biography” if the existing component uses one.
7. Ensure the panel has a close action and does not trap the reader permanently.
8. Ensure the trigger is reachable by keyboard and has an understandable accessible name.
9. Ensure the content remains available on touch devices, where hover does not exist.
10. Ensure the note can be dismissed without requiring a precise click on a tiny icon.

If Goodness uses a custom JavaScript interaction, follow that interaction rather than creating a CSS-only hover state. A hover-only definition fails on touch and is inaccessible to keyboard users.

#### Contextual-note quality gate

For every note, the agent should be able to answer yes to all of these:

- Is this note genuinely useful to a non-specialist reader?
- Is it attached to the correct first-use anchor?
- Can the reader understand it without leaving the page?
- Is the wording concise enough for a floating panel?
- Does it avoid making a disputed claim sound certain?
- Does the note have an accurate type: definition, biography, place, institution, or text?
- Does it look like it belongs to Goodness rather than a browser tooltip?
- Does it work on desktop, mobile, keyboard, and touch?
- Can the reader return to the essay without losing their place?

#### Contextual-note density

Use judgment rather than a mechanical count. A long essay may need many notes; a short essay may need only a few. As a starting point, identify all candidates, then keep the strongest set that materially reduces reader friction. If every other sentence has an interactive term, remove the least necessary notes.

## 8. Build the manifest deliberately

Create `content/<slug>/manifest.json` by copying the structure of the nearest working manifest and adapting it to the new volume. Do not invent a parallel schema.

### 7.1 Stable IDs

Every visual should have a stable, unique ID. A practical naming scheme is:

```text
FOO-HERO-01
FOO-ILL-01
FOO-ILL-02
FOO-DIAG-01
FOO-PULL-01
FOO-CARD-01
```

Use uppercase IDs if that matches the existing manifests. The important properties are uniqueness, readability, and permanence.

Do not rename an existing visual ID casually. IDs can be referenced by placement logic, reports, or future editorial work.

### 7.2 Illustrative manifest pattern

The exact field names must match the repository's existing manifest schema. The following is a conceptual pattern showing the information that should be represented:

```json
{
  "title": "A Human-Readable Title",
  "slug": "foo",
  "theme": "short-theme-name",
  "hero": {
    "visual_id": "FOO-HERO-01",
    "alt": "A concise description of the opening image"
  },
  "pulls": [
    {
      "id": "FOO-PULL-01",
      "text": "A short sentence that can stand alone.",
      "tone": "normal",
      "chapter": "chapter-id"
    }
  ],
  "visuals": [
    {
      "id": "FOO-ILL-01",
      "kind": "image",
      "src": "assets/foo/example.png",
      "alt": "What the reader should understand from the image",
      "chapter": "chapter-id"
    }
  ]
}
```

Treat this as a planning example only. Confirm the real keys by inspecting Goodness and Resurrection before committing the file.

### 7.3 Placement choices

A visual should be attached to the nearest meaningful anchor, not to a random paragraph index that will become fragile when the essay is edited.

Prefer placement concepts such as:

- after the opening of a chapter;
- before a named objection;
- after the paragraph that introduces a sequence;
- immediately following the explanation of a diagram;
- before the conclusion of a movement.

If the implementation currently uses paragraph indexes, keep a short placement note beside each entry so a future agent can relocate it if the source changes.

### 7.4 Pull quote rules

A strong pull quote is:

- short enough to scan;
- taken from the essay or explicitly identified as editorial copy;
- meaningful outside its original paragraph;
- not so frequent that it becomes background noise;
- visually distinct from a normal blockquote.

Avoid using a pull quote for:

- a sentence that requires three paragraphs of context;
- a sentence with unresolved pronouns such as “this” or “they”;
- a paragraph that is already prominent as a card;
- production commentary;
- a generic slogan that could belong to any essay.

Use a pressure tone when the quote expresses friction, doubt, objection, cost, or a difficult question. Use a normal or answer tone when it clarifies, gathers, resolves, or invites reflection. The tone should correspond to the essay's argument, not just to the desired color.

## 9. Generate and curate images

Images should extend the essay's visual world. They should not feel like unrelated stock art placed between paragraphs.

### 8.1 Write a visual brief first

For each image, write a short brief with:

- the essay section it belongs to;
- the exact idea it should embody;
- the intended emotional temperature;
- composition and aspect ratio;
- color and material vocabulary;
- what must not appear;
- whether text inside the image is prohibited;
- accessibility description for the final asset.

Example:

```text
Section: the threshold between absence and witness
Idea: a sealed threshold that is not depicted as a horror scene, but as a quiet movement from concealment into disclosure
Mood: solemn, luminous, patient
Composition: vertical, centered threshold with generous negative space for the article layout
Palette: warm stone, dusk blue, muted gold
Avoid: modern objects, captions, logos, photorealistic gore, visible UI
Alt text: A quiet stone threshold opening into a narrow field of warm light.
```

### 8.2 Maintain a coherent art direction

Across a single volume, keep consistent decisions about:

- palette;
- grain or paper texture;
- contrast;
- line weight;
- degree of abstraction;
- use of empty space;
- lighting direction;
- visual age or materiality.

Goodness has a refined editorial atmosphere. A new volume can have its own palette and imagery, but it should still feel like it belongs to the same library. Avoid mixing glossy commercial photography, flat clip art, noisy AI collage, and unrelated diagram styles unless the essay itself justifies the tension.

### 8.3 House image language: lucid surrealism and mystical dream imagery

Unless the user specifies a different direction, use this as the visual north star for raster illustrations:

> A refined surrealist oil painting with the lucid visual poetry of Rene Magritte, transformed into a mystical and beautiful dream image for a contemplative essay. Use ordinary symbolic objects in impossible but calm arrangements, vast luminous skies, quiet thresholds, floating or inverted forms, soft atmospheric perspective, and a sense that the visible world is opening onto a deeper order.

The important qualities are:

- **Lucid surrealism**: the image should be clear and composed, not chaotic or hallucinatory.
- **Impossible but calm relationships**: objects may float, open, mirror, conceal, or transform, but the scene should feel intentional and contemplative.
- **Oil-paint materiality**: visible brushwork, layered pigment, softened edges, subtle canvas texture, and painterly light rather than sterile 3D rendering.
- **Mystical atmosphere**: luminosity, reverence, silence, thresholds, hidden depths, celestial scale, and the feeling of a beautiful mystery.
- **Dream logic**: the image should imply a question or paradox without explaining it with text.
- **Editorial restraint**: a small number of meaningful forms, generous negative space, and a composition that can sit beside serious prose.
- **Emotional beauty**: wonder, longing, peace, awe, and quiet revelation are preferred over fear, spectacle, gore, or shock.

Use a volume-specific palette, but begin from restrained surrealist colors such as:

- deep night blue and desaturated teal;
- cloud white and warm stone;
- muted ochre, brass, or antique gold;
- dusk rose, pale peach, or quiet vermilion when warmth is needed;
- black used as a softened atmospheric anchor rather than a harsh graphic void.

The agent should adapt the symbols to the essay. For example:

| Essay idea | Possible image language |
| --- | --- |
| Hiddenness and disclosure | A familiar object concealing a luminous interior, a curtain opening onto an impossible sky, or a doorway where no wall should be |
| Memory and witness | A suspended room, a stone object reflected in water, or an empty chair beneath a changing sky |
| Resurrection and transformation | A sealed form becoming a window, a quiet landscape emerging from darkness, or a body implied through light rather than depicted literally |
| Doubt and faith | Two incompatible horizons meeting, an object casting a different shadow, or a small light held inside a vast blue field |
| Time and history | Anachronistic objects sharing one calm table, layered architecture, or a clock dissolving into weather |
| Love and goodness | Ordinary objects arranged as a quiet constellation, an open hand holding a landscape, or warm light passing through an impossible structure |

These are compositional prompts, not mandatory motifs. The image must arise from the essay rather than forcing every volume into the same set of symbols.

#### Image-generation prompt formula

For each asset, construct the prompt in this order:

```text
essay idea + symbolic scene + impossible relationship + composition + oil-paint materiality + mystical atmosphere + volume palette + negative-space/layout requirement + exclusions
```

Example:

```text
An image about the moment a hidden witness becomes visible: a quiet stone doorway standing alone in a dark meadow, its interior opening not onto a room but onto a luminous dawn sky, one small chair facing the threshold, calm impossible geometry, refined surrealist oil painting with Magritte-like lucid symbolism, layered pigment and soft brushwork, mystical and dreamlike atmosphere, deep blue, warm stone, muted gold, generous negative space around the doorway for an editorial essay layout, no text, no captions, no logos, no UI, no photorealistic horror, no clutter.
```

Do not put the artist's name, an imitation signature, text, captions, or watermarks inside the final image. Do not recreate a specific existing painting. Borrow the high-level visual language of lucid surrealism and symbolic dream composition while creating an original scene for the essay.

#### Image selection quality gate

Keep an image only if it passes all of these tests:

- Does it embody a specific idea from the essay?
- Does the symbolism remain open enough for contemplation without becoming arbitrary?
- Does it feel beautiful, mystical, and dreamlike rather than merely strange?
- Does the oil-paint surface and palette belong with the other images in the volume?
- Does it have a clear focal point at the intended display size?
- Can it sit beside prose without overwhelming the reading experience?
- Does it avoid generic fantasy imagery, cliché religious stock imagery, visual noise, and accidental comedy?
- Does it contain no text, signature, logo, watermark, or production artifact?
- Does its alt text describe the actual visible composition without interpreting the entire essay for the reader?

### 8.4 Asset naming and storage

Store assets under the volume directory:

```text
assets/foo/
```

Use descriptive, stable names:

```text
threshold-of-witness.png
three-voices.svg
the-open-chamber.jpg
```

Avoid:

```text
image1.png
final-final.png
generated_004.png
Screenshot 2026-08-03 at 6.16.12 AM.png
```

Prefer web-friendly formats and reasonable dimensions. Do not ship a 20 MB source image when a carefully resized version will preserve the intended appearance. Preserve the original outside the published asset directory if the project needs it for future editing.

### 8.5 Image accessibility

Every meaningful image needs alt text that describes its communicative content, not its filename.

Good:

```text
Three narrow paths converge at a single illuminated doorway.
```

Weak:

```text
An artistic illustration.
```

If an image is purely decorative and the surrounding prose carries all meaning, use the renderer's supported decorative-image convention rather than forcing meaningless alt text.

Do not put crucial essay text only inside an image. If a visual contains labels or a sequence, reproduce the essential information in nearby HTML or a caption.

## 10. Add custom illustrations and diagrams

The current project uses both raster assets and code-native visuals. Use the simplest implementation that preserves the intended result.

### 9.1 Prefer existing visual kinds

Before adding code, search `src/visuals.py` and the manifests for an existing visual kind that already expresses the need. Reusing a visual kind keeps the system coherent and reduces CSS surface area.

Known Resurrection-era custom concepts include:

- `claim-doors`
- `method-window`
- `worlds-grid`
- `source-fan`
- `appearance-ladder`
- `gospel-windows`
- `prior-scale`

These names are examples of existing conceptual treatments, not a requirement that every future volume use them.

### 9.2 When a new visual kind is justified

Add a new kind only when:

- the visual represents a reusable conceptual structure;
- an image would be less clear than a semantic HTML diagram;
- the existing kinds cannot express the relationship cleanly;
- the new visual will remain readable without depending on hover or animation;
- the CSS and markup can be made responsive.

Do not add a custom kind simply to avoid preparing a suitable image.

### 9.3 Implementation contract for a new kind

When adding a new kind:

1. Add a renderer branch in `src/visuals.py`.
2. Give the root element a stable, volume-neutral class plus a specific modifier class.
3. Use semantic HTML where possible: headings, lists, figures, captions, and labels.
4. Keep the visual data in the manifest rather than hard-coding essay-specific text in the renderer.
5. Add CSS in `style.css` for the base layout, type, color, spacing, and narrow widths.
6. Include a readable fallback if the visual fails to load or the viewport is too narrow.
7. Add an accessible textual explanation adjacent to the visual.

### 9.4 Diagram content rules

The diagram must answer a question. Before implementation, write the sentence:

```text
This diagram helps the reader see that __________________.
```

If the sentence cannot be completed clearly, the diagram is probably decorative or under-specified.

Keep labels concise. Use the prose around the diagram for nuance. Do not cram the entire argument into tiny nodes.

## 11. Add the volume to the build pipeline

The exact function names may evolve, but the integration responsibilities remain the same.

### 10.1 Register source and metadata

In `build.py`, locate the structures that define:

- available essay slugs;
- source paths;
- volume titles and subtitles;
- cover or theme metadata;
- root landing-card copy;
- route generation;
- tab links;
- reader exclusion rules.

Add the new volume everywhere the existing volumes are represented. A volume that appears in only one registry will produce a partial integration.

The new slug should generally be present in all of these conceptual locations:

```text
source discovery
volume metadata
root landing page
volume route generation
shared tab switcher
reader filtering configuration, if needed
integrity/report configuration, if needed
```

### 10.2 Preserve existing routes

Do not replace a route list with a new list containing only the new volume. Merge the new entry into the existing structure.

The following routes must remain available after the change:

```text
/
/goodness/index.html
/resurrection/index.html
/<new-slug>/index.html
```

If the root page uses relative links, verify that links behave correctly from both `/index.html` and `/<slug>/index.html`. Relative paths are a common source of the “clicking Goodness opens an error” failure.

### 10.3 Tab behavior

The shared tabs should be treated as a site-level navigation component, not duplicated one-off markup.

For each tab, check:

- visible label;
- destination href;
- active-state logic;
- route-relative path behavior;
- title or aria label if present;
- order in the switcher;
- behavior at narrow widths.

Use the full volume title in the page heading but a compact label in the tab when necessary. Do not abbreviate a tab so far that it becomes ambiguous.

### 10.4 Root landing card

The root card should communicate:

- the volume title;
- a concise one- or two-sentence invitation;
- the visual identity or cover image;
- the destination route;
- any series or ordering relationship that matters.

Do not put internal build status, generated-image notes, file paths, or agent commentary in the card.

## 12. Create the page's visual composition

The volume page should feel designed from top to bottom.

### 11.1 Opening section

The opening should establish three things quickly:

- what the essay is about;
- what kind of attention it asks from the reader;
- why the visual world looks the way it does.

Possible opening components:

- title and subtitle;
- short epigraph;
- hero illustration;
- restrained metadata;
- a first pull quote;
- a visual motif that returns later.

Avoid putting every available element above the fold. The opening should invite entry, not look like a dashboard.

### 11.2 Shaded background breaks

Shaded blocks are one of the most effective ways to match the Goodness-style reading rhythm. They should mark a change in function, not merely fill empty space.

Use a shaded break for:

- a new movement in the argument;
- a shift from exposition to objection;
- a compact answer after sustained pressure;
- a reflective pause;
- a transition from historical material to present implication;
- a section that needs a different reading tempo.

Vary the shade subtly by semantic role. Keep the palette restrained and derived from the volume's theme. Too many competing fills make the page look like a collection of cards rather than an essay.

### 11.3 Quote and card hierarchy

Readers should be able to distinguish these at a glance:

1. Ordinary prose.
2. A cited blockquote.
3. A support pull.
4. A pressure card.
5. An answer or synthesis card.

If all five have the same background, border, font size, and padding, the hierarchy has collapsed. Use differences in scale, tone, spacing, and placement rather than relying on loud colors.

### 11.4 Chapter endings

At the end of a chapter, consider one of:

- a short closing pull;
- a visual that gathers the chapter's idea;
- extra whitespace before the next chapter;
- a restrained shaded transition.

Do not force a card at the end of every chapter. Sometimes uninterrupted prose followed by generous space is the strongest transition.

## 13. Responsive and accessibility requirements

A visually rich essay must remain a reading experience on mobile.

### 12.1 Narrow-width behavior

Every visual must be checked conceptually at narrow widths. It should:

- fit within the content column;
- avoid fixed-width overflow;
- allow labels to wrap or stack;
- keep text at a readable size;
- preserve adequate contrast;
- avoid requiring hover to reveal meaning;
- keep the focal point visible after cropping;
- avoid making the chapter rail unusably tall.

For diagrams, define a narrow layout explicitly. Common strategies include:

- stacking columns vertically;
- turning a horizontal sequence into a vertical sequence;
- reducing decorative connectors while retaining labels;
- moving the caption above or below the figure;
- allowing horizontal scrolling only when the relationship genuinely requires it and the scroll affordance is clear.

### 12.2 Typography

The site is an essay reader, so typography is structural. Check:

- body line length;
- paragraph spacing;
- heading wraps;
- quote size;
- card density;
- line height;
- contrast against shaded backgrounds;
- the difference between display and reading type.

Do not solve a wrapping problem by making text illegibly small. Prefer shorter labels, better layout, or a responsive stack.

### 12.3 Motion and interaction

Any motion should support orientation or reveal, not distract from reading. Avoid making essential content depend on animation. Ensure cards, quotes, and diagrams are understandable when motion is disabled.

### 12.4 Accessibility checklist

- Heading levels describe a real hierarchy.
- Links have clear labels.
- Active tab state is available visually and semantically where supported.
- Images have useful alt text or are explicitly decorative.
- Text is not encoded only in an image.
- Color is not the only signal for pressure versus answer.
- Focus states remain visible.
- Interactive elements are reachable by keyboard.
- Diagram explanations are available as text.

## 14. Remove AI and production fingerprints from the public reader

This project is a finished essay library. The reader should encounter the author's argument, not the machinery used to assemble it.

### 13.1 Audit all public surfaces

Check more than the essay body:

- root landing page;
- volume title and subtitle;
- tab labels;
- chapter rail;
- captions;
- pull quotes;
- image alt text;
- footer or metadata;
- empty states;
- error messages;
- generated report links;
- HTML comments if they can be exposed through the UI;
- browser document title.

### 13.2 Language to remove or rewrite

Do not expose internal phrases such as:

```text
AI generated
generated by an agent
prompt
pipeline
verification pass
build artifact
source audit
integrity check
drafting charter
future agent
```

Some of these phrases may be legitimate in source notes or reports. The rule is not to destroy useful provenance. The rule is to keep internal provenance out of the reader-facing presentation unless the user explicitly wants it visible.

### 13.3 Filtering safely

Use exact structural exclusions rather than broad substring deletion. Broad deletion can silently damage theology, history, or argumentation when ordinary words happen to match an internal keyword.

After filtering, compare the source's intended chapter sequence with the rendered sequence. The reader should not encounter a mysterious jump because an entire meaningful section matched an over-broad filter.

## 15. Build and integrity workflow

The normal build command is:

```bash
python3 build.py
```

Run it after the source, manifest, renderer, or styles are ready. The build should be the mechanism that updates generated pages and reports.

### 14.1 Expected build effects

Depending on repository policy, a successful build should update or emit:

- root `index.html`;
- `<new-slug>/index.html`;
- existing volume pages if the shared shell changed;
- copied or referenced site assets;
- integrity or content reports under `reports/`.

Do not assume that a successful exit code means every visual rendered. Review the build's own output and the generated route list when the workflow calls for verification.

### 14.2 Integrity principles

The canonical source should remain stable and traceable. When adding visual treatments:

- do not rebuild the essay from a summary;
- do not silently normalize quotations;
- do not remove paragraphs merely because they are hard to style;
- do not change source text to make a hash pass unless the source change is intentional;
- keep generated markup separate from canonical prose.

If the project emits a hash or integrity report, treat an unexpected hash change as a content decision that requires explanation, not as a nuisance to suppress.

### 14.3 Targeted checks

Use targeted searches for the new volume:

```bash
rg -n "foo|New Essay Title" build.py content assets index.html foo/index.html
rg -n "AI generated|generated by an agent|verification pass|pipeline|future agent" index.html foo/index.html
```

If a command reports missing generated files, first determine whether the file is meant to be generated or whether the route was never registered. Do not manually create a fake output page as a workaround.

## 16. Manual reader QA

When the user asks for launch or visual verification, serve the site over HTTP rather than relying only on `file://` behavior. Relative routes and browser security rules can differ.

A simple local server is:

```bash
python3 -m http.server 8765
```

Run it from the repository root. Keep the process alive for the browser session when the environment requires an attached process.

### 15.1 Route QA

Open and exercise:

```text
/
/goodness/index.html
/resurrection/index.html
/<new-slug>/index.html
```

For each route:

- click every volume tab;
- return to the root page;
- click the root card for each volume;
- click several chapter rail entries;
- use browser back and forward;
- refresh on a deep route;
- inspect an image or diagram section;
- check that no navigation link points to a stale path.

### 15.2 Visual QA

Inspect the page at:

- a wide desktop viewport;
- a narrow mobile-like viewport;
- a width where chapter labels are likely to wrap;
- a width where diagrams must stack.

Look specifically for:

- clipped text;
- cards that are too tall or too dense;
- images that dominate a chapter unintentionally;
- illustrations that feel unrelated to the adjacent claim;
- shaded blocks with insufficient contrast;
- rail labels that become unreadable;
- whitespace that signals a deliberate pause rather than a missing asset;
- repeated visual treatment that makes the page monotonous;
- broken images or missing captions;
- a conclusion that feels visually abandoned.

### 15.3 Editorial QA

Read the essay in order, not just by jumping between visual sections. Confirm:

- the opening makes sense;
- no source-only notes leak into the body;
- no important argument disappears near a filtered section;
- each visual appears near the text it explains;
- pressure and answer treatments occur in the correct order;
- the closing movement is complete;
- the root card and page title use the correct title.

## 17. Self-checking and self-improvement protocol

The agent must inspect its own work before declaring the volume complete. “The build succeeded” is only one signal. A finished volume requires structural, editorial, visual, interactive, and accessibility review.

Use this loop:

```text
build
  -> inspect
  -> identify defects and weak decisions
  -> rank them
  -> repair the highest-impact issues
  -> rebuild
  -> inspect again
  -> stop only when every quality gate passes or a limitation is explicitly recorded
```

Do not treat the first generated page as final. The first pass is an assembly pass. The second pass is where the page becomes intentional.

### 16.1 Create a quality ledger

During the work, keep a compact internal ledger with one row for each check:

| Area | Question | Evidence | Status | Repair |
| --- | --- | --- | --- | --- |
| Source | Is the essay complete and in order? | Source/build comparison | pass or issue | Restore or explain missing material |
| Routes | Do all volume links resolve? | Generated href review and browser | pass or issue | Fix registration or relative path |
| Context | Are definitions and bios useful and correctly placed? | Note inventory and interaction review | pass or issue | Rewrite, move, or remove note |
| Visuals | Does each major movement have an appropriate treatment? | Chapter-by-chapter visual map | pass or issue | Add, remove, or relocate visual |
| Responsive | Does it remain readable at narrow widths? | Narrow viewport inspection | pass or issue | Stack, resize, or simplify |
| Public copy | Is internal process language absent? | Targeted output search | pass or issue | Filter or rewrite |

The ledger can be temporary. Its purpose is to force the agent to gather evidence rather than rely on confidence.

### 16.2 Structural audit

Check the implementation mechanically before making aesthetic judgments:

1. Confirm `content/<slug>/essay.md` exists and contains the complete source.
2. Confirm `content/<slug>/manifest.json` exists and parses as JSON.
3. Confirm every referenced asset exists.
4. Confirm the new slug appears in all relevant build registries.
5. Confirm the generated root page and volume page exist.
6. Confirm the shared tab data contains every existing volume plus the new one.
7. Confirm chapter IDs used by the rail exist in the generated page.
8. Confirm visual and contextual-note IDs are unique within the new volume.
9. Confirm no generated page was manually patched instead of fixing its source.

Useful targeted checks include:

```bash
python3 -m json.tool content/<slug>/manifest.json >/dev/null
rg -n "<slug>|New Essay Title" build.py index.html <slug>/index.html
rg --files assets/<slug> content/<slug>
```

If the project has a built-in integrity test or report, use it. If it does not, do not pretend that a search is a complete integrity proof; record the limitation.

### 16.3 Source-to-reader audit

Compare the canonical essay and rendered reader as an editor, not only as a programmer.

Check:

- title and subtitle;
- opening paragraph;
- every chapter heading;
- transitions between chapters;
- quotations and lists;
- the central claim;
- objection or pressure sections;
- conclusion;
- appendices or notes intended for readers.

Look for these specific regressions:

- a paragraph silently omitted by filtering;
- a heading swallowed because it was interpreted as metadata;
- a list rendered as one paragraph;
- a quotation losing its attribution;
- duplicated title or epigraph;
- a chapter appearing out of order;
- an internal section leaking into the public reader;
- a visual inserted between two sentences that should remain together.

If source filtering is intentional, document exactly what was excluded and why. If the reader seems to jump, inspect the source and filter logic before changing the prose.

### 16.4 Contextual-layer audit

Build a note inventory from the essay and compare it to the rendered page.

For each important term or person, ask:

1. Is a note needed at all?
2. Is the note attached at the first meaningful use?
3. Does the definition or bio explain relevance rather than merely repeat a label?
4. Is the note concise enough to float without becoming an article?
5. Does it use the same visual language as Goodness?
6. Does it open by click or tap, not only by hover?
7. Does it work with keyboard focus?
8. Does it close cleanly?
9. Does it avoid covering the current sentence on a narrow viewport?
10. Does it preserve the reader's place after dismissal?

Remove notes that are technically correct but editorially unnecessary. The standard is reduced reader friction, not maximum annotation density.

### 16.5 Visual and pacing audit

Read the volume in order and make a one-line note for each major movement:

```text
Opening: invitation is clear; hero supports the question.
Movement 1: prose has room; definition appears at first key term.
Movement 2: diagram clarifies the sequence rather than repeating prose.
Pressure turn: card creates tension without overwhelming the page.
Answer turn: shaded section gives the reader a place to gather the argument.
Conclusion: final image or whitespace provides closure.
```

The agent should repair any of these conditions:

- two visually intense blocks compete directly;
- a long section has no visual or typographic breathing room;
- an image appears before the idea it represents has been introduced;
- a diagram appears after the reader has already forgotten the relationship it explains;
- a pull quote repeats the adjacent paragraph without adding emphasis;
- every chapter uses the same intervention, making the page predictable;
- one chapter has many illustrations while another important chapter has none;
- the art direction changes without an argument for why;
- the closing section has less care than the opening.

When a visual is weak, first try moving or removing it. Adding another image is not always the best repair.

### 16.6 Responsive audit

Inspect at least one wide and one narrow viewport, then deliberately test the failure points:

- the longest heading;
- the longest rail label;
- the widest diagram;
- the largest pull quote;
- the floating definition with the longest text;
- the bio near the bottom edge of the viewport;
- the first and last image;
- the tab row with every volume present.

Repair problems at the layout level. Do not solve overflow by hiding text that the reader needs.

### 16.7 Accessibility and interaction audit

For every interactive or informational visual element, confirm:

- the meaning survives without color;
- a keyboard user can reach and activate it;
- a touch user can open it;
- focus is visible;
- close controls are clear;
- images have alt text or an explicit decorative treatment;
- diagrams have a nearby textual explanation;
- text remains readable against every background;
- no essential content exists only inside an image or hover state.

### 16.8 Public-language audit

Search generated public output, not just source files:

```bash
rg -n -i "ai-generated|generated by an agent|prompt|pipeline|verification pass|build artifact|source audit|future agent|drafting charter" index.html <slug>/index.html
```

Review any match in context. A match may be legitimate essay content, but it must not be dismissed automatically. Remove or filter genuine production fingerprints while preserving ordinary essay language.

### 16.9 Defect ranking and repair loop

Rank findings before changing code:

| Priority | Meaning | Examples |
| --- | --- | --- |
| P0 | The reader cannot use the volume | Build failure, broken route, missing essay, unusable mobile layout |
| P1 | The volume is materially incomplete or misleading | Missing chapter, leaked internal note, absent key visual, inaccessible definition |
| P2 | The volume works but feels unfinished | Repetitive cards, weak art direction, awkward spacing, overly long bio |
| P3 | Optional polish | Minor copy tightening, small spacing refinement, nonessential variation |

Repair all P0 and P1 findings before polishing P2 or P3 issues. After each meaningful repair, rebuild and rerun the affected audit. Do not stack many speculative changes before checking whether the problem is solved.

### 16.10 Self-approval standard

The agent may declare the work complete only when:

- no P0 or P1 findings remain;
- every major essay movement has been read in the generated page;
- contextual notes have been reviewed as a set, not just individually;
- the visual system is coherent from opening through conclusion;
- existing volumes remain available;
- the public output contains no accidental process language;
- any unverified item is explicitly listed as a limitation.

If the agent cannot perform browser or image inspection in its environment, it must still complete the structural, source, manifest, output-language, and route checks and state that visual inspection remains outstanding. It must not claim exceptional visual quality without visual evidence.

## 18. Common failure modes and repairs

### Failure: clicking an existing volume opens an error

Likely causes:

- a route was renamed instead of preserved;
- a relative href was calculated from the wrong directory;
- a root link points to a source path rather than a generated route;
- the server is serving a different working directory;
- an existing tab entry was overwritten while adding the new one.

Repair by checking the generated hrefs from both the root page and a nested volume page. Preserve the existing route names and make the new entry additive.

### Failure: the new volume appears on the root page but the tab is missing

The root card and shared tab registry are separate concerns. Add the volume to the shared tab data and regenerate every page that contains the shell.

### Failure: the page loads but all the visual work is absent

Likely causes:

- the manifest filename or path is wrong;
- manifest keys do not match the actual schema;
- visual IDs do not match placement IDs;
- the renderer does not recognize the `kind`;
- the asset path is relative to the wrong directory;
- generated HTML was not rebuilt after the manifest changed.

Repair by tracing one visual end to end: manifest entry, renderer lookup, generated markup, CSS class, and final asset URL.

### Failure: a custom diagram renders as a blank box

Likely causes:

- the visual kind has no renderer branch;
- data fields are missing or named differently than the renderer expects;
- the CSS makes text transparent or collapses the container;
- the diagram is using a fixed size that is invalid at the current width.

Start with one minimal data entry and one visible label. Add complexity only after the simplest version renders.

### Failure: the page feels like a slide deck instead of an essay

Likely causes:

- too many illustrations;
- every paragraph has a card treatment;
- background colors change too often;
- pull quotes repeat sentences without adding pacing;
- diagrams are not connected to the text.

Restore longer runs of prose. Reserve strong treatments for genuine turns, pressures, and syntheses.

### Failure: the page feels like plain Markdown

Likely causes:

- no opening composition;
- no visual grammar;
- all visual work is pushed to the end;
- long sections have no shaded transitions or pulls;
- the manifest exists but is not wired into the renderer.

Build a visual map from the content map and add treatments at argumentative turning points.

### Failure: internal AI/process language is visible

Search every public surface, not just the Markdown body. Then add a scoped structural exclusion or rewrite the reader-facing metadata. Do not use a broad global replacement that might damage the canonical essay.

### Failure: chapter rail labels are too long

Use meaningful shorter labels or let the existing `chapter_rail_label` helper do its job. Add CSS ellipsis only where it preserves usability. Never make the rail so wide that it steals the reading column.

### Failure: images look inconsistent

Create an art-direction brief, then regenerate or curate the outliers. Matching only subject matter is not enough; match palette, texture, contrast, abstraction, and composition.

### Failure: a generated page was edited directly

Move the change into `build.py`, the manifest, the source, `src/visuals.py`, or `style.css`, then rebuild. Direct edits to generated HTML will be lost and create confusing divergence.

## 19. Recommended implementation order

Use this order for a normal new volume.

### Phase A: source and inventory

1. Choose and record the permanent slug.
2. Create `content/<slug>/` and `assets/<slug>/`.
3. Add the complete canonical `essay.md`.
4. Map the chapter structure and identify reader-only material.
5. Identify important terms and people that need Goodness-style floating notes.
6. Compare the existing Goodness and Resurrection source/manifests to understand actual conventions.

### Phase B: route and shell integration

7. Register the new volume in `build.py` source discovery.
8. Add volume metadata and root-card content.
9. Add the new entry to the shared volume tab data.
10. Add the route to the page-generation loop.
11. Add scoped reader exclusions if needed.

### Phase C: visual design

12. Make a content-to-visual map.
13. Define the volume's palette and art direction.
14. Choose hero, illustrations, diagrams, pulls, shaded breaks, definitions, and bios.
15. Create `manifest.json` with stable IDs and anchored placements.
16. Add or curate image assets.
17. Add custom renderer cases only where existing visual kinds are insufficient.
18. Add contextual-note data and reuse the Goodness interaction pattern.
19. Add CSS for any new visual classes and responsive states.

### Phase D: build and QA

20. Run `python3 build.py`.
21. Review generated routes and reports.
22. Search public output for process language.
23. Exercise tabs, chapter links, and contextual notes over HTTP.
24. Read the full essay in order.
25. Inspect wide and narrow layouts.
26. Run the self-checking and repair loop in Section 17.
27. Fix any issues in source/configuration, then rebuild.

### Phase E: handoff

25. Record the files changed and why.
26. Record any new visual kinds and their IDs.
27. Record asset provenance or generation notes outside the public reader if required.
28. Record known limitations and future opportunities.
29. Commit in logical chunks if the user has requested a commit.

## 20. GitHub publication protocol

Pushing the finished volume is part of the task. A local build is not the final deliverable.

### 19.1 Inspect the repository before staging

Before touching the index, establish the current Git state:

```bash
git status --short
git branch --show-current
git remote -v
```

The agent must protect work it did not create. If the worktree contains unrelated changes, leave them unstaged. If unrelated edits overlap the same files and cannot be separated safely, pause and ask the user before staging or committing. Never use `git reset --hard`, `git checkout --`, `git clean`, or another destructive command to make the worktree look clean.

### 19.2 Define the commit scope

The commit should contain the complete new volume and the shared-site changes required to make it work, including only files that belong to this task:

- new source Markdown;
- new manifest;
- new volume assets;
- `build.py` changes;
- `style.css` changes;
- `src/visuals.py` changes;
- generated outputs required by repository policy;
- generated reports required by repository policy.

Do not stage unrelated user work, temporary screenshots, local logs, secrets, credentials, browser profiles, or speculative cleanup.

Stage explicit paths rather than using a blind `git add .` when the worktree is not known to be task-clean:

```bash
git add content/<slug>/essay.md content/<slug>/manifest.json assets/<slug> build.py style.css src/visuals.py
```

Include generated files only when this repository tracks generated outputs. If the repository's existing pattern tracks generated `index.html` files and reports, include the corresponding new and updated outputs. If it does not, do not add them merely because they changed locally.

### 19.3 Review the staged change

Before committing, inspect exactly what will be published:

```bash
git diff --cached --stat
git diff --cached --name-only
git diff --cached --check
```

Confirm that:

- the complete essay is present;
- no source-only production note leaked into reader-facing output;
- no unrelated file is staged;
- no generated file contains a local machine path or secret;
- assets are not accidentally duplicated under the wrong volume;
- the new route and tab are included;
- the contextual definitions and bios are included;
- formatting errors and trailing whitespace are absent.

If the staged diff is wrong, unstage only the incorrect paths with a non-destructive command such as `git restore --staged <path>`, then stage the correct paths. Do not discard the underlying working-tree changes.

### 19.4 Commit clearly

Use a concise commit message that names the volume:

```bash
git commit -m "Add <title> essay volume"
```

If the change includes a substantial shared renderer or design-system update, make that clear in the commit body or use the repository's established commit convention. Do not create a vague commit such as `updates`, `stuff`, or `final changes`.

### 19.5 Push the active branch

First confirm the branch and remote again if the work took a long time. Push the branch that contains the commit:

```bash
git push origin HEAD
```

If the branch has no upstream yet, use:

```bash
git push -u origin HEAD
```

Never force-push for this workflow. Do not rewrite remote history, delete branches, merge directly into a protected branch, or close a pull request unless the user explicitly asks for that separate action.

### 19.6 Prove the push result

A push command returning an error is not a successful publication. After a successful push, record:

```bash
git status --short
git log -1 --oneline
git branch --show-current
```

The handoff must state:

- branch name;
- commit hash and subject;
- remote pushed to;
- whether the push succeeded;
- whether a pull request is still needed.

If authentication, network access, branch protection, or remote configuration blocks the push, report the exact blocker and say clearly that the change is committed locally but not pushed. Do not say “published,” “on GitHub,” or “done” in that situation.

### 19.7 GitHub completion gate

The volume is not complete until both of these are true:

1. The local commit contains the intended scoped change.
2. The commit has been successfully pushed to the intended remote branch.

The user may later request a pull request or merge, but those are separate operations. Pushing the branch is required; merging is not inferred.

## 21. Practical file-change checklist

For a typical volume, the set of files that may need modification is:

```text
content/<slug>/essay.md       required
content/<slug>/manifest.json  required
assets/<slug>/*                usually required
build.py                       required
style.css                      likely required
src/visuals.py                 only for new code-native visuals
reports/*                      generated when the build updates them
index.html                     generated
<slug>/index.html              generated
```

Do not touch files merely because they exist in the project. Identify the exact responsibility of each file first.

## 22. Handoff template

When handing the work to another agent or to the user, include a compact summary like this:

```text
Volume: <title>
Slug: <slug>
Route: /<slug>/index.html

Canonical source:
- content/<slug>/essay.md

Editorial configuration:
- content/<slug>/manifest.json
- reader-only exclusions in build.py: <none or identifiers>

Visual assets:
- assets/<slug>/<asset-name>
- assets/<slug>/<asset-name>

Renderer/style changes:
- build.py: <what changed>
- src/visuals.py: <none or visual kinds>
- style.css: <what changed>

Generated outputs:
- index.html
- <slug>/index.html
- reports/<report-name>

GitHub publication:
- branch: <branch>
- commit: <hash> <subject>
- remote: <remote>
- push: <succeeded or exact blocker>
- pull request: <not needed, requested, or URL if created>

Known limitations:
- <brief, honest note>
```

## 23. Final pre-handoff checklist

Before declaring the new volume complete, answer every item with yes or not applicable.

### Source

- Is the full essay present?
- Is the source order intact?
- Are headings meaningful and navigable?
- Are source-only notes intentionally filtered rather than accidentally omitted?
- Did any canonical wording change unintentionally?

### Supplied source package

- Was the boundary between reader manuscript and source package identified?
- Were `Sources and Notes` used for grounding without being rendered wholesale?
- Was the `Website Handoff` parsed into a coverage ledger?
- Were the supplied chapter titles mapped to actual manuscript movements?
- Were visual ideas implemented, adapted, combined, or omitted with reasons?
- Were glossary entries turned into selective floating definitions?
- Were named thinkers turned into concise first-use bios where appropriate?
- Were objection-card passages matched against the essay exactly?
- Were pull-quote candidates verified before being attributed to the essay?
- Was the supplied visual atmosphere used to shape the volume's visual arc?
- Were conflicts between the manuscript and handoff recorded and resolved using the stated priority order?

### Build

- Is the slug registered in every required build structure?
- Does the root card link to the generated route?
- Does the shared tab switcher include the new volume?
- Do Goodness and Resurrection still have working routes?
- Did the build complete?

### Visuals

- Does the opening have a deliberate composition?
- Are there enough visual pauses for the essay's length?
- Are illustrations tied to specific ideas?
- Are diagrams used for relationships that benefit from being seen?
- Are pressure and answer moments differentiated?
- Are the shaded blocks paced rather than repetitive?
- Do the illustrations share a lucid surrealist oil-painting and mystical dream language while remaining specific to this essay?
- Do the images avoid generic fantasy, visual clutter, text, logos, signatures, and watermarks?
- Does the conclusion receive appropriate visual closure?

### Contextual notes

- Are important terms defined at their first meaningful use?
- Are important people given concise, relevant bios?
- Are notes selective rather than attached to every unfamiliar word?
- Do definitions and bios follow the Goodness visual and interaction pattern?
- Do they open by click or tap and work with keyboard focus?
- Do they close cleanly without losing the reader's place?
- Do they remain readable and unobtrusive on narrow screens?

### Accessibility and responsive behavior

- Are images described or marked decorative?
- Are diagrams explained in text?
- Are links and tabs understandable?
- Does the page remain readable on narrow widths?
- Do labels wrap or truncate safely?
- Is color not the only carrier of meaning?

### Public presentation

- Is all AI/process language absent from public surfaces?
- Are captions, alt text, titles, and metadata reader-facing?
- Are there no broken images or stale links?
- Does the site feel like one coherent essay library?

### GitHub publication

- Was the repository state inspected before staging?
- Were unrelated changes left untouched?
- Does the staged diff contain only this volume and required shared-site changes?
- Was the commit reviewed before it was created?
- Was the commit pushed to the intended remote branch?
- Is the commit hash recorded?
- If the push failed, is the exact blocker clearly disclosed?

### Handoff

- Are all changed files named?
- Are new visual IDs documented?
- Are the branch, commit, remote, and push result documented?
- Are known limitations disclosed?
- Is the generated output consistent with repository policy?

## 21. The governing principle

The best new volume is not the one with the most effects. It is the one where form follows thought.

Use the essay's own movements to determine where the page should open up, darken, pause, clarify, gather, or become luminous. Preserve the source as the authority. Let the manifest describe visual intent. Let the renderer provide reusable structure. Let the CSS create atmosphere without competing with the reading. Keep internal production machinery out of the reader's field of view.

If a future agent follows those principles, a new essay will not merely be appended to the site. It will become another fully realized room in the same library.
