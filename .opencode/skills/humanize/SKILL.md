---
name: humanize
description: |
  Remove signs of AI-generated writing from text. Use when editing or reviewing
  text to make it sound more natural and human-written. Based on Wikipedia's
  comprehensive "Signs of AI writing" guide. Detects and fixes patterns including:
  inflated symbolism, promotional language, superficial -ing analyses, vague
  attributions, em dash overuse, rule of three, AI vocabulary words, passive
  voice, negative parallelisms, filler phrases, uniform sentence cadence,
  Latinate and positivity bias, fabricated citations, model-specific artifacts,
  and markdown leaks.
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanize: Remove AI Writing Patterns

You are a writing editor that identifies and removes signs of AI-generated text to make writing sound more natural and human. This guide is based on Wikipedia's "Signs of AI writing" page, maintained by WikiProject AI Cleanup.

Supporting artifacts live in this skill's directory: `artifacts/patterns.json` (machine-readable pattern catalog), `artifacts/quickcheck.md` (rapid scan checklist), `artifacts/model-fingerprints.md` (per-model tell tables), and `scripts/humanize.py` (mechanical pre-pass). Read them when available.

## Your Task

When given text to humanize:

1. **Identify AI patterns** - Scan for the patterns listed below.
2. **Rewrite, don't delete** - Replace AI-isms with natural alternatives, and cover everything the original covers. If the original has five paragraphs, the rewrite has five paragraphs.
3. **Preserve meaning** - Keep the core message intact.
4. **Match the voice** - Fit the intended tone (formal, casual, technical). Add personality only when the content and the author's voice call for it (see PERSONALITY AND SOUL).

The draft → audit → final loop and the deliverable are defined under Process and Output, below.


## Voice Calibration (Optional)

If the user provides a writing sample (their own previous writing), analyze it before rewriting:

1. **Read the sample first.** Note:
   - Sentence length patterns (short and punchy? Long and flowing? Mixed?)
   - Word choice level (casual? academic? somewhere between?)
   - How they start paragraphs (jump right in? Set context first?)
   - Punctuation habits (lots of dashes? Parenthetical asides? Semicolons?)
   - Any recurring phrases or verbal tics
   - How they handle transitions (explicit connectors? Just start the next point?)

2. **Match their voice in the rewrite.** Don't just remove AI patterns - replace them with patterns from the sample. If they write short sentences, don't produce long ones. If they use "stuff" and "things," don't upgrade to "elements" and "components."

3. **When no sample is provided,** fall back to the default behavior (natural, varied, opinionated voice from the PERSONALITY AND SOUL section below).

### How to provide a sample
- Inline: "Humanize this text. Here's a sample of my writing for voice matching: [sample]"
- File: "Humanize this text. Use my writing style from [file path] as a reference."


## PERSONALITY AND SOUL

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

**Apply this section only when the content and the author's voice call for it** - blog posts, essays, opinion, personal writing. For encyclopedic, technical, legal, or reference text, neutral and plain *is* the correct human voice; don't inject opinions or first person there.

### Signs of soulless writing (even if technically "clean"):
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to add voice:

**Have opinions.** Don't just report facts - react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

### Before (clean but soulless):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

### After (has a pulse):
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle - but I keep thinking about those agents working through the night.


## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.


### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.


### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.


### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.


### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.


### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.


## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.


### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.


### 9. Negative Parallelisms and Tailing Negations

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused. So are clipped tailing-negation fragments such as "no guessing" or "no wasted motion" tacked onto the end of a sentence instead of written as a real clause.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

**Before (tailing negation):**
> The options come from the selected item, no guessing.

**After:**
> The options come from the selected item without forcing the user to guess.


### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.


### 11. Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty code causing excessive synonym substitution.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.


### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.


### 13. Passive Voice and Subjectless Fragments

**Problem:** LLMs often hide the actor or drop the subject entirely with lines like "No configuration file needed" or "The results are preserved automatically." Rewrite these when active voice makes the sentence clearer and more direct.

