/* ============================================================
   GOODNESS ITSELF — interactive layer
   floating definitions · who's-who · pop-out quotations
   scroll reveals · progress · particles · theme
   ============================================================ */

/* ---------- the dictionary: concepts & people ----------
   k: key · pat: regex pattern (longest first wins) · t: term|person
   n: card title · d: definition/bio · l: optional link          */

const ENTRIES = [
  /* ===== LATIN & TECHNICAL TERMS ===== */
  { k:"esse", t:"term", n:"Ipsum esse subsistens", pat:"ipsum esse subsistens",
    d:`Latin: "Being itself, subsisting." The classical formula for God: not a being among beings, but the sheer act of existing, standing on its own rather than being a feature of something else.` },
  { k:"bonum", t:"term", n:"Ipsum bonum subsistens", pat:"ipsum bonum subsistens",
    d:`Latin: "Goodness itself, subsisting." The essay's central claim: the same reality as ipsum esse subsistens, read under the aspect of what draws and completes.` },
  { k:"subratione", t:"term", n:"Sub ratione boni", pat:"sub ratione boni",
    d:`Latin: "under the aspect of good." Aquinas's claim that the will can only aim at what is presented to it dressed as a good — even evil must disguise itself to be willed.` },
  { k:"bonumdiff", t:"term", n:"Bonum diffusivum sui", pat:"bonum diffusivum sui",
    d:`Latin: "the good pours itself out." The axiom the tradition adopted from Dionysius: goodness by its nature communicates rather than hoards.` },
  { k:"exnihilo", t:"term", n:"Ex nihilo", pat:"ex nihilo",
    d:`Latin: "from nothing." Creation required nothing and nothing was owed: existence is, strictly, gift — the precondition of there being anyone to receive gifts.` },
  { k:"suigeneris", t:"term", n:"Sui generis", pat:"sui generis",
    d:`Latin: "of its own kind" — irreducible, explainable as nothing else.` },
  { k:"aposteriori", t:"term", n:"A posteriori", pat:"a posteriori|a priori",
    d:`Reasoning that starts from observed reality and asks what it requires — as opposed to a priori reasoning, which starts from concepts alone.` },

  /* ===== SECTION I — THE WORDS ===== */
  { k:"firstprinciples", t:"term", n:"First principles", pat:"first principles",
    d:`The starting points of thought that can't be derived from anything deeper, because there is nothing deeper. The rules of logic are the classic case: you can't argue for them without using them.` },
  { k:"metaphysics", t:"term", n:"Metaphysics", pat:"metaphysics",
    d:`A big theory about what reality fundamentally is. The essay's point: "at bottom there is no reason, only fact" is one too — not the neutral default it pretends to be.` },
  { k:"naturaltheology", t:"term", n:"Natural theology", pat:"natural theology",
    d:`Knowledge of God by reason alone, from what nature is and does — no scripture, no revelation. This essay is an exercise in it.` },
  { k:"thomist", t:"term", n:"Thomist", pat:"Thomist",
    d:`A follower of Thomas Aquinas (1225–1274), the philosopher-monk whose system this essay examines. Crucially: the Thomist claims to discover what "good" means, not to stipulate it.`,
    l:"https://en.wikipedia.org/wiki/Thomism" },
  { k:"actuality", t:"term", n:"Actuality", pat:"actuality",
    d:`Realness-in-action: not just being there, but being fully at work as the kind of thing you are — capacities switched on and running. The acorn's program fully run is the oak.` },
  { k:"potentiality", t:"term", n:"Potentiality", pat:"potentiality",
    d:`A real but unrealized capacity — the oak in the acorn, the statue in the marble. Not nothing; not yet operative. Pure act is actuality with none of this left over.` },
  { k:"pureact", t:"term", n:"Pure act", pat:"pure act",
    d:`Actuality without remainder: no unrealized capacities, nothing switched off. The terminus of Section III's argument — and, the essay argues, identical with unlimited goodness.` },
  { k:"convertibility", t:"term", n:"Convertibility", pat:"convertibility",
    d:`The medieval thesis that "being" and "good" name one reality under two descriptions — from the side of what is, and from the side of what pulls. Like "morning star" and "evening star" naming Venus.` },
  { k:"transcendental", t:"term", n:"Transcendentals", pat:"transcendental",
    d:`Properties so general they cross every category and apply to everything that is: being, unity, truth, goodness.` },
  { k:"formalobject", t:"term", n:"Formal object", pat:"formal object",
    d:`The built-in target of a faculty — what it is for. Light is the eye's formal object; truth, the intellect's; the good, the will's.` },
  { k:"intentionality", t:"term", n:"Intentionality", pat:"intentionality|intentional",
    d:`In philosophy of mind: "aboutness." A thought or desire is always of or about something, the way an arrow is pointed somewhere. Brentano made it the mark of the mental.` },
  { k:"falsifiable", t:"term", n:"Falsifiable", pat:"falsifiable",
    d:`Sticking its neck out: a claim that could die on a counterexample. Section I's analysis names the three counterexample-forms that would kill it — an invitation standing open for seven hundred years.`,
    l:"https://en.wikipedia.org/wiki/Falsifiability" },
  { k:"openquestion", t:"term", n:"The Open Question Argument", pat:"Open Question Argument|open question",
    d:`G. E. Moore's 1903 argument: if "this has property X — but is it good?" stays a meaningful question, then "good" can't mean X. Section I answers it with informative identities.` },
  { k:"infoidentity", t:"term", n:"Informative identity", pat:"informative identities|informative identity",
    d:`A true statement that two descriptions pick out one reality — "water is H₂O," "the morning star is the evening star" — discovered by investigation, not read off the dictionary. The claimed status of "goodness is actuality."` },
  { k:"attributive", t:"term", n:"Attributive adjectives", pat:"attributive",
    d:`Geach's category: adjectives that can't be split from their noun. A "good knife" is good as a knife; you can't factor it into "knife + good" the way "red car" factors into "car + red."` },
  { k:"ontoscale", t:"term", n:"Ontological scale", pat:"ontological scale",
    d:`A scale of how much being something has: a stone is; a tree lives; an animal perceives; a human knows that she is. Each step up is a wider range of powers, a deeper openness to reality.` },
  { k:"predicate", t:"term", n:"Predicate", pat:"predicate",
    d:`In logic, a feature attributed to a subject. Kant's famous claim: existence is not a real predicate — "…and it exists" adds no feature to a thing's description.` },
  { k:"quantifier", t:"term", n:"Quantifier", pat:"quantifier",
    d:`The "there is at least one…" operator of modern logic — how Frege expresses existence: not a property of things, but of concepts that have instances.`,
    l:"https://en.wikipedia.org/wiki/Quantifier_(logic)" },
  { k:"ontarg", t:"term", n:"The ontological argument", pat:"ontological argument",
    d:`The argument (St Anselm's) that tries to extract God's existence from the mere concept of God. Kant's "existence is not a predicate" was built to kill it. Section III's argument runs the other way: from existing things, not from a concept.`,
    l:"https://plato.stanford.edu/entries/ontological-arguments/" },

  /* ===== SECTION II — PRIVATION ===== */
  { k:"privation", t:"term", n:"Privation", pat:"privation\\w*",
    d:`The absence of a good that ought to be present given a thing's nature. Darkness in a coal cellar: mere absence. Blindness in an eye: privation — because the eye's nature specifies sight as its due.` },
  { k:"phenomenology", t:"term", n:"Phenomenology", pat:"phenomenolog\\w*",
    d:`Nothing scarier than: the careful description of things exactly as they actually show up in experience.` },
  { k:"evilgod", t:"term", n:"The evil god challenge", pat:"evil god challenge",
    d:`Stephen Law's argument: any evidence for a good God can be mirrored for an evil one — so both are absurd. Section II's asymmetry is the essay's answer: the mirror never existed.`,
    l:"https://en.wikipedia.org/wiki/Evil_God_challenge" },

  /* ===== SECTION III — THE CLIMB ===== */
  { k:"essence", t:"term", n:"Essence", pat:"essence",
    d:`What a thing is — its nature, its kind. In everything finite, the "what" never includes the "that": you can master unicorn anatomy without learning whether any exist.` },
  { k:"existence", t:"term", n:"Existence", pat:"existence",
    d:`That a thing is. In finite things existence is received — really had, but on loan. Section III asks where the loan-chain terminates.` },
  { k:"essordered", t:"term", n:"Essentially ordered series", pat:"essentially ordered series",
    d:`A chain of simultaneous, right-now dependence — every member transmitting a power it doesn't originate, all at once. A train of cars needs an engine, however many cars you add.` },
  { k:"humeedwards", t:"term", n:"The Hume–Edwards principle", pat:"Hume\u2013Edwards principle",
    d:`The claim that explaining each member of a series explains the whole. True for walls of bricks; demonstrably false for borrowed features — a corridor of mirrors still needs a lamp.` },
  { k:"compfallacy", t:"term", n:"Fallacy of composition", pat:"fallacy of composition",
    d:`Assuming what's true of the parts must be true of the whole — "every man has a mother, so mankind has a mother." Section III argues the cosmological case commits no such fallacy.` },
  { k:"brutefact", t:"term", n:"Brute fact", pat:"brute facticity|brute fact\\w*|selective brutalism",
    d:`A fact with no explanation at all — "it's just there." The essay's charge: everyone rejects brute facts everywhere except the one spot protecting their own worldview.` },
  { k:"psr", t:"term", n:"Principle of Sufficient Reason", pat:"Principle of Sufficient Reason|PSR",
    d:`The principle that contingent facts — facts that could have been otherwise — have explanations. The engine of the cosmological argument and, the essay notes, of all science.`,
    l:"https://plato.stanford.edu/entries/sufficient-reason/" },
  { k:"modallogic", t:"term", n:"Modal logic", pat:"modal logic",
    d:`The formal logic of possibility and necessity — "could have been" and "could not have been otherwise." Gale and Pruss use it to reach a necessary being from a weakened premise.` },
  { k:"necessarybeing", t:"term", n:"Necessary being", pat:"necessary being",
    d:`Something that could not fail to exist — whose essence just is to exist. Section III is a contest over what, if anything, deserves the title; its answer: only the absolutely simple qualifies.` },
  { k:"simplicity", t:"term", n:"Divine simplicity", pat:"divine simplicity|simplicity",
    d:`The doctrine that God has no parts, no separable features, no dials: essence identical with existence, attributes one simple act. The essay's structural requirement for a genuine stopping point.`,
    l:"https://plato.stanford.edu/entries/divine-simplicity/" },
  { k:"participation", t:"term", n:"Participation", pat:"participation",
    d:`Sharing-in: the way a sunlit wall has light without being light. Creatures have goodness by participation; the terminus simply is what creatures share in.` },

  /* ===== SECTION IV — THE BRIDGE ===== */
  { k:"propcause", t:"term", n:"Proportionate causality", pat:"proportionate causality",
    d:`The principle that whatever perfection exists in an effect must exist in its total cause in some manner: formally (as fire heats), virtually (as the chef has cake-capacity), or eminently (as white light "has" every color). No gifts from empty hands.` },
  { k:"emergence", t:"term", n:"Emergence", pat:"emergence",
    d:`When a whole shows properties its parts lack — wetness from non-wet molecules. Section IV argues emergence illustrates the virtual mode of proportionate causality rather than violating it.`,
    l:"https://en.wikipedia.org/wiki/Emergence" },
  { k:"motext", t:"term", n:"Motivational externalism", pat:"motivational externalism",
    d:`The view that knowing the good and being moved by it are separable — the psychopath's gap. Section IV argues the gap needs two things pure act lacks: composition and privation.` },
  { k:"actpotency", t:"term", n:"Act precedes potency", pat:"act precedes potency",
    d:`The principle that possibilities are rooted in actual powers: a possible statue exists only because actual marble and sculptors do. Erase all actuality and you erase the possibilities. Hence: no menu of divine natures.` },
  { k:"platonism", t:"term", n:"Platonism", pat:"Platonic\\w*|Platoni\\w*",
    d:`Plato's picture of a timeless realm of perfect Forms beyond the physical. Godless Platonism about value is Contestant Two in Section VI's tournament — and, the essay argues, drowns in infinitely many brute necessities.`,
    l:"https://en.wikipedia.org/wiki/Platonism" },
  { k:"powersmod", t:"term", n:"Powers-based modality", pat:"powers-based|powers ontolog\\w*|dispositional",
    d:`A leading school in current analytic metaphysics (Pruss, Jacobs, Vetter): possibility is grounded in the actual powers of actual things. Possibilities don't float; they inhere.` },
  { k:"brutecont", t:"term", n:"Brute contingency", pat:"brute contingency",
    d:`"Just how it is" in the bad sense: could have been otherwise, and there is no reason it isn't. An intellectual dead end — the naturalist's "the universe is just there."` },
  { k:"selfexp", t:"term", n:"Self-explanatory necessity", pat:"self-explanatory necessity",
    d:`Could not have been otherwise, and is intelligible through itself — that in which "what it is" and "that it is" are identical. Structurally the opposite of a brute fact, not a variant of one.` },
  { k:"nonrigid", t:"term", n:"Non-rigid designator", pat:"non-rigid designator\\w*",
    d:`A description that picks out different things in different circumstances — "the number of the apostles" designates twelve, but would have designated ten. Section IV's key to defusing modal collapse.`,
    l:"https://en.wikipedia.org/wiki/Rigid_designator" },
  { k:"cambridge", t:"term", n:"Cambridge relation", pat:"Cambridge relation",
    d:`A change in description with no change in the thing: Socrates becomes "shorter than Theaetetus" purely because Theaetetus grew — not one atom of Socrates changes. All the real change sits on one side of the relation.` },
  { k:"modalcollapse", t:"term", n:"Modal collapse", pat:"modal collapse",
    d:`The sharpest live objection to classical theism (R. T. Mullins): if God's one act is necessary, and that act is the creation of this world, isn't the world necessary? Answered in Section IV.`,
    l:"https://plato.stanford.edu/entries/divine-simplicity/" },

  /* ===== SECTION V — EUTHYPHRO ===== */
  { k:"euthyphro", t:"term", n:"The Euthyphro dilemma", pat:"Euthyphro dilemma|Euthyphro",
    d:`Plato's 2,400-year-old fork: is something good because God wills it (morality arbitrary), or does God will it because it is good (a standard above God)? Section V takes every horn, including the third.`,
    l:"https://en.wikipedia.org/wiki/Euthyphro_dilemma" },
  { k:"voluntarism", t:"term", n:"Voluntarism", pat:"voluntarism",
    d:`The view that whatever God commands is thereby good — championed by William of Ockham, fought by Aquinas and the Catholic mainstream precisely because it makes morality arbitrary.` },
  { k:"analogy", t:"term", n:"The doctrine of analogy", pat:"doctrine of analogy",
    d:`The teaching that words apply to God neither in exactly our sense (univocally) nor in a totally unrelated sense (equivocally), but stretched — truly, while exceeding our grip.` },
  { k:"naturallaw", t:"term", n:"Natural law", pat:"natural law",
    d:`The Catholic tradition that ethics is readable off what beings are and what fulfills them — morality as the grain of the wood, not a memo from headquarters; knowable, the Church teaches, without revelation.`,
    l:"https://plato.stanford.edu/entries/natural-law-ethics/" },

  /* ===== SECTION VI — OBJECTIVITY ===== */
  { k:"stance", t:"term", n:"Stance-independence", pat:"stance-independence|stance-independent|stance-dependent",
    d:`A fact is stance-independent when it doesn't obtain in virtue of anyone's contingent attitudes — when nobody's approving, desiring, or deciding is what makes it so. What people mean by moral objectivity.` },
  { k:"expressivism", t:"term", n:"Expressivism", pat:"expressivis\\w*",
    d:`The view that moral talk expresses attitudes rather than stating facts — "cruelty is wrong" as a vented preference, not a claim.`,
    l:"https://en.wikipedia.org/wiki/Expressivism" },
  { k:"errortheory", t:"term", n:"Error theory", pat:"error theory",
    d:`J. L. Mackie's view: all moral claims are simply false, since there's nothing for them to be true of. Contestant One — eliminated, Section VI argues, in the first person.` },
  { k:"ibe", t:"term", n:"Inference to the best explanation", pat:"inference to the best explanation",
    d:`Science's own reasoning form: which hypothesis explains all the data, most economically, with the fewest unexplained leftovers? Section VI's tournament is run as one.` },
  { k:"wielrealism", t:"term", n:"Robust normative realism", pat:"robust normative realism|godless Platonism|brute Platonism",
    d:`Erik Wielenberg's position: moral facts are real, necessary, and brute — floating free with no God needed. Normative: concerning oughts. Realism: really out there. Robust: unapologetically so.` },
  { k:"antirealism", t:"term", n:"Anti-realism", pat:"anti-realism",
    d:`The view that value isn't real: either all moral claims are false (error theory) or they were never claims at all (expressivism). Contestant One in the tournament.` },
  { k:"naturalgoodness", t:"term", n:"Natural goodness", pat:"natural goodness",
    d:`Philippa Foot's framework: goodness anchored in natures and their realization — a good wolf, a good oak, a good human, each measured by the flourishing of its kind. Section VI calls it the first half of the true story.` },
  { k:"teleology", t:"term", n:"Teleology", pat:"teleolog\\w*",
    d:`Directedness toward ends: hearts for pumping, struck matches for fire. The deep question of Section VI — is it real, and if so, what grounds it in things that cannot intend?` },
  { k:"physintent", t:"term", n:"Physical intentionality", pat:"physical intentionality",
    d:`George Molnar's arresting discovery: real dispositions are directed at manifestations that may never occur — the solubility of salt never wetted. Pointing-at-the-absent: the traditional signature of mind, found in physics.` },
  { k:"trilemma", t:"term", n:"Trilemma", pat:"trilemma",
    d:`A fork with three prongs — here: Humean coincidence, brute powers, or an ordering intellect. No comfortable horn.` },
  { k:"fifthway", t:"term", n:"The Fifth Way", pat:"Fifth Way",
    d:`Aquinas's fifth argument: ubiquitous directedness in mindless things requires an ordering intellect — the arrow's flight referred to the archer. Section VI reaches it without one pious word.`,
    l:"https://en.wikipedia.org/wiki/Five_Ways_(Aquinas)" },
  { k:"induction", t:"term", n:"Induction", pat:"induction",
    d:`Reasoning from observed cases to the next case — science's engine. Hume's pattern-only picture of causation famously found no rational basis for it.` },

  /* ===== SECTION VII — THE ACID ===== */
  { k:"debunk", t:"term", n:"Evolutionary debunking", pat:"debunk\\w*",
    d:`Sharon Street's argument: selection optimizes for fitness, not truth — so our moral convictions are explained without moral facts playing any role. Section VII pours the acid both ways.` },
  { k:"geneticfallacy", t:"term", n:"Genetic fallacy", pat:"genetic fallacy",
    d:`The mistake of thinking that explaining a belief's origin refutes its content. Genealogy convicts no one on either side; arguments must do the convicting.`,
    l:"https://en.wikipedia.org/wiki/Genetic_fallacy" },
  { k:"cosmicauthority", t:"term", n:"Cosmic authority problem", pat:"cosmic authority problem",
    d:`Thomas Nagel's confession: "I want atheism to be true… I don't want there to be a God." Section VII's point: wishes run both directions.` },
  { k:"defeater", t:"term", n:"Defeater", pat:"defeater",
    d:`A discovered reason to distrust a belief's source — which, once admitted, can spread to every belief the source produces, including the belief in naturalism itself.` },
  { k:"offtrack", t:"term", n:"Off-track premise", pat:"off-track premise",
    d:`What every debunking argument needs: the claim that the belief-producing process was not aimed at truth. Which, Section VII notes, depends on which worldview is true — the very question at issue.` },
  { k:"secondarycause", t:"term", n:"Secondary causation", pat:"secondary causation|instrumentality",
    d:`God working through natural processes as a writer works through a pen — instruments, not rivals. On theism, evolution is instrumentality; the genealogy is on-track by design.` },
  { k:"eaan", t:"term", n:"The evolutionary argument against naturalism", pat:"evolutionary argument against naturalism",
    d:`Plantinga's argument: selection sees behavior, not belief-content — adaptive behavior can ride on wildly false beliefs, so on naturalism the reliability of our faculties is low or inscrutable.`,
    l:"https://en.wikipedia.org/wiki/Evolutionary_argument_against_naturalism" },
  { k:"materialism", t:"term", n:"Materialism", pat:"materialism",
    d:`The view that the mind is wholly physical — brain and nothing more.` },
  { k:"naturalism", t:"term", n:"Naturalism", pat:"naturalis\\w*",
    d:`The view that the physical world is all there is. Its portfolio, per Section IX: existence brute, constants brute, teleology an accident, value unreal or stranded, reason's authority a spandrel.`,
    l:"https://en.wikipedia.org/wiki/Metaphysical_naturalism" },
  { k:"spandrel", t:"term", n:"Spandrel", pat:"spandrel",
    d:`An evolutionary by-product: a feature that arises as the side effect of other adaptations, not selected for itself. The skeptic's charge is that God is one.`,
    l:"https://en.wikipedia.org/wiki/Spandrel_(biology)" },
  { k:"epistemology", t:"term", n:"Epistemology", pat:"epistemolog\\w*|epistemic",
    d:`The theory of knowledge: what we should believe and why. "You ought to believe what the evidence supports" is a normative claim — which is why anti-realism can't run its own epistemology.` },
  { k:"expmachine", t:"term", n:"The experience machine", pat:"experience machine",
    d:`Robert Nozick's test: a device giving a lifetime of perfectly convincing experiences while you float in a tank. Nearly everyone recoils — we want the realities, not just the experiences of them.`,
    l:"https://en.wikipedia.org/wiki/Experience_machine" },
  { k:"humeslave", t:"term", n:"Reason, slave of the passions", pat:"slave of the passions",
    d:`Hume's picture: desires are original brute pushes, and reason only serves them. Section IV replies three ways — ending with the observation that Humean passions are appetites arising from lack.` },

  /* ===== SECTION VIII — EVIL & THE DOCUMENTS ===== */
  { k:"theodicy", t:"term", n:"Theodicy", pat:"theodic\\w*",
    d:`A proposed account of why God permits evil. Section VIII offers none — deliberately: "no one has the fawn's receipt."` },
  { k:"skepticaltheism", t:"term", n:"Skeptical theism", pat:"skeptical theism",
    d:`The response that our inability to see a justifying reason for the fawn is expected at our scale — a mind related to ours as ours to a beetle's. A defensive check, the essay concedes, never a worldview.`,
    l:"https://en.wikipedia.org/wiki/Skeptical_theism" },
  { k:"soulmaking", t:"term", n:"Soul-making", pat:"soul-making",
    d:`John Hick's tradition: goods like courage, forgiveness, and self-sacrifice are logically impossible without genuine stakes. A padded universe has contentment but no heroism.` },
  { k:"evidential", t:"term", n:"The evidential problem of evil", pat:"evidential problem|logical problem",
    d:`Not "evil disproves God" but "this much evil, distributed this way, is strong evidence against him." The serious version — Rowe's fawn, Draper's distribution — as opposed to the dead logical problem.` },
  { k:"embarrassment", t:"term", n:"Criterion of embarrassment", pat:"criterion of embarrassment",
    d:`The historians' rule: details embarrassing to the teller are likelier true, since no one fabricates against himself. Women discovering the tomb — discounted witnesses in that legal culture — is the classic case.`,
    l:"https://en.wikipedia.org/wiki/Criterion_of_embarrassment" },
  { k:"cor15", t:"term", n:"The 1 Corinthians 15 creed", pat:"First Corinthians 15",
    d:`The formula Paul says he received — died, buried, raised, appeared — dated by critical scholars across the spectrum to within two to five years of the crucifixion; Dunn put it within months. Living-memory time.`,
    l:"https://en.wikipedia.org/wiki/1_Corinthians_15" },
  { k:"priors", t:"term", n:"Priors", pat:"priors",
    d:`How likely you judge a claim to be before the new evidence arrives. Section VIII's honesty: everything depends on whether a resurrection is an intrusion into a closed system or the signature act of the reality independently described.` },
  { k:"freewilldef", t:"term", n:"The free will defense", pat:"free will defense",
    d:`Plantinga's argument that ended the logical problem of evil: a world with free creatures — or any goods that logically require the possibility of loss — is consistent with a wholly good, omnipotent God.`,
    l:"https://en.wikipedia.org/wiki/Alvin_Plantinga%27s_free-will_defense" },

  /* ===== SECTION IX — THE VERDICT ===== */
  { k:"trinity", t:"term", n:"The Trinity", pat:"Trinity",
    d:`The doctrine that the one infinite act of To-Be is not solitary: eternally Knower, Known, and the Love between them — Father, Word, Gift. Why "God is love" is an ontological report, not a compliment.`,
    l:"https://en.wikipedia.org/wiki/Trinity" },
  { k:"incarnation", t:"term", n:"The Incarnation", pat:"Incarnation",
    d:`The Christian claim that the eternal Word took a creature's nature into the divine life — that the terminus of Section III took the wound of Section VIII into itself.`,
    l:"https://en.wikipedia.org/wiki/Incarnation_(Christianity)" },
  { k:"fideism", t:"term", n:"Fideism", pat:"fideism",
    d:`The position that faith must fly blind — that reason has no road to God. Condemned by name at the First Vatican Council, 1870.`,
    l:"https://en.wikipedia.org/wiki/Fideism" },
  { k:"vatican1", t:"term", n:"The First Vatican Council", pat:"First Vatican Council",
    d:`The 1870 council that made it dogma — on pain of anathema — that God can be known with certainty by natural reason from created things.`,
    l:"https://en.wikipedia.org/wiki/First_Vatican_Council" },
  { k:"anathema", t:"term", n:"Anathema", pat:"anathema",
    d:`The Church's most solemn formal condemnation. Vatican I bound itself on pain of it to the proposition that this essay's method is legitimate.` },
  { k:"dogma", t:"term", n:"Dogma", pat:"dogma",
    d:`A solemnly defined teaching of the Church. The strange one here: a dogma about the legitimacy of arguments — that reason is not the rival of this faith but its outer court.` },
  { k:"naturalreason", t:"term", n:"Natural reason", pat:"natural reason",
    d:`Human reason unaided by revelation. The Church alone among the world's institutions has bound itself, on pain of anathema, to the claim that it can reach God with certainty from created things.` },
  { k:"defeasible", t:"term", n:"Defeasible", pat:"defeasible",
    d:`Capable of being defeated by counter-evidence. The essay's honest concession: each line is defeasible alone — but independent partial confirmations multiply.` },
  { k:"confessions", t:"term", n:"The Confessions", pat:"Confessions",
    d:`Augustine's c. 397 AD autobiography — the book that basically invented introspective autobiography, and the source of this essay's closing sentence.`,
    l:"https://en.wikipedia.org/wiki/Confessions_(Augustine)" },

  /* ===== THE CAST — PEOPLE ===== */
  { k:"aquinas", t:"person", n:"Thomas Aquinas", pat:"Thomas Aquinas|Aquinas",
    d:`Dominican friar (1225–1274) whose synthesis of Aristotle and Christian theology — the Five Ways, essence and existence, the convertibility of being and goodness — is the system this essay examines.`,
    l:"https://en.wikipedia.org/wiki/Thomas_Aquinas" },
  { k:"aristotle", t:"person", n:"Aristotle", pat:"Aristotle",
    d:`Greek philosopher (384–322 BC), author of the formula this essay starts from: the good is what all things desire.`,
    l:"https://en.wikipedia.org/wiki/Aristotle" },
  { k:"augustine", t:"person", n:"Augustine of Hippo", pat:"Augustine",
    d:`North African bishop (354–430) whose Confessions invented the introspective autobiography — and who gave this essay its closing sentence.`,
    l:"https://en.wikipedia.org/wiki/Augustine_of_Hippo" },
  { k:"plato", t:"person", n:"Plato", pat:"Plato",
    d:`Athenian philosopher (c. 428–348 BC). His dialogue Euthyphro poses the dilemma Section V answers; his realm of Forms is Contestant Two's ancestor.`,
    l:"https://en.wikipedia.org/wiki/Plato" },
  { k:"socrates", t:"person", n:"Socrates", pat:"Socrates",
    d:`The questioner of Athens (c. 470–399 BC), who corners Euthyphro in Plato's dialogue — and appears here as a Cambridge-relation example.`,
    l:"https://en.wikipedia.org/wiki/Socrates" },
  { k:"moore", t:"person", n:"G. E. Moore", pat:"G\\. E\\. Moore|Moore",
    d:`Cambridge philosopher (1873–1958) whose Open Question Argument (1903) tried to prove "good" indefinable — and ruled ethics for half a century.`,
    l:"https://en.wikipedia.org/wiki/G._E._Moore" },
  { k:"kripke", t:"person", n:"Saul Kripke", pat:"Saul Kripke|Kripke",
    d:`Logician (1940–2022) whose work on naming showed that informative identities — water is H₂O — can be necessary yet discovered, not read off the dictionary.`,
    l:"https://en.wikipedia.org/wiki/Saul_Kripke" },
  { k:"geach", t:"person", n:"Peter Geach", pat:"Peter Geach|Geach",
    d:`British philosopher (1916–2013); his point that "good" is attributive turns out, in Section I, to confirm the analysis it attacked.`,
    l:"https://en.wikipedia.org/wiki/Peter_Geach" },
  { k:"kant", t:"person", n:"Immanuel Kant", pat:"Immanuel Kant|Kant",
    d:`Königsberg philosopher (1724–1804); author of "existence is not a predicate," aimed at the ontological argument.`,
    l:"https://en.wikipedia.org/wiki/Immanuel_Kant" },
  { k:"frege", t:"person", n:"Gottlob Frege", pat:"Gottlob Frege|Frege",
    d:`German logician (1848–1925), founder of modern logic, where existence is expressed by the quantifier, not a predicate.`,
    l:"https://en.wikipedia.org/wiki/Gottlob_Frege" },
  { k:"mill", t:"person", n:"John Stuart Mill", pat:"John Stuart Mill|Mill",
    d:`British utilitarian (1806–1873), ridiculed for sliding from "desired" to "desirable" — the slide Weld One defends against.`,
    l:"https://en.wikipedia.org/wiki/John_Stuart_Mill" },
  { k:"nozick", t:"person", n:"Robert Nozick", pat:"Robert Nozick|Nozick",
    d:`Harvard philosopher (1938–2002); his experience machine is the decisive test against hedonism in Section I.`,
    l:"https://en.wikipedia.org/wiki/Robert_Nozick" },
  { k:"schopenhauer", t:"person", n:"Arthur Schopenhauer", pat:"Schopenhauer",
    d:`German pessimist (1788–1860): reality at bottom is blind striving Will, and existence a mistake. Section III's tragic option.`,
    l:"https://en.wikipedia.org/wiki/Arthur_Schopenhauer" },
  { k:"nietzsche", t:"person", n:"Friedrich Nietzsche", pat:"Nietzsche",
    d:`German philosopher (1844–1900): the bottom is power, and "good" is what the strong call their strength. Section III answers that power is capacity, and capacity is act.`,
    l:"https://en.wikipedia.org/wiki/Friedrich_Nietzsche" },
  { k:"russell", t:"person", n:"Bertrand Russell", pat:"Bertrand Russell|Russell",
    d:`British philosopher (1872–1970); in a famous 1948 radio debate with F. C. Copleston he held that "the universe is just there, and that's all."`,
    l:"https://en.wikipedia.org/wiki/Bertrand_Russell" },
  { k:"hume", t:"person", n:"David Hume", pat:"David Hume|Hume",
    d:`Scottish empiricist (1711–1776): causation as pattern, reason as slave of the passions, miracles ruled out by the prior. The essay engages him at three separate joints.`,
    l:"https://en.wikipedia.org/wiki/David_Hume" },
  { k:"vaninwagen", t:"person", n:"Peter van Inwagen", pat:"Peter van Inwagen|van Inwagen",
    d:`American metaphysician (b. 1942); argued the unrestricted PSR self-destructs by necessitating all contingency. Section III's Objection 2.`,
    l:"https://en.wikipedia.org/wiki/Peter_van_Inwagen" },
  { k:"oppy", t:"person", n:"Graham Oppy", pat:"Graham Oppy|Oppy",
    d:`Australian philosopher (b. 1960), widely regarded as the leading atheist metaphysician; his move: grant the necessary terminus, then make it physical.`,
    l:"https://en.wikipedia.org/wiki/Graham_Oppy" },
  { k:"gale", t:"person", n:"Richard Gale", pat:"Richard Gale|Gale",
    d:`American philosopher (1932–2023); with Alexander Pruss he showed that a weakened PSR — the universe's existence possibly has an explanation — still reaches a necessary being.`,
    l:"https://en.wikipedia.org/wiki/Richard_M._Gale" },
  { k:"pruss", t:"person", n:"Alexander Pruss", pat:"Alexander Pruss|Pruss",
    d:`Baylor philosopher and mathematician; co-author of the Gale–Pruss modal cosmological argument and a developer of powers-based modality.`,
    l:"https://en.wikipedia.org/wiki/Alexander_Pruss" },
  { k:"plantinga", t:"person", n:"Alvin Plantinga", pat:"Alvin Plantinga|Plantinga",
    d:`American philosopher (b. 1932), giant of analytic philosophy of religion: the free will defense, the evolutionary argument against naturalism — and, here, honest pressure on divine simplicity.`,
    l:"https://en.wikipedia.org/wiki/Alvin_Plantinga" },
  { k:"mullins", t:"person", n:"R. T. Mullins", pat:"R\\. T\\. Mullins|Mullins",
    d:`Philosopher prosecuting the sharpest current case against classical theism: modal collapse. Section IV flags it as a live wound — and answers it.`,
    l:"https://plato.stanford.edu/entries/divine-simplicity/" },
  { k:"tomaszewski", t:"person", n:"Christopher Tomaszewski", pat:"Christopher Tomaszewski|Tomaszewski",
    d:`Philosopher whose analysis of modal collapse — "the act of creating this world" as a non-rigid designator — supplies Section IV's reply.` },
  { k:"ockham", t:"person", n:"William of Ockham", pat:"William of Ockham|Ockham",
    d:`Franciscan friar (c. 1287–1347), champion of voluntarism — the view Aquinas and the Catholic mainstream fought as making morality arbitrary.`,
    l:"https://en.wikipedia.org/wiki/William_of_Ockham" },
  { k:"morriston", t:"person", n:"Wes Morriston", pat:"Wes Morriston|Morriston",
    d:`University of Colorado philosopher; presses the Euthyphro's "third horn" against divine-nature ethics.` },
  { k:"koons", t:"person", n:"Jeremy Koons", pat:"Jeremy Koons|Koons",
    d:`Georgetown philosopher; with Morriston and Wielenberg, a leading voice of the Euthyphro's third horn.` },
  { k:"wielenberg", t:"person", n:"Erik Wielenberg", pat:"Erik Wielenberg|Wielenberg",
    d:`DePauw philosopher; author of robust normative realism — objective morality without God — the strongest atheist move in Section VI's tournament.`,
    l:"https://en.wikipedia.org/wiki/Erik_Wielenberg" },
  { k:"alston", t:"person", n:"William Alston", pat:"William Alston|Alston",
    d:`American philosopher (1921–2009); showed that standards can be concrete paradigms — like the meter bar in Paris — not only abstract rules.`,
    l:"https://en.wikipedia.org/wiki/William_Alston" },
  { k:"enoch", t:"person", n:"David Enoch", pat:"David Enoch|Enoch",
    d:`Israeli philosopher; an atheist arguing that the deliberative standpoint can't treat its own verdicts as mere expression. Friendly fire in Section VI.`,
    l:"https://en.wikipedia.org/wiki/David_Enoch" },
  { k:"foot", t:"person", n:"Philippa Foot", pat:"Philippa Foot|Foot",
    d:`British philosopher (1920–2010); her "natural goodness" anchored ethics in natures and their flourishing — without theology. Section VI calls it the first half of the true story.`,
    l:"https://en.wikipedia.org/wiki/Philippa_Foot" },
  { k:"thompson", t:"person", n:"Michael Thompson", pat:"Michael Thompson|Thompson",
    d:`University of Pittsburgh philosopher; developed Foot's natural-goodness program in Life and Action.` },
  { k:"molnar", t:"person", n:"George Molnar", pat:"George Molnar|Molnar",
    d:`Australian philosopher (1934–1999); an atheist whose standard work on powers named their "physical intentionality" — directedness at what does not exist.`,
    l:"https://en.wikipedia.org/wiki/George_Molnar_(philosopher)" },
  { k:"brentano", t:"person", n:"Franz Brentano", pat:"Franz Brentano|Brentano",
    d:`Austrian philosopher (1838–1917) who made "aboutness" — intentionality — the defining mark of the mental.`,
    l:"https://en.wikipedia.org/wiki/Franz_Brentano" },
  { k:"street", t:"person", n:"Sharon Street", pat:"Sharon Street|Street",
    d:`NYU philosopher; author of the evolutionary debunking argument — the universal solvent tested in Section VII.`,
    l:"https://en.wikipedia.org/wiki/Sharon_Street" },
  { k:"nagel", t:"person", n:"Thomas Nagel", pat:"Thomas Nagel|Nagel",
    d:`American philosopher (b. 1937); an atheist who pressed the reliability-of-reason problem in Mind and Cosmos and confessed a "cosmic authority problem."`,
    l:"https://en.wikipedia.org/wiki/Thomas_Nagel" },
  { k:"feuerbach", t:"person", n:"Ludwig Feuerbach", pat:"Ludwig Feuerbach|Feuerbach",
    d:`German philosopher (1804–1872): God is humanity's self-image projected onto the sky.`,
    l:"https://en.wikipedia.org/wiki/Ludwig_Feuerbach" },
  { k:"freud", t:"person", n:"Sigmund Freud", pat:"Sigmund Freud|Freud",
    d:`Founder of psychoanalysis (1856–1939): God is the longed-for father, a wish-fulfillment. Section VII notes the wish can run both ways.`,
    l:"https://en.wikipedia.org/wiki/Sigmund_Freud" },
  { k:"rowe", t:"person", n:"William Rowe", pat:"William Rowe|Rowe",
    d:`American philosopher (1931–2015); his fawn in the forest fire is the evidential problem of evil at its most honest.`,
    l:"https://en.wikipedia.org/wiki/William_Rowe" },
  { k:"draper", t:"person", n:"Paul Draper", pat:"Paul Draper|Draper",
    d:`Purdue philosopher; argues the biological distribution of pain and pleasure fits indifference better than perfect Goodness.`,
    l:"https://en.wikipedia.org/wiki/Paul_Draper_(philosopher)" },
  { k:"mackie", t:"person", n:"J. L. Mackie", pat:"J\\. L\\. Mackie|Mackie",
    d:`Australian philosopher (1917–1981); his logical problem of evil — and his error theory — are both answered in this essay.`,
    l:"https://en.wikipedia.org/wiki/J._L._Mackie" },
  { k:"epicurus", t:"person", n:"Epicurus", pat:"Epicurus",
    d:`Athenian philosopher (341–270 BC); the ancient questions descend from him: is God willing but not able? Able but not willing?`,
    l:"https://en.wikipedia.org/wiki/Epicurus" },
  { k:"dostoevsky", t:"person", n:"Fyodor Dostoevsky", pat:"Dostoevsky",
    d:`Russian novelist (1821–1881); The Brothers Karamazov gives Section VIII its voice of protest.`,
    l:"https://en.wikipedia.org/wiki/Fyodor_Dostoevsky" },
  { k:"karamazov", t:"person", n:"Ivan Karamazov", pat:"Ivan Karamazov",
    d:`Dostoevsky's character who "returns the ticket": even universal harmony is refused if purchased at the price of one tortured child.`,
    l:"https://en.wikipedia.org/wiki/The_Brothers_Karamazov" },
  { k:"tacitus", t:"person", n:"Tacitus", pat:"Tacitus",
    d:`Roman historian (c. 56–120 AD), an aristocrat with contempt for Christianity; his Annals 15.44 attests the crucifixion under Pontius Pilate.`,
    l:"https://en.wikipedia.org/wiki/Tacitus" },
  { k:"josephus", t:"person", n:"Josephus", pat:"Josephus",
    d:`Jewish historian (c. 37–100 AD); a non-Christian source for both Jesus's death and the execution of James.`,
    l:"https://en.wikipedia.org/wiki/Josephus" },
  { k:"ludemann", t:"person", n:"Gerd Lüdemann", pat:"Gerd Lüdemann|Lüdemann",
    d:`New Testament scholar and atheist who grants it "may be taken as historically certain" that the disciples had experiences of the risen Jesus.`,
    l:"https://en.wikipedia.org/wiki/Gerd_L%C3%BCdemann" },
  { k:"dunn", t:"person", n:"James D. G. Dunn", pat:"James D\\. G\\. Dunn|Dunn",
    d:`New Testament scholar (1939–2020) who dated the creed of 1 Corinthians 15 to within months of the crucifixion.`,
    l:"https://en.wikipedia.org/wiki/James_D._G._Dunn" },
  { k:"sherwinwhite", t:"person", n:"A. N. Sherwin-White", pat:"A\\. N\\. Sherwin-White|Sherwin-White",
    d:`Oxford Roman historian; his study of legendary accretion found even two generations too short for legend to erase a historical core.`,
    l:"https://en.wikipedia.org/wiki/A._N._Sherwin-White" },
  { k:"wright", t:"person", n:"N. T. Wright", pat:"N\\. T\\. Wright|Wright",
    d:`New Testament scholar; his exhaustive survey shows first-century Jewish "resurrection" meant the general raising at the end of history — no template for one man raised mid-time.`,
    l:"https://en.wikipedia.org/wiki/N._T._Wright" },
  { k:"milton", t:"person", n:"John Milton", pat:"John Milton|Milton",
    d:`English poet (1608–1674); Paradise Lost gives absolute evil its most compelling voice — and makes the concession: "Evil, be thou my good."`,
    l:"https://en.wikipedia.org/wiki/Paradise_Lost" },
  { k:"dionysius", t:"person", n:"Dionysius", pat:"Dionysius",
    d:`The anonymous Syrian author (c. 500 AD) called Pseudo-Dionysius; the tradition adopted his axiom: bonum diffusivum sui — the good pours itself out.`,
    l:"https://en.wikipedia.org/wiki/Pseudo-Dionysius_the_Areopagite" },
  { k:"cthulhu", t:"person", n:"Cthulhu", pat:"Cthulhu",
    d:`H. P. Lovecraft's cosmic monster — the essay's test case for "a being of infinite power could be an infinite monster." Section IV runs him through the mechanics of malice.`,
    l:"https://en.wikipedia.org/wiki/Cthulhu" },
  { k:"darwin", t:"person", n:"Charles Darwin", pat:"Charles Darwin|Darwin",
    d:`Naturalist (1809–1882); natural selection explains organismic adaptation — and, Section VI argues, presupposes the deeper directedness it cannot explain.`,
    l:"https://en.wikipedia.org/wiki/Charles_Darwin" },
  { k:"jacobs", t:"person", n:"Jonathan Jacobs", pat:"Jonathan Jacobs|Jacobs",
    d:`Philosopher; with Pruss and Vetter, a developer of powers-based (dispositional) modality.` },
  { k:"vetter", t:"person", n:"Barbara Vetter", pat:"Barbara Vetter|Vetter",
    d:`Berlin philosopher; author of Potentiality, a landmark of powers-based modality.` }
];

