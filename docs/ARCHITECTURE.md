# Faith essay library architecture

The repository is a small static site. `content/<essay>/essay.md` is the only source for essay prose. Each Markdown block receives a structural ID during parsing; visual placement manifests target those IDs and never search for sentence fragments.

`build.py` parses both essays, verifies their recorded SHA-256 hashes, renders independent pages at `/goodness/` and `/resurrection/`, writes the library home at `/`, copies the shared CSS/JavaScript into `assets/`, and compares the generated essay container against the canonical block sequence.

Supporting data lives beside each essay in `manifest.json`. Glossary entries and visual captions are intentionally outside the canonical essay container. `content/resurrection/site-handoff.md` and `master-scaffold.md` remain included as research and placement references; they never override `essay.md`.

Build with:

```sh
python3 build.py --check
```

Preview the generated root with:

```sh
python3 -m http.server 8000
```

The generated root is deployable to a static host. The compatibility tradeoff is explicit: the old root URL is now the library home, while Goodness has its own stable route at `/goodness/`.
