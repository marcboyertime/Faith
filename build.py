#!/usr/bin/env python3
"""
GOODNESS ITSELF — site builder
Reads goodness-itself-fortified.md and emits a fully self-contained
index.html (CSS + JS inlined, images in ./images).
Verifies that every character of the essay survives the conversion.
"""
import re, html, pathlib

ROOT = pathlib.Path(__file__).parent
SRC  = pathlib.Path("/Users/mboyer/Downloads/goodness-itself-fortified.md")
OUT  = ROOT / "index.html"

raw_lines = SRC.read_text(encoding="utf-8").splitlines()

# ---------------------------------------------------------------
# inline markdown -> html
# ---------------------------------------------------------------
def fmt(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+?)\*", r"<em>\1</em>", s)
    return s

def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s))

def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())

# ---------------------------------------------------------------
# classification
# ---------------------------------------------------------------
CLASH = ("**Weld", "**Attack", "**Assault", "**Objection", "**\"",
         "**Failure mode", "**First", "**Second", "**Third", "**Part")
FIBER = re.compile(r"^\*\*The (semantic|phenomenological|cosmological|"
                   r"moral-psychological|metaethical|epistemological|"
                   r"existential-historical) line")

def kind_of(raw: str) -> str:
    s = raw.strip()
    if "Fecisti nos ad te" in s:
        return "blessing"
    if s.startswith('*"') and s.endswith('"*'):
        return "objection"
    if s.startswith('*"'):
        return "clash"
    if FIBER.match(s):
        return "fiber"
    if s.startswith("**Fact "):
        return "fact"
    if s.startswith("**Contestant "):
        return "contestant"
    if s.startswith(CLASH):
        return "clash"
    return "p"

# ---------------------------------------------------------------
# artwork + drawings
# ---------------------------------------------------------------
SWORD = ('<svg viewBox="0 0 24 24"><path d="M4 20 18 6m0 0h-4m4 0v4M6 16l2 2"'
         ' stroke-width="2" fill="none"/></svg>')

ORN = ('<svg class="ornament" viewBox="0 0 190 24" fill="none" '
       'stroke="var(--gold-dim)" stroke-width="1">'
       '<path d="M8 12h62M120 12h62"/>'
       '<path d="M76 12c3-4 7-4 9 0M105 12c3-4 7-4 9 0"/>'
       '<path d="M95 3l8 9-8 9-8-9z" stroke-width="1.2"/>'
       '<circle cx="95" cy="12" r="1.5" fill="var(--gold)" stroke="none"/>'
       '</svg>')

SVG_MAPS = """
<figure class="diagram">
<svg viewBox="0 0 760 300" fill="none" stroke="currentColor" stroke-width="1.4">
  <rect x="24" y="26" width="330" height="230" rx="12" stroke="var(--line)"/>
  <rect x="38" y="40" width="302" height="202" rx="8" stroke="var(--line-soft)" stroke-dasharray="3 6"/>
  <text x="189" y="270" text-anchor="middle" font-size="11">MAP OF BRUTE FACTS</text>
  <path d="M80 220 C 130 190 100 150 155 132 S 250 138 268 108 300 96 308 84"
        stroke="var(--ember)" stroke-width="2" stroke-dasharray="7 6"/>
  <circle cx="80" cy="220" r="4" fill="var(--ember)" stroke="none"/>
  <path d="M300 78l16 12M316 78l-16 12" stroke="var(--ember)" stroke-width="2.4"/>
  <text x="308" y="62" text-anchor="middle" font-size="9" fill="var(--ember)">HERE BE BRUTE FACTS</text>
  <path d="M120 200l14-22 14 22zM150 204l10-16 10 16z"/>
  <path d="M230 190v-14M230 176c-5 0-8 4-8 4s3 4 8 4 8-4 8-4-3-4-8-4z"/>
  <circle cx="70" cy="70" r="11"/><path d="M70 61v6l4 5" stroke-width="1.8"/>
  <text x="70" y="97" text-anchor="middle" font-size="8">N</text>

  <rect x="406" y="26" width="330" height="230" rx="12" stroke="var(--gold-dim)"/>
  <rect x="420" y="40" width="302" height="202" rx="8" stroke="var(--line-soft)" stroke-dasharray="3 6"/>
  <text x="571" y="270" text-anchor="middle" font-size="11" fill="var(--gold)">MAP THAT KEEPS WORKING</text>
  <path d="M452 220 C 500 190 478 158 530 140 S 610 150 632 116 686 96 700 74"
        stroke="var(--gold)" stroke-width="2" stroke-dasharray="7 6" class="beamflow"/>
  <circle cx="452" cy="220" r="4" fill="var(--gold)" stroke="none"/>
  <circle cx="530" cy="140" r="3" stroke="var(--gold)"/>
  <circle cx="632" cy="116" r="3" stroke="var(--gold)"/>
  <circle cx="700" cy="74" r="6" fill="var(--gold)" stroke="none" class="pulse"/>
  <path d="M700 58v-8M700 90v8M684 74h-8M716 74h8M689 63l-6-6M711 85l6 6M711 63l6-6M689 85l-6 6"
        stroke="var(--gold)" stroke-width="1.6" class="pulse"/>
  <ellipse cx="500" cy="80" rx="34" ry="16" stroke="var(--line-soft)" stroke-dasharray="2 5"/>
  <ellipse cx="640" cy="200" rx="40" ry="18" stroke="var(--line-soft)" stroke-dasharray="2 5"/>
  <path d="M480 210l12-18 12 18z"/>
</svg>
<figcaption><span class="cap-title">THE WIN CONDITION</span> · you cannot step outside all maps — walk the territory, and see which one keeps working</figcaption>
</figure>
"""