/* ---------- pop-out quotations ---------- */

const PULLS = [
  { m:"denying it costs more than accepting it", d:"A case is airtight when denying it costs more than accepting it — on every front at once.", c:"THE WIN CONDITION" },
  { m:"performed in the currency of the good", d:"The denial of the good is always performed in the currency of the good.", c:"SECTION I" },
  { m:"The fish can doubt many things", d:"The fish can doubt many things. The water is what it doubts them in.", c:"SECTION I" },
  { m:"Nobody holds a funeral for gravel", d:"Grief is calibrated to being. Nobody holds a funeral for gravel.", c:"SECTION I" },
  { m:"Same inventory; catastrophically less actuality", d:"Same inventory; catastrophically less actuality.", c:"THE CORONER TEST" },
  { m:"paved with it", d:"Every path out of the good turns out to be paved with it.", c:"SECTION III" },
  { m:"not one thing in the story that", d:"Infinite mirrors, infinite reflected light — and still not one thing in the story that shines.", c:"THE CORRIDOR OF MIRRORS" },
  { m:"still need a table", d:"Dice that roll unpredictably still need a table.", c:"OBJECTION 3, ANSWERED" },
  { m:"absolutely simple can be absolutely necessary", d:"Only the absolutely simple can be absolutely necessary.", c:"SECTION III" },
  { m:"scales up with power", d:"Malice is not a capacity that scales up with power. It is, in every observed instance, a symptom of poverty.", c:"THE MECHANICS OF MALICE" },
  { m:"Large holes are still holes", d:"Large holes are still holes.", c:"ON CTHULHU" },
  { m:"It is not restraint", d:"It is not restraint. It is grammar.", c:"EUTHYPHRO, ANSWERED" },
  { m:"runs on fuel that only", d:"The strongest argument against God runs on fuel that only God's world supplies.", c:"SECTION VIII" },
  { m:"no one has the fawn", d:"No one has the fawn's receipt.", c:"THE HONESTY PARAGRAPH" },
  { m:"Being can be raised", d:"Being can be raised. A hole cannot.", c:"THE LAST CLAUSE" },
  { m:"escape punishment", d:"You do not pursue goodness to escape punishment. The punishment just is what missing goodness amounts to.", c:"SECTION IX" }
];

