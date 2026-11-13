# Working on Project S'mores

Notes for Claude Code sessions. This repo is public: nothing personal goes in
here (emails, addresses, account names). Personal notes live in the private
memory repo, `~/github/sienna-camper-memory`, which is linked in as Claude
Code's memory folder on each computer.

## Two computers

- Start of a session: `git pull` here and in `~/github/sienna-camper-memory`.
- End of a session, or when switching computers mid-task: write a
  `SESSION_HANDOFF_<topic>.md` with status, measurements and next steps, then
  commit and push both repos.
- Commit and push only when the owner asks.

## Keep everything in sync

One change usually touches several files. Keep them agreeing:

- `sienna_camper_build_plan.md`: the plan, the source of truth for the text.
- The HTML shop sheets (`*_assembly.html`, `*_tiedown.html`, `bed_risers.html`,
  `window_vent_template.html`, ...).
- `shopping_list.html`.
- `Project_Smores.pdf` and `build_plan.html`: generated, never edited by hand.

Rebuild the PDF with `python3 build_pdf.py`. Shop sheets are appended from the
`DRAWING_SHEETS` list in `build_pdf.py`, so add a new sheet there when it's
ready for the plan. Publish to the site from this repo with
`./publish_plan.py --no-build` (stages it in the portal repo); `--push` deploys
smoresoutdoors.life.

## Shop sheets

- Copy the `<head>` styling from `bed_risers.html` (CSS tokens, dark mode) so
  every sheet looks the same.
- Check a sheet by rendering it (`google-chrome --headless=new --screenshot`)
  and look at the image for overlapping labels before calling it done.
- Open each finished sheet for the owner with `xdg-open`.

## House rules

- No drilling into the van.
- US spelling and inches, to the nearest 1/16".
- Measured beats estimated: say which numbers are photo estimates.
- Hold loose units with a rubber mat and one strap; propose a cleat only when
  nothing else stops it.
- No threadlocker on plastic.
- "Front" can mean the tailgate end (Panel C's side braces); for the window
  vent it means the front of the van. Check which when it matters.
- Save any multi-line shell command to a script file and run the file.