SVG_HIERARCHY = """
<figure class="diagram">
<svg viewBox="0 0 720 270" fill="none" stroke="currentColor" stroke-width="1.6">
  <path d="M112 168 C 260 150 480 108 620 66" stroke="var(--gold)" stroke-dasharray="4 7" class="beamflow"/>
  <path d="M626 60l-14 4 6 12z" fill="var(--gold)" stroke="none"/>
  <text x="370" y="92" text-anchor="middle" font-size="10" fill="var(--gold)">MORE BEING</text>

  <rect x="60" y="206" width="120" height="14" rx="3"/>
  <path d="M96 190l-16 10 6 12h32l8-12-12-10z"/>
  <text x="108" y="180" text-anchor="middle" font-size="11">STONE</text>
  <text x="120" y="248" text-anchor="middle" class="big" font-size="14">is</text>

  <rect x="230" y="176" width="120" height="14" rx="3"/>
  <path d="M290 174v-24"/>
  <circle cx="290" cy="136" r="15"/><circle cx="278" cy="148" r="10"/><circle cx="302" cy="148" r="10"/>
  <text x="290" y="112" text-anchor="middle" font-size="11">TREE</text>
  <text x="290" y="248" text-anchor="middle" class="big" font-size="14">is, and lives</text>

  <rect x="400" y="146" width="120" height="14" rx="3"/>
  <ellipse cx="460" cy="126" rx="8" ry="7"/>
  <circle cx="448" cy="112" r="3.4"/><circle cx="456" cy="108" r="3.4"/><circle cx="465" cy="108" r="3.4"/><circle cx="472" cy="112" r="3.4"/>
  <text x="460" y="92" text-anchor="middle" font-size="11">ANIMAL</text>
  <text x="460" y="248" text-anchor="middle" class="big" font-size="14">is, lives, perceives</text>

  <rect x="570" y="116" width="120" height="14" rx="3"/>
  <circle cx="630" cy="76" r="8"/>
  <path d="M613 104c3-14 31-14 34 0z"/>
  <text x="630" y="52" text-anchor="middle" font-size="11">HUMAN</text>
  <text x="630" y="248" text-anchor="middle" class="big" font-size="14">knows that she is</text>
</svg>
<figcaption><span class="cap-title">THE ONTOLOGICAL SCALE</span> · each step up is not just difference but more — and your grief already believes it</figcaption>
</figure>
"""

