# Session handoff: WAVE 3 window vent panel

*Written 13 Nov 2026. Picking this up on another machine.*

The full design is **Appendix J** of `sienna_camper_build_plan.md`: the options, the layout, the sizing formulas, the measuring sheet and the results table. This file is the short version, plus what to do next.

## Status

Designed but not built. Every measurement has been taken (12 Nov 2026). **Next: cut the cardboard template and test-fit it.**

## The setup

- **Van:** 2026 Sienna Woodland. Nothing gets drilled.
- **Window:** the driver-side sliding door, glass all the way down. The panel sits in the opening above the glass and stands in the glass's side channels.
- **Corner trim:** the curved upper corner trim (6⅞" radius) sits *behind* the glass. The glass slides in front of it, so the panel can be a plain rectangle.
- **Orientation:** looking from inside, the front of the van is on your right.
- **Chosen design:** Option B, a rigid window insert. Both hoses lock into it by their collars. Pieces from the fabric window kit can be reused to seal the gaps.

## Measurements (12 Nov 2026)

| Ref | What | Value |
|---|---|---|
| J3 | Opening width | 34" |
| J4 | Width (second reading) | ~33⅜" |
| J1 | Top of opening to top of glass, at the middle, glass fully down | 12¾" |
| K1 | Same reading from inside, from the top trim | 12¾": the trim doesn't hang below the opening, so it can't cover the holes |
| J7 | | ⅜" |
| J8 / J9 | Front / rear side channel depth | ¾" each |
| J10 | Corner trim radius (behind the glass) | 6⅞" |
| J11 | Glass thickness | 3 mm |
| — | Intake collar body diameter | 6 1/16" |
| — | Exhaust collar body diameter | 5" |
| — | Collar length | ~1–1¼" |
| — | Hose lengths | intake 54", exhaust 55" |
| J20 | Door trim to platform edge, door shut, where the hoses pass | 7": clears the 6" intake hose |
| J21 | Deck height, cargo floor to top of deck | 22¾" |
| J22 / J23 | Drain | Not needed: condensate is handled separately |

The J4 and J7 rows only carry the bare readings here. Appendix J has the full wording for each.

## The panel

- **Size:** 34 11/16" wide × 9¾" tall.
- **Intake hole:** 6⅛" diameter.
- **Exhaust hole:** 5 1/16" diameter.
- **Hole height:** both centers are 4⅞" down from the top edge.
- **Hole spacing:** each center is 9" in from its end of the opening, so the two are 16" apart.
- **Fit in the channels:** one end tucks ¾" into its channel and the other clears by 1/16", so the panel can be swung in and slid over.

## Next steps

1. **Template:** cut a cardboard or trifold science-project board of at least 36" × 12". Try a craft store, Walmart, Target, or a big-box store's free moving boxes. Mark the 34 11/16" × 9¾" rectangle and both holes.
2. **Test-fit:** check the tuck-and-slide fit in the channels. Check that the hoses seat and lock with their collars and that they clear the platform edge. Check that the door still shuts.
3. **Adjust:** fix the template, then write any changed numbers into Appendix J.
4. **Build:** make the real insert from the materials in Appendix J, then seal the edges and the hoses.
5. **After changes:** update Appendix J's results table and status. Then rebuild the PDF with `python3 build_pdf.py` and publish it from the portal repo with `publish_plan.py --no-build`, then commit and push. A push to the portal's master deploys smoresoutdoors.life.

## Other open items from the same session

- **Hose clamps:** the seam hose clamps on the B/C seams, both driver and passenger side, have their screw housings on top. The plan says to turn the housing outward or underneath. Rotate them and re-shoot the photos.
- **Italic PDF:** the whole PDF renders in italic because Chrome picks LiberationSans-Italic. This dates back to at least Oct 1. A font fix in `build_pdf.py` is still open.
- **PDF size:** the PDF is about 55 MB, over GitHub's recommended 50 MB.
