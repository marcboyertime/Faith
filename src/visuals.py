from __future__ import annotations

import html


def _shell(spec: dict, body: str, essay_id: str) -> str:
    return f'''<figure class="support-visual visual-{html.escape(spec["kind"])}" data-supporting="true" id="{html.escape(spec["id"])}" aria-labelledby="{html.escape(spec["id"])}-title">
  <div class="visual-top"><span>{html.escape(spec["id"])}</span><span>{html.escape(spec.get("label", "ARGUMENT MAP"))}</span></div>
  <h3 id="{html.escape(spec["id"])}-title">{html.escape(spec["title"])}</h3>
  {body}
  <figcaption>{html.escape(spec.get("caption", ""))}</figcaption>
</figure>'''


def render_visual(spec: dict, essay_id: str, asset_prefix: str) -> str:
    kind = spec.get("kind", "map")
    if kind == "pull":
        return f'''<aside class="support-pull" data-supporting="true" id="{html.escape(spec["id"])}"><blockquote>“{html.escape(spec["quote"])}”</blockquote><span>{html.escape(spec.get("label", "A LINE TO CARRY"))}</span></aside>'''
    if kind == "image":
        asset = html.escape(spec["asset"])
        body = f'<div class="image-frame"><img src="{asset_prefix}assets/{asset}" alt="{html.escape(spec.get("alt", spec["title"]))}" loading="lazy"></div>'
        return _shell(spec, body, essay_id)
    if kind == "timeline":
        body = '<div class="visual-timeline"><span>CRUCIFIXION<br><b>~30</b></span><span>EARLIEST<br>PROCLAMATION</span><span>PAULINE LETTERS<br><b>48–late 50s</b></span><span>MARK<br><b>65–75</b></span><span>MATTHEW / LUKE<br><b>80–95</b></span><span>JOHN<br><b>90s</b></span></div>'
        return _shell(spec, body, essay_id)
    if kind == "claim-map":
        body = '<div class="claim-layers"><span class="layer history">HISTORY <b>what happened?</b></span><span class="layer inference">INFERENCE <b>what best explains it?</b></span><span class="layer philosophy">PHILOSOPHY <b>what worlds are live?</b></span><span class="layer theology">THEOLOGY <b>what does it mean?</b></span><span class="layer doctrine">CATHOLIC TEACHING <b>what the Church confesses</b></span></div>'
        return _shell(spec, body, essay_id)
    if kind == "afterlife-map":
        body = '<div class="afterlife-map"><span>CONTINUED SOUL</span><i>≠</i><span>GHOST / APPARITION</span><i>≠</i><span>RESUSCITATION</span><i>≠</i><span>TRANSFORMED RESURRECTION</span></div><p class="visual-note">Same vocabulary family, different claims. The final node is not a synonym for survival.</p>'
        return _shell(spec, body, essay_id)
    if kind == "dependence":
        body = '<div class="dependence-tree"><span class="trunk">PRE-PAULINE FORMULA</span><div><span>PAUL</span><span>MARK</span><span>JOHN <small>partial / argued</small></span></div><div><span>MATTHEW ← MARK</span><span>LUKE–ACTS ← MARK + OTHER MATERIAL</span></div></div><p class="visual-note">The stream count is 2–4, not one independent witness per document.</p>'
        return _shell(spec, body, essay_id)
    if kind == "creed":
        body = '<div class="creed-spine"><span> DIED <b>EVENT</b></span><span>BURIED <b>EVENT</b></span><span>RAISED <b>EVENT</b></span><span>APPEARED <b>EVENT</b></span><span>NAMED <b>RECIPIENTS</b></span></div><p class="visual-note">“For our sins” and “according to the Scriptures” are meaning-claims, not extra event clauses.</p>'
        return _shell(spec, body, essay_id)
    if kind == "witness":
        body = '<div class="witness-rings"><span class="ring ring-a">PETER / TWELVE</span><span class="ring ring-b">JAMES · PAUL</span><span class="ring ring-c">FIVE HUNDRED · ALL THE APOSTLES</span></div>'
        return _shell(spec, body, essay_id)
    if kind == "gospel-table":
        body = '''<div class="comparison" data-switcher="gospels"><div class="switcher" role="tablist"><button type="button" data-value="mark" aria-selected="true">MARK</button><button type="button" data-value="matthew" aria-selected="false">MATTHEW</button><button type="button" data-value="luke" aria-selected="false">LUKE</button><button type="button" data-value="john" aria-selected="false">JOHN</button></div><div class="comparison-grid"><span>Visitors</span><span data-panel="mark">Women</span><span data-panel="matthew" hidden>Women + Mary</span><span data-panel="luke" hidden>Women</span><span data-panel="john" hidden>Mary Magdalene</span><span>Geography</span><span data-panel="mark">Galilee promise</span><span data-panel="matthew" hidden>Galilee</span><span data-panel="luke" hidden>Jerusalem</span><span data-panel="john" hidden>Jerusalem + Galilee</span></div></div>'''
        return _shell(spec, body, essay_id)
    if kind == "hypotheses":
        body = '<div class="hypothesis-grid"><article><b>RESURRECTION</b><span>scope: wide</span><span>prior: costly</span><span>fit: conditional on theism</span></article><article><b>COMPOSITE NATURALISM</b><span>scope: wide</span><span>auxiliaries: many</span><span>status: strongest rival</span></article><article><b>INDIVIDUAL VISIONS</b><span>fit: partial</span><span>groups / tomb: debt</span></article><article><b>SUSPENSION</b><span>possible</span><span>cost: leaves the cluster ununified</span></article></div>'
        return _shell(spec, body, essay_id)
    if kind == "bayes":
        body = '<div class="bayes-river"><span>PRIOR</span><i></i><span>DEATH</span><i></i><span>EARLY CLAIM</span><i></i><span>APPEARANCES</span><i></i><span>POSTERIOR</span></div><p class="visual-note">The numerals are intentionally absent: background assumptions and likelihood judgments do the work, not a fake percentage.</p>'
        return _shell(spec, body, essay_id)
    if kind == "cumulative":
        body = '<div class="convergence"><span>DEATH</span><span>EARLY PROCLAMATION</span><span>APPEARANCE CLAIMS</span><span>MISSING BODY</span><span>JEWISH MUTATION</span><b>ONE CUMULATIVE CASE</b></div>'
        return _shell(spec, body, essay_id)
    if kind == "maps":
        body = '<div class="map-pair"><div><b>ORDINARY MAP</b><span>death → grief → memory → movement</span></div><div><b>CHRISTIAN MAP</b><span>death → divine action → transformed life → witness</span></div></div>'
        return _shell(spec, body, essay_id)
    if kind == "afterlife":
        body = '<div class="afterlife-map"><span>SOUL CONTINUES</span><i>≠</i><span>VISION / APPARITION</span><i>≠</i><span>GENERAL RESURRECTION</span><i>≠</i><span>JESUS: ONE MAN FIRST</span></div>'
        return _shell(spec, body, essay_id)
    if kind == "hierarchy":
        body = '<div class="goodness-scale"><span>STONE · IS</span><span>TREE · IS, LIVES</span><span>ANIMAL · PERCEIVES</span><span>HUMAN · KNOWS THAT SHE IS</span><b>MORE ACTUALITY →</b></div>'
        return _shell(spec, body, essay_id)
    if kind == "essence":
        body = '<div class="essence-diagram"><span>WHAT IT IS</span><i>≠</i><span>THAT IT IS</span><b>GAP</b><strong>WHAT = THAT<br><small>no gap</small></strong></div>'
        return _shell(spec, body, essay_id)
    if kind == "train":
        body = '<div class="train-diagram"><span>CAR</span><span>CAR</span><span>CAR</span><b>ENGINE</b><small>has motion of itself</small></div>'
        return _shell(spec, body, essay_id)
    if kind == "prism":
        body = '<div class="prism-diagram"><b>ONE SIMPLE ACT</b><i>→</i><span>being</span><span>goodness</span><span>truth</span><span>beauty</span></div>'
        return _shell(spec, body, essay_id)
    if kind == "goodness-timeline":
        body = '<div class="visual-timeline goodness-history"><span>PLATO<br><b>c. 400 BC</b></span><span>ARISTOTLE<br><b>c. 350 BC</b></span><span>AUGUSTINE<br><b>354</b></span><span>AQUINAS<br><b>1225</b></span><span>HUME<br><b>1711</b></span><span>MOORE<br><b>1873</b></span><span>OPPY<br><b>1960</b></span></div>'
        return _shell(spec, body, essay_id)
    if kind == "goodness-maps":
        body = '<div class="map-pair"><div><b>BRUTE FACTS</b><span>existence → no further question</span></div><div><b>THE MAP THAT KEEPS WORKING</b><span>being → actuality → goodness → source</span></div></div>'
        return _shell(spec, body, essay_id)
    return _shell(spec, '<div class="generic-visual"><span>STRUCTURE</span><b>evidence → inference → judgment</b></div>', essay_id)