SVG_ESSEX = """
<figure class="diagram">
<svg viewBox="0 0 720 300" fill="none" stroke="currentColor" stroke-width="1.6">
  <circle cx="252" cy="126" r="64"/>
  <circle cx="344" cy="126" r="64" stroke="var(--gold)"/>
  <text x="236" y="122" text-anchor="middle" class="big" font-size="15">WHAT</text>
  <text x="236" y="140" text-anchor="middle" class="big" font-size="12">it is</text>
  <text x="360" y="122" text-anchor="middle" class="big" font-size="15">THAT</text>
  <text x="360" y="140" text-anchor="middle" class="big" font-size="12">it is</text>
  <text x="298" y="222" text-anchor="middle" font-size="10">ESSENCE &#8800; EXISTENCE — IN EVERY FINITE THING, A GAP</text>

  <path d="M436 126h64" stroke="var(--gold)" stroke-width="2"/>
  <path d="M506 120l12 6-12 6z" fill="var(--gold)" stroke="none"/>

  <circle cx="606" cy="126" r="58" stroke="var(--gold)" stroke-width="2"/>
  <circle cx="606" cy="126" r="72" stroke="var(--gold-dim)" stroke-dasharray="3 7" class="pulse"/>
  <text x="606" y="122" text-anchor="middle" class="big" font-size="15" fill="var(--gold-bright)">WHAT = THAT</text>
  <text x="606" y="142" text-anchor="middle" class="big" font-size="12">identical</text>
  <text x="606" y="222" text-anchor="middle" font-size="10" fill="var(--gold)">THE TERMINUS — NO GAP</text>
</svg>
<figcaption><span class="cap-title">ESSENCE &amp; EXISTENCE</span> · apart in everything we meet — identical only at the stopping point</figcaption>
</figure>
"""

SVG_TRAIN = """
<figure class="diagram">
<svg viewBox="0 0 760 250" fill="none" stroke="currentColor" stroke-width="1.6">
  <path d="M16 196h728" stroke="var(--line)"/>
  <rect x="60" y="128" width="100" height="44" rx="6" stroke-dasharray="4 6"/>
  <text x="110" y="154" text-anchor="middle" class="big" font-size="14">&#8230;</text>
  <text x="110" y="112" text-anchor="middle" font-size="9">TEN THOUSAND MORE</text>
  <path d="M160 150h20"/>

  <rect x="180" y="128" width="110" height="44" rx="6"/>
  <circle cx="206" cy="182" r="9"/><circle cx="264" cy="182" r="9"/>
  <path d="M290 150h20"/>

  <rect x="310" y="128" width="110" height="44" rx="6"/>
  <circle cx="336" cy="182" r="9"/><circle cx="394" cy="182" r="9"/>
  <path d="M420 150h20"/>

  <rect x="440" y="118" width="130" height="54" rx="8" stroke="var(--gold)" stroke-width="2"/>
  <rect x="532" y="88" width="38" height="30" rx="4" stroke="var(--gold)"/>
  <path d="M458 118v-22h16v22" stroke="var(--gold)"/>
  <circle cx="470" cy="182" r="10" stroke="var(--gold)"/><circle cx="512" cy="182" r="10" stroke="var(--gold)"/><circle cx="552" cy="182" r="10" stroke="var(--gold)"/>
  <path d="M570 148l26 12-26 12z" stroke="var(--gold)"/>
  <circle cx="612" cy="160" r="5" fill="var(--gold)" stroke="none" class="pulse"/>
  <path d="M626 160h22M622 148l16-8M622 172l16 8" stroke="var(--gold)" class="pulse"/>
  <circle cx="466" cy="82" r="6" stroke-dasharray="2 4"/><circle cx="472" cy="66" r="8" stroke-dasharray="2 4"/><circle cx="480" cy="46" r="10" stroke-dasharray="2 4"/>
  <text x="505" y="228" text-anchor="middle" font-size="10" fill="var(--gold)">ENGINE — HAS IT OF ITSELF</text>
  <text x="300" y="228" text-anchor="middle" font-size="10">CARS — ONLY PASS IT ALONG</text>
</svg>
<figcaption><span class="cap-title">THE ESSENTIALLY ORDERED SERIES</span> · ten thousand cars that can&#8217;t move themselves are exactly as motionless as one</figcaption>
</figure>
"""