/* ============================================================ */

(function(){
  const $  = (s, r)=> (r||document).querySelector(s);
  const $$ = (s, r)=> Array.from((r||document).querySelectorAll(s));
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- theme ---------- */
  const root = document.documentElement;
  const saved = localStorage.getItem("gi-theme");
  if (saved) root.setAttribute("data-theme", saved);
  $("#themeBtn").addEventListener("click", ()=>{
    const next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    localStorage.setItem("gi-theme", next);
  });

  /* ---------- menu overlay ---------- */
  const menuov = $("#menuov");
  $("#menuBtn").addEventListener("click", ()=> menuov.classList.add("open"));
  menuov.addEventListener("click", (e)=>{ if (e.target === menuov) menuov.classList.remove("open"); });
  $$("a.mi", menuov).forEach(a => a.addEventListener("click", ()=> menuov.classList.remove("open")));
  document.addEventListener("keydown", (e)=>{
    if (e.key === "Escape"){ menuov.classList.remove("open"); hideCard(); }
  });

  /* ---------- header + progress + chapter spy ---------- */
  const topBar = $("#top"), prog = $("#progress"), chapLabel = $("#chapLabel");
  const railLinks = $$("nav.rail a");
  const sections = $$("section.chapter");

  function onScroll(){
    const h = document.documentElement;
    const pct = h.scrollTop / Math.max(1, (h.scrollHeight - h.clientHeight)) * 100;
    prog.style.width = pct + "%";
    topBar.classList.toggle("on", h.scrollTop > window.innerHeight * 0.62);
    parallax();
  }
  window.addEventListener("scroll", onScroll, { passive:true });

  const spy = new IntersectionObserver((es)=>{
    es.forEach(en=>{
      if (!en.isIntersecting) return;
      const id = en.target.id;
      railLinks.forEach(a => a.classList.toggle("active", a.getAttribute("href") === "#"+id));
      chapLabel.textContent = en.target.dataset.short || "";
    });
  }, { rootMargin: "-38% 0px -55% 0px" });
  sections.forEach(s => spy.observe(s));

  /* ---------- reveal on scroll ---------- */
  const revealTargets = $$("section.chapter .col > p, section.chapter .col > h3, .objection, .clash, .fact, .contestant, .fiber, figure, aside.pull, .timeline, .chapter-head, .legend");
  revealTargets.forEach(el => el.classList.add("rev"));
  const rio = new IntersectionObserver((es)=>{
    es.forEach(en=>{ if (en.isIntersecting){ en.target.classList.add("in"); rio.unobserve(en.target); } });
  }, { threshold: 0.05, rootMargin: "0px 0px -3% 0px" });

  /* ---------- parallax paintings ---------- */
  const artImgs = $$("figure.art img");
  function parallax(){
    if (reduced) return;
    const vh = window.innerHeight;
    artImgs.forEach(img=>{
      const r = img.parentElement.getBoundingClientRect();
      if (r.bottom < -80 || r.top > vh + 80) return;
      const p = (r.top + r.height/2 - vh/2) / vh;
      img.style.transform = "scale(1.12) translateY(" + (p * -26) + "px)";
    });
  }

  /* ---------- pop-out quotations ---------- */
  const norm = s => (s||"").toLowerCase().replace(/[^a-z0-9]/g, "");
  const essayParas = $$("main p[data-essay]");
  const used = new Set();
  PULLS.forEach(pull=>{
    const needle = norm(pull.m);
    const p = essayParas.find(el => !used.has(el) && norm(el.textContent).includes(needle));
    if (!p) return;
    used.add(p);
    const aside = document.createElement("aside");
    aside.className = "pull";
    aside.innerHTML = '<blockquote>' + pull.d + '</blockquote><div class="cite">' + pull.c + '</div>';
    p.parentNode.insertBefore(aside, p.nextSibling);
    aside.classList.add("rev");
  });

  /* ---------- floating definitions ---------- */
  const BY_KEY = {};
  ENTRIES.forEach(e => BY_KEY[e.k] = e);
  const sorted = ENTRIES.slice().sort((a,b)=> b.pat.length - a.pat.length);
  const RX = new RegExp(
    sorted.map((e)=>{
      const body = e.t === "person" ? "(?:" + e.pat + ")" : "(?i:(?:" + e.pat + "))";
      return "(?<T" + e.k.replace(/[^a-z0-9]/gi,"") + ">\\b" + body + "\\b)";
    }).join("|")
  );
  const KEYOF = {};
  sorted.forEach(e => KEYOF["T" + e.k.replace(/[^a-z0-9]/gi,"")] = e.k);

  const SEEN = new Set();
  const main = $("main");

  function scanNode(node){
    if (!node || !node.data || node.data.length < 2) return;
    const m = RX.exec(node.data);
    if (!m) return;
    const gname = Object.keys(m.groups).find(g => m.groups[g] !== undefined);
    if (!gname) return;
    const entry = BY_KEY[KEYOF[gname]];
    const idx = m.index, text = m[0];
    const sec = node.parentElement.closest("[data-sec]");
    const secId = sec ? sec.getAttribute("data-sec") : "x";
    const seenKey = entry.k + "@" + secId;
    const frag = document.createDocumentFragment();
    const before = node.data.slice(0, idx);
    if (before) frag.appendChild(document.createTextNode(before));
    if (!SEEN.has(seenKey)){
      SEEN.add(seenKey);
      const span = document.createElement("span");
      span.className = "term" + (entry.t === "person" ? " person" : "");
      span.textContent = text;
      span.setAttribute("data-k", entry.k);
      span.tabIndex = 0;
      frag.appendChild(span);
    } else {
      frag.appendChild(document.createTextNode(text));
    }
    const rest = document.createTextNode(node.data.slice(idx + text.length));
    frag.appendChild(rest);
    node.parentNode.replaceChild(frag, node);
    scanNode(rest);
  }

  const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, {
    acceptNode(n){
      if (!n.data.trim()) return NodeFilter.FILTER_REJECT;
      const p = n.parentElement;
      if (!p || p.closest("script,style,h1,h2,h3,figcaption,.doodle,a.mi,.pull,.legend")) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  const textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);
  textNodes.forEach(scanNode);

  /* ---------- the floating card ---------- */
  const card = document.createElement("div");
  card.id = "termcard";
  document.body.appendChild(card);
  let hideTimer = null, currentTerm = null;

  function fillCard(entry, displayText){
    card.className = entry.t === "person" ? "person-card" : "";
    card.innerHTML =
      '<div class="tc-tag">' + (entry.t === "person" ? "IN THE ARGUMENT" : "WORKING CONCEPT") + '</div>' +
      '<div class="tc-title">' + entry.n + '</div>' +
      '<div class="tc-def">' + entry.d + '</div>' +
      (entry.l ? '<a class="tc-link" href="' + entry.l + '" target="_blank" rel="noopener noreferrer">LEARN MORE &#8599;</a>' : '');
  }
  function placeCard(term){
    if (window.innerWidth < 720) return; /* CSS docks it as a bottom sheet */
    const r = term.getBoundingClientRect();
    card.style.visibility = "hidden";
    card.classList.add("show");
    const ch = card.offsetHeight, cw = card.offsetWidth;
    let left = r.left + r.width/2 - cw/2;
    left = Math.max(12, Math.min(left, window.innerWidth - cw - 12));
    let top = r.top - ch - 12;
    if (top < 64) top = r.bottom + 12;
    card.style.left = left + "px";
    card.style.top = top + "px";
    card.style.visibility = "";
  }
  function showCard(term){
    const entry = BY_KEY[term.getAttribute("data-k")];
    if (!entry) return;
    clearTimeout(hideTimer);
    if (currentTerm) currentTerm.classList.remove("open");
    currentTerm = term;
    term.classList.add("open");
    fillCard(entry, term.textContent);
    placeCard(term);
    card.classList.add("show");
  }
  function hideCard(){
    hideTimer = setTimeout(()=>{
      card.classList.remove("show");
      if (currentTerm) currentTerm.classList.remove("open");
      currentTerm = null;
    }, 160);
  }
  main.addEventListener("mouseover", e=>{
    const t = e.target.closest(".term");
    if (t) showCard(t);
  });
  main.addEventListener("mouseout", e=>{
    const t = e.target.closest(".term");
    if (t) hideCard();
  });
  main.addEventListener("focusin", e=>{
    const t = e.target.closest(".term");
    if (t) showCard(t);
  });
  main.addEventListener("focusout", hideCard);
  main.addEventListener("click", e=>{
    const t = e.target.closest(".term");
    if (!t) return;
    if (currentTerm === t && card.classList.contains("show")){ hideCard(); return; }
    showCard(t);
  });
  card.addEventListener("mouseenter", ()=> clearTimeout(hideTimer));
  card.addEventListener("mouseleave", hideCard);
  document.addEventListener("click", e=>{
    if (!e.target.closest(".term") && !e.target.closest("#termcard")){
      card.classList.remove("show");
      if (currentTerm) currentTerm.classList.remove("open");
      currentTerm = null;
    }
  });
  window.addEventListener("resize", ()=> card.classList.remove("show"));

  /* ---------- hero dust particles ---------- */
  const canvas = $("#dust");
  if (canvas && !reduced){
    const ctx = canvas.getContext("2d");
    let W, H, parts = [], running = true;
    function size(){
      W = canvas.width = canvas.offsetWidth * devicePixelRatio;
      H = canvas.height = canvas.offsetHeight * devicePixelRatio;
    }
    size();
    window.addEventListener("resize", size);
    for (let i = 0; i < 90; i++){
      parts.push({
        x: Math.random(), y: Math.random(),
        r: 0.5 + Math.random()*1.7,
        s: 0.00012 + Math.random()*0.00042,
        ph: Math.random()*Math.PI*2,
        sw: 0.00004 + Math.random()*0.00012,
        a: 0.25 + Math.random()*0.55,
        tw: Math.random()*Math.PI*2
      });
    }
    const hero = $(".hero");
    new IntersectionObserver(es => { running = es[0].isIntersecting; }, {threshold: 0}).observe(hero);
    (function tick(){
      requestAnimationFrame(tick);
      if (!running) return;
      ctx.clearRect(0,0,W,H);
      parts.forEach(p=>{
        p.y -= p.s; p.tw += 0.02; p.ph += p.sw;
        if (p.y < -0.02){ p.y = 1.02; p.x = Math.random(); }
        const x = (p.x + Math.sin(p.ph*8)*0.006) * W;
        const y = p.y * H;
        const alpha = p.a * (0.55 + 0.45*Math.sin(p.tw));
        ctx.beginPath();
        ctx.arc(x, y, p.r * devicePixelRatio, 0, Math.PI*2);
        ctx.fillStyle = "rgba(232, 196, 111, " + alpha.toFixed(3) + ")";
        ctx.fill();
      });
    })();
  }

  /* ---------- observe reveals (after all injections) ---------- */
  $$(".rev").forEach(el => rio.observe(el));
  onScroll();
})();