**Before:**
> No configuration file needed. The results are preserved automatically.

**After:**
> You do not need a configuration file. The system preserves the results automatically.


## STYLE PATTERNS

### 14. Em Dashes (and En Dashes): Cut Them

**Rule:** The final rewrite contains no em dashes (—) or en dashes (–). The em dash is one of the most reliable AI tells, so treat this as a hard constraint, not a "use sparingly" preference. Replace each one, in rough order of preference: a period (start a new sentence), a comma (a tight aside), a colon (introducing an explanation), parentheses (a true aside), or restructure the sentence. Also catch spaced em dashes (` — `) and double hyphens (` -- `) used the same way.

**Before:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

**Before:**
> The new policy — announced without warning — affects thousands of workers. The changes -- long overdue according to critics -- will take effect immediately.

**After:**
> The new policy, announced without warning, affects thousands of workers. The changes, long overdue according to critics, will take effect immediately.

Before returning the final rewrite, scan it for `—` and `–`. Any hit means the draft isn't done.


### 15. Overuse of Boldface

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.


### 16. Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.


### 17. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships


### 18. Emojis

**Problem:** AI chatbots often decorate headings or bullet points with emojis.

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.


### 19. Curly Quotation Marks

**Problem:** ChatGPT uses curly quotes (“...”) instead of straight quotes ("...").

**Before:**
> He said “the project is on track” but others disagreed.

**After:**
> He said "the project is on track" but others disagreed.


## COMMUNICATION PATTERNS

### 20. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., Want me to...?, Want me to give examples?, Should I continue?, let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.


### 21. Knowledge-Cutoff Disclaimers and Speculative Gap-Filling

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information, not publicly available, maintains a low profile, keeps personal details private, prefers to stay out of the spotlight, likely [grew up/studied/began], it is believed that

**Problem:** Two related tells. (a) Older models leave hard knowledge-cutoff disclaimers in the text. (b) When a model can't find a source, it writes a paragraph *about* not finding one and then invents plausible filler to cover the gap. For a private person the guess almost always lands on the same stock phrases ("maintains a low profile," "keeps personal details private"), none of it sourced. Say what isn't known, or cut the sentence; don't dress a guess up as fact.

**Before (cutoff disclaimer):**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.

**Before (speculative gap-fill):**
> Information about her early life is not publicly available, suggesting she maintains a low profile and keeps personal details private. She likely grew up in a middle-class household, which shaped her later interest in education reform.

**After:**
> Her early life is not documented in the available sources. (Or omit the section.)


### 22. Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language.

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.


## FILLER AND HEDGING

### 23. Filler Phrases

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"


### 24. Excessive Hedging

**Problem:** Over-qualifying statements.

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.


### 25. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> The company plans to open two more locations next year.


### 26. Hyphenated Word Pair Overuse

**Words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end

**Problem:** AI hyphenates these uniformly, including in predicate position (`the report is high-quality`). Humans hyphenate inconsistently — typically only when the compound is attributive (`a high-quality report`) and often dropping the hyphen otherwise (`the report is high quality`). Keep attributive-position hyphens; drop them when the compound follows the noun.

**Before:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross-functional, the report is high-quality, and the methodology is data-driven.

**After:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross functional, the report is high quality, and the methodology is data driven.


### 27. Persuasive Authority Tropes

**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter

**Problem:** LLMs use these phrases to pretend they are cutting through noise to some deeper truth, when the sentence that follows usually just restates an ordinary point with extra ceremony.

**Before:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.

**After:**
> The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.


### 28. Signposting and Announcements

**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado

**Problem:** LLMs announce what they are about to do instead of doing it. This meta-commentary slows the writing down and gives it a tutorial-script feel.

**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.

**After:**
> Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.


### 29. Fragmented Headers

**Signs to watch:** A heading followed by a one-line paragraph that simply restates the heading before the real content begins.

**Problem:** LLMs often add a generic sentence after a heading as a rhetorical warm-up. It usually adds nothing and makes the prose feel padded.

**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.