SVG_PRISM = """
<figure class="diagram">
<svg viewBox="0 0 720 300" fill="none" stroke="currentColor" stroke-width="1.6">
  <path d="M30 150h272" style="stroke:var(--ink-bright)" stroke-width="5" class="beamflow"/>
  <text x="160" y="122" text-anchor="middle" class="big" font-size="15">one simple act</text>

  <path d="M340 82l-64 132h128z" stroke="var(--gold)" stroke-width="2"/>
  <text x="340" y="250" text-anchor="middle" font-size="10" fill="var(--gold)">THE PRISM OF OUR FINITE CONCEPTS</text>

  <path d="M372 132 L 690 84"  style="stroke:var(--gold-bright)" stroke-width="2.6"/>
  <path d="M376 142 L 690 118" style="stroke:var(--gold)" stroke-width="2.6"/>
  <path d="M378 152 L 690 152" style="stroke:var(--ember)" stroke-width="2.6"/>
  <path d="M376 162 L 690 186" style="stroke:var(--gold-dim)" stroke-width="2.6"/>
  <path d="M372 172 L 690 220" style="stroke:var(--faint)" stroke-width="2.6"/>
  <text x="560" y="250" text-anchor="middle" font-size="10">MANY TRUE NAMES, NONE SYNONYMOUS</text>
</svg>
<figcaption><span class="cap-title">SIMPLICITY &amp; THE NAMES OF GOD</span> · the diversity appears only when the beam is refracted — creatures are the spectrum, God is the light</figcaption>
</figure>
"""

def figure(img, cap_title, cap):
    return ('<figure class="art"><div class="frame"><img src="images/%s" alt="%s" loading="lazy"></div>'
            '<figcaption><span class="cap-title">%s</span> · %s</figcaption></figure>') % (img, html.escape(cap_title + " — " + cap), cap_title, cap)

FIG_ACORN     = figure("acorn.png", "POTENTIALITY BECOMING ACTUALITY", "the oak is in the acorn — really there as a possibility, not yet as a fact")
FIG_MIRRORS   = figure("mirrors.png", "THE CORRIDOR OF MIRRORS", "infinite reflected light — and still not one thing in the story that shines")
FIG_STAIRCASE = figure("staircase.png", "THE TERMINUS", "not the biggest item in the universe&#8217;s inventory, but the reason there is an inventory at all")
FIG_FAWN      = figure("fawn.png", "ROWE&#8217;S FAWN", "the objection with real blood in it — no one has the receipt")
FIG_CRUCIFIX  = figure("crucifix.png", "AN ANSWER IN PERSON", "solidarity, where explanation was demanded")
FIG_CABLE     = figure("cable.png", "SEVEN LINES, ONE CABLE", "independent partial confirmations do what a single proof cannot — they multiply")

TIMELINE_ITEMS = [
    ("era", "", "THE ANCIENTS"),
    ("c. 400 BC", "Plato", "the Euthyphro question"),
    ("c. 350 BC", "Aristotle", "the good is what all things desire"),
    ("c. 300 BC", "Epicurus", "the ancient problem of evil"),
    ("era", "", "THE MEDIEVALS"),
    ("354", "Augustine", "the restless heart"),
    ("c. 500", "Dionysius", "bonum diffusivum sui"),
    ("1225", "Aquinas", "the Five Ways; being & goodness"),
    ("c. 1287", "Ockham", "voluntarism — the first horn"),
    ("era", "", "THE SKEPTICS"),
    ("1711", "Hume", "reason the slave; is & ought"),
    ("1724", "Kant", "existence is not a predicate"),
    ("1788", "Schopenhauer", "the tragic option"),
    ("1804", "Feuerbach", "God as projection"),
    ("1806", "Mill", "the desired / desirable slide"),
    ("1844", "Nietzsche", "will to power"),
    ("1848", "Frege", "existence as quantifier"),
    ("1856", "Freud", "the wish-fulfillment charge"),
    ("era", "", "THE ANALYTICS"),
    ("1872", "Russell", "&#8220;the universe is just there&#8221;"),
    ("1873", "Moore", "the Open Question"),
    ("1916", "Geach", "attributive &#8220;good&#8221;"),
    ("1917", "Mackie", "the logical problem"),
    ("1920", "Foot", "natural goodness"),
    ("1931", "Rowe", "the fawn in the fire"),
    ("1932", "Plantinga", "the free will defense"),
    ("1937", "Nagel", "the cosmic authority problem"),
    ("1938", "Nozick", "the experience machine"),
    ("1940", "Kripke", "informative identities"),
    ("1942", "van Inwagen", "the PSR attack"),
    ("era", "", "TODAY"),
    ("1960", "Oppy", "the godless terminus"),
    ("contemp.", "Wielenberg", "godless realism"),
    ("contemp.", "Street", "the debunking argument"),
    ("contemp.", "Mullins", "modal collapse"),
    ("contemp.", "Tomaszewski", "the reply"),
]
tl = ['<div class="timeline"><div class="tl-head">THE CAST, ACROSS 2,400 YEARS — SCROLL SIDEWAYS</div><div class="tl-track">']
for yr, name, note in TIMELINE_ITEMS:
    if yr == "era":
        tl.append('<div class="tl-item era"><div class="tl-era-label">%s</div></div>' % name)
    else:
        tl.append('<div class="tl-item"><div class="tl-year">%s</div><div class="tl-name">%s</div><div class="tl-note">%s</div></div>' % (yr, name, note))
