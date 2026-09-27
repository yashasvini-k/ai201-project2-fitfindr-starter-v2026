# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

A user describes something they want to find while thrifting — an item type, a size, and a price ceiling, e.g. "a vintage graphic tee under $30, size M." FitFindr searches the listings data for matches, picks a candidate, and works out what it would pair with from a wardrobe. It returns a short, postable caption (a "fit card") describing the item and how to style it. If nothing matches the search, it stops and tells the user what to change instead of guessing.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Filters data/listings.json down to items whose title, description, or style_tags match a text description, whose size matches (or contains) the requested size, and whose price is at or below a maximum.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
description (str) — free-text search term, e.g. "vintage graphic tee", matched against title / description / style_tags
size (str) — size to match, e.g. "M" — note sizes in the data aren't uniform ("W30 L30", "S/M", "One Size", "US 8"), so this needs to be a substring/contains check, not exact-equals
max_price (float) — upper price bound, e.g. 30.0
- **Returns:** A list of listing dicts, each with id (str), title (str), description (str), category (str), style_tags (list of str), size (str), condition (str), price (float), colors (list of str), brand (str or None), platform (str).
- **When it has nothing:** An empty list ([]). Never None, never an exception.

### `suggest_outfit`

- **What it does:** Takes one listing dict (usually the top search result) and a wardrobe, and returns outfit pairing ideas using the model — likely reasoning over category, colors, and style_tags on both the new item and each wardrobe item to suggest complementary pieces.
- **Inputs:**
new_item (dict) — a single listing dict, same shape as one entry returned by search_listings
wardrobe (dict) — matches data/wardrobe_schema.json: {"items": [...]}, where each item has id (str), name (str), category (str — one of tops, bottoms, outerwear, shoes, accessories), colors (list of str), style_tags (list of str), notes (str or None). Note this is wardrobe["items"], not the wardrobe itself as a bare list.
- **Returns:** A single non-empty string — the outfit suggestion prose, which may describe more than one outfit within that one string (e.g. two labeled options separated by newlines).
- **When it has nothing:** If wardrobe["items"] is an empty list (the empty_wardrobe case in the schema file — the expected shape for a new user), returns general styling advice for the item instead of failing — still a list of strings, just not wardrobe-specific.

### `create_fit_card`


- **What it does:** Writes a short, postable caption combining the outfit ideas and the new item (using title, brand when present, colors) into something a person would actually caption a photo with.
- **Inputs:**
outfit (list of str) — the output of suggest_outfit
new_item (dict) — the same listing dict passed to suggest_outfit
- **Returns:** A single string — the caption text.
- **When it has nothing:** If outfit is an empty or whitespace-only string, returns a descriptive fallback caption built from new_item alone (title, price, platform) rather than failing.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in session["message"] naming what the user could change (e.g. try a higher price ceiling or a different size), leave session["fit_card"] as None, and stop before calling suggest_outfit. Otherwise, take the first item in the results, store it in session["selected_item"], and continue to suggest_outfit and then create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->session["selected_item"] (the listing dict search_listings chose) flows into suggest_outfit; session["outfit"] (its return value) flows into create_fit_card; session["fit_card"] holds the final caption, or None plus session["message"] on the empty-search path.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```
$ python -c "from tools import suggest_outfit; ..."

```
Here are two specific outfits using the vintage Levi's 501 jeans and pieces from their existing wardrobe:

**Outfit 1: Casual Streetwear**
* **Bottoms:** Vintage Levi's 501 Jeans
* **Top:** White ribbed tank top
* **Outerwear:** Vintage black denim jacket (worn over the tank)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

*Why it works:* This is a classic, effortless combination. The fitted white tank balances the straight-leg fit of the 501s, while the black denim jacket layered on top adds a cool, vintage double-denim aesthetic that ties into their streetwear style.

**Outfit 2: Cozy & Edgy**
* **Bottoms:** Vintage Levi's 501 Jeans
* **Top:** Oversized grey crewneck sweatshirt
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt and black crossbody bag

*Why it works:* Pairing the oversized grey crewneck with the structured medium-wash 501s creates a great proportion play (baggy on top, straight-leg on bottom). Tucking the front of the sweatshirt in with the brown leather belt pulls the look together, and the black combat boots add a nice grunge edge.

```
$ python -c "from tools import create_fit_card; ..."

```
I am literally shaking, I just scored these vintage Levi's 501 jeans on Depop for only $38! Medium wash is honestly the holy grail, and I can't wait to live in these with just a simple white tee and sneakers. My lucky streak continues! ✨👖

```
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I used Claude to help me figure out why one test case failed while the rest passed and how to make sure all the test cases passed.
- *What came back:* Claude said that 9/10 test cases passing meant that the environment was fine and asked for the exact output that I was seeing in terminal
- *What I changed:* I realised that I was using an older version of python and had to install the latest version so all the test cases could pass.

**Moment 2**

- *What I asked for:* I gave Claude the 3 criteria that I came up with for the criteria.md file and asked how to make it more specific and if there was any ambiguity.
- *What came back:* Claude told me how to test each one, along with narrowing down an actual contradiction in criteria 5
- *What I changed:* I decided to follow Claude and changed my criteria so there was no contradiction. 

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