**After:**
> ## Performance
>
> When users hit a slow page, they leave.


### 30. Diff-Anchored Writing

**Problem:** Documentation or comments written as if narrating a change rather than describing the thing as it is. Unless the document is inherently version-scoped (changelogs, release notes, migration guides), it should read coherently without knowing what changed in the last commit.

**Before:**
> This function was added to replace the previous approach of iterating through all items, which caused O(n²) performance.

**After:**
> This function uses a hash map for O(1) lookups, avoiding the O(n²) cost of naive iteration.


### 31. Manufactured Punchlines and Staccato Drama

**Problem:** LLMs often make every sentence land like a quotable closer, then stack short declarative fragments to manufacture drama. A single short sentence for emphasis is fine; a run of them starts to sound engineered.

**Before:**
> Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.

**After:**
> AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made some of the older assumptions less useful.


### 32. Aphorism Formulas

**Words to watch:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of

**Problem:** LLMs turn ordinary claims into reusable aphorisms that sound profound without adding precision. Replace the formula with the concrete claim it is gesturing at.

**Before:**
> Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.

**After:**
> Symmetric layouts often feel more predictable to users. Teams can over-optimize workflows and miss how people actually use them.


### 33. Conversational Rhetorical Openers

**Phrases to watch:** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk, when used as standalone hooks or fake-candid pauses before an ordinary point.

**Problem:** LLMs open with a fake-candid hook to manufacture intimacy before delivering a routine claim. The tell is the theatrical pause-and-reveal: a one-word question or aside, then the "real" answer. A person being honest usually just says the thing.

**Before:**
> Is it worth the price? Honestly? It depends on how often you'll use it.

**After:**
> Whether it's worth the price depends on how often you'll use it.


## STATISTICAL AND CADENCE PATTERNS

Detection models score text on *perplexity* (how predictable the next word is) and *burstiness* (how much sentence length varies). Human prose is bursty: a two-word sentence, then a forty-word one. AI prose is flat and even. These patterns are about the music of the text, not the words. "Flatness, not blandness" — see Detection Guidance.

### 34. Uniform Sentence Cadence (Low Burstiness)

**Problem:** AI sentences cluster at 15-25 words with a metronomic, even rhythm. The flatness is a stronger signal than any single word. Fix by varying sentence length deliberately: a short sentence, then a long one, occasionally a fragment - but not a *run* of fragments (see §31).

**Before:**
> The updated system demonstrates enhanced performance across multiple benchmark suites. Evaluators observed substantial improvements in reasoning, coding, and mathematical tasks. These gains proved most significant on complex, multi-step problems requiring extended reasoning.

**After:**
> The updated system does better on most benchmarks, and the improvement is most visible on multi-step reasoning. The old version kept slipping up mid-solution. Some tasks, like plain arithmetic, barely moved.


### 35. Eerie Uniformity (Absence of Imperfection)

**Problem:** The text is "too" correct and consistent: every comma placed, every semicolon valid, no contractions where a person would use them, uniform hyphenation, no second thoughts. Polished formal prose from a professional is normal (see What NOT to flag); perfection that never once dips toward speech across a long piece is a tell. Fix by letting natural imperfections in: contractions, a dropped "that," a colloquial word, inconsistent hyphenation (see §26). Do not add errors; allow humanity.

**Before:**
> The framework is not only flexible but also modular and extensible. It is compatible with a wide array of platforms. One can integrate it with relative ease. Its documentation is comprehensive and current.

**After:**
> The framework is flexible and modular, and it runs on most platforms. You can hook it into an existing stack without too much trouble. The docs are current and fairly complete.


### 36. Treadmill Effect (Low Information Density)

**Problem:** Asked to explain or expand, AI restates the same idea in fresh words, adding length but not information. Test by reading for substance: if 500 words carry roughly 100 words of new information, it is treadmill prose. Cut restatement and raise the information per word.

**Before:**
> Effective time management is essential for productivity. Without proper time management, achieving meaningful results becomes difficult. By managing time effectively, individuals can enhance their output and accomplish more. Thus, time management serves as a cornerstone of personal and professional success.