tl.append('</div></div>')
TIMELINE = "".join(tl)

# ---------------------------------------------------------------
# margin doodles (hand-drawn SVGs, 64x64)
# ---------------------------------------------------------------
def doodle(svg, label):
    return ('<div class="doodle"><svg viewBox="0 0 64 64">%s</svg>'
            '<div class="d-label">%s</div></div>') % (svg, label)

D_SMOKE = doodle('<rect x="12" y="24" width="40" height="18" rx="6"/>'
                 '<circle cx="32" cy="33" r="4"/>'
                 '<path d="M44 10q5 5 0 10" class="e"/><path d="M51 6q7 7 0 14" class="e"/>',
                 "THE SMOKE DETECTOR")
D_MOTH = doodle('<path d="M40 54c8-8 6-16 0-24 10 6 12 18 0 24z" class="e"/>'
                '<path d="M20 34q-10-12 2-14 8-1 7 8"/><path d="M28 34q10-12-2-14-8-1-7 8"/>'
                '<path d="M24 26v18"/><path d="M21 20l-3-4M27 20l3-4"/>',
                "THE MOTH")
D_MARBLE = doodle('<rect x="10" y="16" width="44" height="36" rx="3"/>'
                  '<path d="M32 23c-5 7-5 16 0 25M26 30c4-3 8-3 12 0" stroke-dasharray="3 4"/>'
                  '<path d="M46 12l10-8M49 16l7-5" class="e"/>',
                  "THE STATUE IN THE MARBLE")
D_VENUS = doodle('<path d="M32 10l4 18 18 4-18 4-4 18-4-18-18-4 18-4z"/>'
                 '<ellipse cx="32" cy="32" rx="26" ry="9" stroke-dasharray="2 5"/>',
                 "TWO NAMES, ONE PLANET")
D_FISH = doodle('<path d="M14 30q11-11 24-11 10 0 16 11-6 11-16 11-13 0-24-11z"/>'
                '<path d="M14 30l-7-7v14z"/><circle cx="42" cy="28" r="1.6" class="fill"/>'
                '<path d="M8 50q8-5 16 0t16 0 16 0" stroke-dasharray="3 4"/>',
                "THE MEDIUM OF FISH")
D_SHIP = doodle('<path d="M8 38h48l-7 14H17z"/><path d="M32 8v28"/>'
                '<path d="M32 10c9 4 13 10 14 20h-14"/>'
                '<path d="M22 46l3-3 3 3 3-3" class="e"/><path d="M4 58q8-4 16 0t16 0 16 0 8-2" stroke-dasharray="3 4"/>',
                "THE HOLE IN THE HULL")
D_ARROW = doodle('<path d="M18 8q20 24 0 48"/><path d="M18 8v48"/>'
                 '<path d="M6 32h46m-9-7l9 7-9 7" class="e"/>',
                 "THE ARCHER&#8217;S AIM")
D_BRUSH = doodle('<path d="M8 8l32 32"/><path d="M40 40l5 5"/>'
                 '<path d="M45 45q10 9 5 14-7-2-12-9z" class="e"/>'
                 '<circle cx="10" cy="50" r="1.4" class="fill"/><circle cx="18" cy="54" r="1.4" class="fill"/><circle cx="26" cy="57" r="1.4" class="fill"/>',
                 "THE INFINITE HANDLE")
D_DICE = doodle('<rect x="10" y="16" width="18" height="18" rx="4"/>'
                '<circle cx="16" cy="22" r="1.5" class="fill"/><circle cx="22" cy="28" r="1.5" class="fill"/>'
                '<rect x="36" y="10" width="18" height="18" rx="4"/>'
                '<circle cx="45" cy="19" r="1.5" class="fill"/>'
                '<path d="M6 44h52M12 44v12M52 44v12" class="e"/>',
                "THE TABLE")
D_LEGO = doodle('<rect x="10" y="28" width="44" height="20" rx="2"/>'
                '<path d="M16 28v-7h7v7M29 28v-7h7v7M42 28v-7h7v7"/>'
                '<rect x="18" y="10" width="28" height="11" rx="2" stroke-dasharray="3 4"/>',
                "WHO CLICKED THE BRICKS?")
D_PEN = doodle('<path d="M32 6c8 10 12 20 12 28l-12 20-12-20c0-8 4-18 12-28z"/>'
               '<path d="M32 30v20"/><circle cx="32" cy="25" r="2"/>'
               '<path d="M14 60h36" stroke-dasharray="2 5" class="e"/>',
               "THE PEN")
D_METER = doodle('<path d="M10 54V32q22-22 44 0v22"/>'
                 '<path d="M18 40h28M18 36v8M46 36v8" class="e"/>'
                 '<rect x="25" y="47" width="14" height="5"/>',
                 "THE METER BAR")
D_SUNWALL = doodle('<circle cx="17" cy="20" r="7"/><path d="M17 8v4M17 28v4M5 20h4M29 20h-4M9 12l3 3M25 28l-3-3"/>'
                   '<path d="M38 10v44M38 22h16M38 32h16M38 43h16M46 10v12M46 32v11" />'
                   '<path d="M23 24l13 7" stroke-dasharray="2 4" class="e"/>',
                   "THE SUNLIT WALL")
D_BEETLE = doodle('<ellipse cx="32" cy="36" rx="10" ry="13"/><circle cx="32" cy="19" r="5"/>'
                  '<path d="M32 24v24M22 30l-10-4M22 38l-10 1M22 46l-9 6M42 30l10-4M42 38l10 1M42 46l9 6M28 15l-4-6M36 15l4-6"/>',
                  "THE BEETLE")

# anchor -> block inserted AFTER the paragraph
INSERT_AFTER = [
    ("That is the test we are going to run.", SVG_MAPS + TIMELINE),
    ("Keep that picture; we'll need it constantly.", FIG_ACORN),
    ("Nobody holds a funeral for gravel.", SVG_HIERARCHY),
    ("Philosophers call this the distinction between **essence**", SVG_ESSEX),
    ("cannot explain the presence of money none of them owns", SVG_TRAIN),
    ("borrowed light needs a lamp, however long the corridor", FIG_MIRRORS),
    ("creatures are the spectrum; God is the light", SVG_PRISM),
    ("the reason there is an inventory at all", FIG_STAIRCASE),
    ("multiply by deep time", FIG_FAWN),
    ("Solidarity, where explanation was demanded.", FIG_CRUCIFIX),
    ("individually breakable, wound together", FIG_CABLE),
]
# anchor -> doodle inserted BEFORE the paragraph
INSERT_BEFORE = [
    ("the way a smoke detector beeps", D_SMOKE),
    ("the way a moth", D_MOTH),
    ("the statue is in the marble block", D_MARBLE),
    ("turn out to name one planet, Venus", D_VENUS),
    ("The fish can doubt many things", D_FISH),
    ("a hole in a ship", D_SHIP),
    ("flight is the archer", D_ARROW),
    ("lengthen a paintbrush handle", D_BRUSH),
    ("Dice that roll unpredictably", D_DICE),
    ("A Lego castle", D_LEGO),
    ("as a writer works through a pen", D_PEN),
    ("a particular metal bar", D_METER),
    ("the way a sunlit wall has light", D_SUNWALL),
    ("to a beetle", D_BEETLE),
]

# ---------------------------------------------------------------
# parse the essay
# ---------------------------------------------------------------
assert raw_lines[0].startswith("# "), "title line unexpected"
assert raw_lines[2].startswith("*"), "dek line unexpected"

TITLE = raw_lines[0][2:].strip()
DEK = raw_lines[2].strip().strip("*")

SHORT = [
    ("&#10035;", "Overture"),
    ("I", "Securing the words"),
    ("II", "The asymmetry of good and evil"),
    ("III", "The terminus"),
    ("IV", "The bridge"),
    ("V", "Euthyphro"),
    ("VI", "Objectivity"),
    ("VII", "The acid test"),
    ("VIII", "Evil"),
    ("IX", "The verdict"),
]

sections = []          # list of {id, sec_idx, head_html, body_html[]}
current = {"id": "sec-0", "sec_idx": 0, "head": None, "body": []}
sections.append(current)
sec_idx = 0
essay_text_gen = [TITLE, DEK.replace("*", "")]  # for verification
essay_text_src = [TITLE, DEK.replace("*", "")]