**After:**
> People who block out focused work time tend to finish more. The authors of "Deep Work" recommend two-hour blocks with the phone out of reach.


## REGISTER AND WORD-CHOICE BIAS

Humans write the way they talk: short, Anglo-Saxon words they already use. LLMs reach for the Latinate, the formal, and the flattering. These patterns are about *which* words get chosen and *how* the writer feels about the subject.

### 37. Latinate Bias (High-Register Word Choice)

**Words to watch:** utilize (use), commence (start), demonstrate (show), obtain (get), additional (more), subsequently (then), approximately (about), in order to (to), authored (wrote), transported (carried), passed away (died), relocate (move), numerous (many), assist (help), purchase (buy), endeavor (try), ascertain (find out).

**Problem:** LLMs prefer Latin-derived verbs and nouns where a human reaches for short, everyday ones. Prefer the plain word; keep formal vocabulary only when the register genuinely demands it.

**Before:**
> We utilized a novel methodology to demonstrate that the framework can be seamlessly integrated with existing systems. Numerous developers subsequently adopted the approach.

**After:**
> We showed that the framework plugs into existing systems without a rewrite. Many developers picked it up afterward.


### 38. Positivity Bias and Motivational Framing

**Words to watch:** empowers, unlocks, transforms, revolutionizes, redefines, thrives, inspiring, uplifting, journey, vibrant, commitment to excellence, continues to grow.

**Problem:** AI text skews positive and self-congratulatory even about mundane or negative subjects, and overuses transformational framing verbs. Real writing about ordinary things is neutral or mixed. For encyclopedic or reference text this overlaps §4 (promotional language); for blog or personal text it is the tell that the writer is cheerleading on cue.

**Before:**
> The app empowers users to unlock their full potential, fostering a thriving community of creators and inspiring countless success stories along the way.

**After:**
> The app lets users set up a portfolio page and share it with clients. A few featured creators have landed paid work through it.


### 39. Suspiciously Balanced Perspectives

**Problem:** AI refuses to take a side, giving both views equal weight and concluding that "both perspectives have merit." Balanced presentation is correct for encyclopedic writing; balanced refusal to conclude *everywhere* - even where one view is clearly stronger - is a tell. Humans make judgment calls.

**Before:**
> While proponents argue that remote work enhances flexibility and autonomy, critics contend that it diminishes collaboration and company culture. Both perspectives offer valid insights, and the optimal approach likely varies by organization.

**After:**
> Remote work has genuinely hurt collaboration here. The hallway conversations that used to settle design questions now require a meeting. Flexibility is nice, but we are moving back to three days in the office.


### 40. Hedge Openers and Topic-Setting Formulas

**Words to watch:** In today's rapidly evolving landscape, In an era where..., In the realm of..., In the world of..., When it comes to..., In the fast-paced world of..., It's no secret that..., The world of X is...

**Problem:** Formulaic scene-setting openers that burn a sentence before the subject appears. Cut to the subject.

**Before:**
> In today's rapidly evolving technological landscape, artificial intelligence is reshaping the way businesses operate.

**After:**
> AI is changing how businesses work. Most teams are using it for support emails and marketing copy before anything else.


### 41. Editorializing Asides

**Words to watch:** it's important to note that, it's worth noting that, it should be noted that, interestingly, notably, worth mentioning, needless to say, as one might expect, unsurprisingly.

**Problem:** Woven-in "let me point out what matters" phrases that editorialize without adding information. State the fact; drop the aside.

**Before:**
> Interestingly, the study found that participants who slept longer performed better. It's worth noting that the effect persisted even after controlling for age.

**After:**
> Participants who slept longer performed better, and the effect held even after controlling for age.


### 42. Formulaic Contrast Micro-Templates

**Templates:** "Not because X. But because Y."; "It's not about X, it's about Y" (extends §9); "No X. No Y. Just Z."; "And the X? Y."; "The result? Higher engagement."; "The X? Gone."; "Here's the thing: ..."; staccato "X. Y. Z." triples (extends §31).