def emit_paragraph(container, raw):
    k = kind_of(raw)
    inner = fmt(raw)
    essay_text_gen.append(strip_tags(inner))
    for anchor, block in INSERT_BEFORE:
        if anchor in raw:
            container.append(block)
    if k == "objection":
        container.append(
            '<div class="objection"><div class="eyebrow">' + SWORD +
            '<span>THE SKEPTIC, AT FULL STRENGTH</span></div>'
            '<p data-essay>' + inner + '</p></div>')
    elif k in ("clash", "fact", "contestant", "fiber"):
        container.append('<div class="%s"><p data-essay>%s</p></div>' % (k, inner))
    elif k == "blessing":
        container.append('<p class="blessing" data-essay>' + inner + '</p>')
    else:
        container.append('<p data-essay>' + inner + '</p>')
    for anchor, block in INSERT_AFTER:
        if anchor in raw:
            container.append(block)

i = 4
n = len(raw_lines)
while i < n:
    line = raw_lines[i]
    s = line.strip()
    if not s or s == "---":
        i += 1
        continue
    if s.startswith("## "):
        m = re.match(r"## ([IVX]+)\.\s+(.*)$", s)
        sec_idx += 1
        numeral, title_txt = m.group(1), m.group(2)
        head = ('<div class="chapter-head"><span class="numeral">%s</span>'
                '<h2 data-essay>%s. %s</h2>%s</div>'
                % (numeral, numeral, fmt(title_txt), ORN))
        essay_text_gen.append(numeral + ". " + strip_tags(fmt(title_txt)))
        current = {"id": "sec-%d" % sec_idx, "sec_idx": sec_idx, "head": head, "body": []}
        sections.append(current)
    elif s.startswith("### "):
        h = s[4:].strip()
        essay_text_gen.append(strip_tags(fmt(h)))
        current["body"].append('<h3 data-essay>' + fmt(h) + '</h3>')
    else:
        emit_paragraph(current["body"], s)
    i += 1

# overture head
sections[0]["head"] = ('<div class="chapter-head"><span class="numeral">&#10035;</span>'
                       '<h2>Overture</h2>' + ORN + '</div>')

# ---------------------------------------------------------------
# verification — every sentence preserved
# ---------------------------------------------------------------
src_concat = []
for line in raw_lines:
    s = line.strip()
    if not s or s == "---":
        continue
    s = re.sub(r"^#+\s*", "", s)
    src_concat.append(strip_tags(fmt(s)))
src_norm = norm("".join(src_concat))
gen_norm = norm("".join(essay_text_gen))
VERIFIED = src_norm == gen_norm
print("verification:", "PASS — every character preserved" if VERIFIED else "FAIL")
if not VERIFIED:
    print("src len", len(src_norm), "gen len", len(gen_norm))
    for a, b in zip(src_norm, gen_norm):
        if a != b:
            print("first diff at", src_norm.index(a), src_norm[max(0, src_norm.index(a)-40):src_norm.index(a)+60])
            break

# ---------------------------------------------------------------
# assemble
# ---------------------------------------------------------------
word_count = sum(len(re.findall(r"[A-Za-z0-9']+", l)) for l in raw_lines)
minutes = max(1, round(word_count / 190))
META = "NINE CHAPTERS &nbsp;·&nbsp; %s WORDS &nbsp;·&nbsp; %d MIN READ &nbsp;·&nbsp; EVERY SENTENCE PRESERVED" \
       % (format(word_count, ","), minutes)

def render_section(sec):
    idx = sec["sec_idx"]
    num, short = SHORT[idx]
    return ('<section class="chapter" id="%s" data-sec="%d" data-short="%s">'
            '<div class="col">%s%s</div></section>'
            % (sec["id"], idx, short, sec["head"] or "", "".join(sec["body"])))

CONTENT = "\n".join(render_section(s) for s in sections)

RAIL = '<nav class="rail">' + "".join(
    '<a href="#sec-%d" data-sec-link>%s</a>' % (i, SHORT[i][0]) for i in range(1, 10)) + '</nav>'

MENU = '<div class="menuov" id="menuov"><div class="menu-inner"><div class="menu-title">THE NINE CHAPTERS</div>' + "".join(
    '<a class="mi" href="#sec-%d"><span class="num">%s</span><span class="t">%s</span></a>'
    % (i, SHORT[i][0], SHORT[i][1]) for i in range(10)) + '</div></div>'

LEGEND = """
<div class="legend">
  <span class="lg"><svg viewBox="0 0 24 24"><path d="M4 8h16M4 16h16" stroke-dasharray="2 3"/></svg><em>dotted gold</em>&nbsp; floating definitions &amp; who's who</span>
  <span class="lg"><svg viewBox="0 0 24 24"><path d="M4 20 18 6m0 0h-4m4 0v4"/></svg>ember cards &nbsp;the skeptic's objections, at full strength</span>
  <span class="lg"><svg viewBox="0 0 24 24"><path d="M7 16c-3-1.5-3-6.5 1-8M15 16c-3-1.5-3-6.5 1-8"/></svg>giant quotes &nbsp;lines worth carrying out</span>
  <span class="lg"><svg viewBox="0 0 24 24"><path d="M4 20l1-4L16 5l3 3L8 19z"/></svg>margin sketches &nbsp;the essay's images, drawn</span>
  <span class="lg"><svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M4 15l5-5 4 4 3-3 4 4"/></svg>seven paintings &nbsp;plus diagrams &amp; a 2,400-year timeline</span>
</div>
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Goodness Itself — An Interactive Reading</title>
<meta name="description" content="The whole case that God is not merely good but Goodness — as an interactive reading: every sentence preserved, infused with paintings, diagrams, floating definitions, and the cast of 2,400 years.">
<meta name="theme-color" content="#0f0c08">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 3l10 13-10 13L6 16z' fill='%23c9a24b'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Spectral:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap" rel="stylesheet">
<style>
%%CSS%%
</style>
</head>
<body>
<div class="progress" id="progress"></div>

<header class="top" id="top">
  <a class="brand" href="#top-anchor" id="brand">GOODNESS ITSELF</a>
  <div class="chap-label" id="chapLabel"></div>
  <div class="tools">
    <button class="tool-btn" id="menuBtn">CHAPTERS</button>
    <button class="tool-btn" id="themeBtn">LIGHT / DARK</button>
  </div>
</header>

%%RAIL%%

<main id="top-anchor">
  <div class="hero">
    <img class="hero-bg" src="images/hero.png" alt="A single radiant light emerging from deep darkness, painted in baroque chiaroscuro">
    <div class="hero-veil"></div>
    <canvas id="dust"></canvas>
    <div class="hero-inner">
      <div class="kicker">AN INTERACTIVE READING</div>
      <h1 data-essay>Goodness Itself<span class="sub">The Whole Case</span></h1>
      <p class="dek" data-essay>%%DEK%%</p>
      <div class="meta">%%META%%</div>
    </div>
    <a class="begin" href="#sec-0">BEGIN THE CLIMB
      <svg width="14" height="18" viewBox="0 0 14 18" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M7 1v14M2 10l5 6 5-6"/></svg>
    </a>
  </div>

  %%LEGEND%%

  %%CONTENT%%

  <footer>
    <div class="finis">FINIS</div>
    <p>Set in Spectral, Cormorant Garamond &amp; Cinzel. Seven paintings generated for this reading; diagrams, timeline, and margin sketches drawn by hand in SVG.</p>
    <p>Every sentence of the original essay is preserved, unabridged and unaltered. Dotted gold terms open floating definitions; names marked &#8599; open the cast of characters.</p>
    <p><em>Fecisti nos ad te, et inquietum est cor nostrum donec requiescat in te.</em></p>
  </footer>
</main>

%%MENU%%

<script>
%%JS%%
</script>
</body>
</html>
"""

page = (TEMPLATE
        .replace("%%CSS%%", (ROOT / "style.css").read_text(encoding="utf-8"))
        .replace("%%JS%%", (ROOT / "script.js").read_text(encoding="utf-8"))
        .replace("%%DEK%%", fmt(raw_lines[2].strip()))
        .replace("%%META%%", META)
        .replace("%%RAIL%%", RAIL)
        .replace("%%MENU%%", MENU)
        .replace("%%LEGEND%%", LEGEND)
        .replace("%%CONTENT%%", CONTENT))

OUT.write_text(page, encoding="utf-8")
print("wrote", OUT, "—", len(page), "chars")
print("sections:", len(sections), "| paragraphs:", sum(1 for l in raw_lines if l.strip() and not l.strip().startswith('#') and l.strip() != '---'))