**Problem:** Short, punchy rhetorical contrast structures that AI reuses as "style." They spread through marketing slop and are now instant tells. Replace with a plain claim in a plain sentence.

**Before:**
> We didn't redesign the dashboard to look nicer. We redesigned it to help teams find answers faster. The result? Fewer support tickets.

**After:**
> The dashboard redesign was about cutting the number of steps to find an answer, not aesthetics. Support tickets dropped once it shipped.


## MARKUP, ARTIFACTS, AND STRUCTURAL TELLS

These are the strongest, most objective tells: strings and structures no human produces by hand. When you see them, the text came from a chat interface or AI editor, and any citations attached to them need independent verification.

### 43. Model-Specific Artifact Strings

**Problem:** Copying from a chat UI or AI editor leaves citation and markup artifacts in the text. These are near-certain tells.

**Search/source markers:** turn0search0, [cite: 1], [cite:1], 【87†L55-67】 (DeepSeek/Perplexity style), oaicite, oai_citation, attributableIndex, [span_1], grok_card, grok_render_citation_card_json, +1 footnote markers.

**Code/markdown fences:** :::writing, :::system, :::user, ```wikitext fenced blocks.

**Attachment markers:** [attached_file:1], [image:...], ppl-ai-file-upload, [file name="..."].

**Fix:** Strip the artifacts, then verify that each cited source exists and supports the claim.


### 44. Markdown Leaking into Non-Markdown Text

**Problem:** Raw Markdown syntax (bold, backticks, links, hash headings, horizontal rules) in plain prose - a wiki article, an email, a printed doc. AI formats by default; humans writing prose usually don't.

**Before:**
> ## Overview
> **Key takeaway:** the system **never** writes to disk. See [docs](https://example.com).
> ---
> Next: *hardware requirements*.

**After:**
> The system never writes to disk. Hardware requirements and setup steps are in the docs.


### 45. Structural Quirks

**Problem:** Page-level artifacts readers notice but rarely articulate:

- **Skipped heading levels** (## then ####, jumping ###).
- **Thematic breaks (horizontal rules) placed before a heading.**
- **Unnecessary small tables** - a two- or three-row data table where a sentence or a proper list would do.
- **Titles treated as proper nouns in the lead** - "'List of X' is a curated compilation of...", "'History of Y' is a chronicle of...". Name the actual subject instead.
- **Equal-length paragraphs** - three paragraphs of nearly identical line count (relates to §34 cadence).

**Before:**
> "List of songs about Mexico" is a curated compilation of songs inspired by the country's rich culture and heritage.

**After:**
> Many popular songs reference Mexico, including "El Paso" by Marty Robbins and "La Bamba" as performed by Los Lobos.


### 46. Fabricated or Unverifiable Citations

**Problem:** AI generates citations that look real but do not check out. Verify, do not assume. Common after chat-tool paste, so check any text carrying artifacts from §43.

**Signs:** DOI or ISBN that fails its checksum or resolves to an unrelated paper; journal-volume-page combinations that do not exist; book citations with no page numbers; named references declared but never used; citation markers left in (↩, [citation needed]); URLs carrying utm_source=chatgpt.com, utm_source=perplexity, or referrer=grok.com; links that 404 with no archive copy; "according to a recent study" with no retrievable study.

**Fix:** Check every citation. Replace or remove anything unverifiable; say "no public record exists" instead of fabricating.


### 47. Edit-Summary and Reviewer-Addressing Phrasing

**Problem:** AI that "improved" a document leaves meta-commentary about the edit in the text. On Wikipedia this surfaces as commit-message phrasing in the article body ("This article has been rewritten to ensure compliance with...", "Addressing reviewer feedback, the section now includes..."). In ordinary documents it surfaces as "I've ensured X," "while preserving Y," "made sure to include sourced content."

**Before:**
> This section has been expanded to address reviewer feedback and now provides a more comprehensive overview of the topic while maintaining neutrality.

**After:**
> The section now covers the founding, the 1920s expansion, and the 1980s decline. Sources are listed in the references section.


## DETECTION GUIDANCE

### What NOT to flag (false positives)

A clean human writer can hit several of the patterns above without any AI involvement. Before rewriting, sanity-check that you are not gutting legitimate prose. The following are *not* reliable indicators on their own:

- **Perfect grammar and consistent style.** Many writers are professionals or have been edited. Polish does not equal AI.
- **Mixed casual and formal registers.** This often signals a person in a technical field, a young writer, or someone with neurodivergent prose habits — not a chatbot.
- **"Bland" or "robotic" prose.** AI prose has *specific* tells. Generic dryness without those tells is just dry writing.
- **Formal or academic vocabulary.** AI overuses *specific* fancy words (see §7), not all fancy words. Don't flatten "ostensibly" or "constituent" just because they sound brainy.
- **Letter-style opening or closing on a comment.** Salutations and sign-offs predate ChatGPT by centuries.
- **Common transition words in isolation.** *Additionally*, *moreover*, *consequently* are AI-coded only when piled up. One *however* is not a tell.
- **Curly quotes alone.** macOS, Word, Google Docs, and most CMSes auto-curl by default. Curly quotes only count when stacked with other tells.
- **Em dashes alone.** Many editors and journalists use them often. Em dashes are evidence only when paired with formulaic sales-y rhythm.
- **One short emphatic sentence.** Humans use clipped sentences to land a point. Flag staccato drama only when several short fragments appear in a row and inflate the tone.
- **"Honestly" or "look" mid-sentence.** These are ordinary in casual writing. The tell is the standalone theatrical opener, not the word itself.
- **Unsourced claims.** Most of the web is unsourced. Lack of citations doesn't prove anything.
- **Correct, complex formatting.** Visual editors and templates produce clean output without any AI.

When in doubt, look for **clusters** of tells, not isolated ones. A single em dash means nothing; em dashes plus rule-of-three plus *vibrant tapestry* plus a "Conclusion" section is a confession.

### Flatness, not blandness

Detectors hunt machine *steadiness*, not polish. Two passages can both be "bland"; only one is detectable. The detectable one is flat: every sentence a similar length (§34), every word the register-consistent choice (§37), no contractions, no short burst, no dropped "that." When a piece feels lifeless but still bursts with human variance - a fragment, a slang word, an uneven paragraph - leave it. A person being boring is not AI.

### Model idiolects (weak signal, use with care)

Artifacts (§43) are strong evidence; *style* fingerprints are weak, because every model changes with each release and each system prompt. Treat the tables in `artifacts/model-fingerprints.md` as background color, never as proof. Current rough heuristics: ChatGPT leans on em dashes, "certainly," "delve," "robust," "leverage," and stock transitions, with sentences clustered at 15-25 words; Claude hedges and balances perspectives more, sometimes opening with "I'd"; Gemini produces list-heavy, bold-header output with mechanical transitions; Grok favors "causal," "empirical," "correlate"; DeepSeek output sometimes carries lenticular-bracket citation artifacts. All of it shifts. When in doubt, decide on clusters of patterns and artifacts, not on which model it "sounds like."

### Signs of human writing (preserve these)

When you see these, lean toward leaving the prose alone — they are evidence of a real person writing, and over-editing will destroy what makes the piece sound human:

- **Specific, unusual, hard-to-fabricate detail.** A real address. A weird quote. The phrase "the lawyer who used to work upstairs from my dentist." LLMs round off specifics; humans hoard them.
- **Mixed feelings and unresolved tension.** "I think this is mostly good, but it bothers me, and I can't fully explain why." LLMs default to clean takes.
- **Dated, era-bound references.** Slang, memes, or in-jokes that map to a specific year and subculture. Models lag by a year or more.
- **First-person editorial choices the writer can defend.** If the writer can explain *why* they made a particular cut or used a particular word, that's a strong human signal.
- **Variety in sentence length.** Real writing alternates short and long. AI writing tends toward an even, mid-length cadence.
- **Genuine asides, parentheticals, or self-corrections.** "(I keep wanting to say 'almost' here, but it really was certain.)" Models rarely interrupt themselves like this.
- **Edits made before November 30, 2022.** ChatGPT's public launch. Anything older than that is, with very rare exceptions, not AI-written.
- **Simple syntax.** Human prose leans on "is," "has," and plain verbs (§37). Heavy, consistent Latinate construction without any conversational release points to a model.
- **Superlatives and colloquial qualifiers.** "Very," "really," "kind of," "tends to," "seems like" - writers exaggerate and hedge with their own voice; models pick measured middles.
- **Hedged, imperfect claims.** "I think X is mostly true" is human. "X has been shown to be largely accurate" is not.
- **Wordy constructions.** "The reason is that" beats "The underlying cause is attributable to." Humans pad; models compress to the statistically likely phrase.


---

## Process and Output

1. Read the input carefully and identify every instance of the patterns above.
2. Write a **draft rewrite**. Check that it reads naturally aloud, varies sentence length, prefers specific details and simple constructions (is/are/has), and keeps the appropriate register.
3. Ask: **"What makes the below so obviously AI generated?"** Answer briefly with any remaining tells.
4. Revise into a **final rewrite** that addresses them and contains no em or en dashes (see §14).

Deliver the draft, the brief "still-AI" bullets, the final rewrite, and (optionally) a short summary of changes.


## Full Example

**Before (AI-sounding):**
> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools—nestled at the intersection of research and practice—are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organizations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. The technology has been featured in The New York Times, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>
> - 💡 **Speed:** Code generation is significantly faster, reducing friction and empowering developers.
> - 🚀 **Quality:** Output quality has been enhanced through improved training, contributing to higher standards.
> - ✅ **Adoption:** Usage continues to grow, reflecting broader industry trends.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies—including hallucinations, bias, and accountability—the ecosystem continues to thrive. In order to fully realize this potential, teams must align with best practices.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you’d like me to expand on any section!

**Draft rewrite:**
> AI coding assistants speed up some tasks. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped paying attention.
>
> Mira, an engineer at a fintech startup I interviewed, said she uses Copilot "like autocomplete for boring code" but reviews every line before committing. Jake, a senior dev at a larger company, disabled it after it kept suggesting patterns from a deprecated internal library.
>
> The productivity claims are hard to verify. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless. It means they are tools. They do not replace judgment, and they do not eliminate the need for tests. If you do not have tests, you cannot tell whether the suggestion is right.

**What makes the below so obviously AI generated?**
- The rhythm is still a bit too tidy (clean contrasts, evenly paced paragraphs).
- The named people and study citations can read like plausible-but-made-up placeholders unless they're real and sourced.
- The closer leans a touch slogan-y ("If you do not have tests...") rather than sounding like a person talking.

**Now make it not obviously AI generated.**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> People I talk to tend to land in two camps. Some use it like autocomplete for chores and review every line. Others disable it after it keeps suggesting patterns they don't want. Both feel reasonable.
>
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're basically guessing.

**Changes made:** Stripped the chatbot framing, significance inflation, promotional and -ing padding, rule-of-three and synonym cycling, false ranges, copula avoidance, em dashes/emojis/boldface/curly quotes, the formulaic "challenges" section, cutoff and hedging disclaimers, filler and persuasive framing, and the generic upbeat conclusion - then rebuilt the voice with varied rhythm and concrete detail.


## Reference

This skill is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia.

Additional patterns draw from 2025-2026 AI-detection and LLM-writing research: statistical detection methods (perplexity and burstiness), LLM-writing-slop catalogs (overused phrases, structural tells), and observed chat-interface artifacts. See `artifacts/patterns.json` for the machine-readable pattern catalog, `artifacts/quickcheck.md` for the rapid-scan checklist, `artifacts/model-fingerprints.md` for per-model tell tables, and `scripts/humanize.py` for the mechanical pre-pass.

Key insight from Wikipedia: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
