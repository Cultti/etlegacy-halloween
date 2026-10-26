# Zombie source artwork

Created using the built-in ImageGen tool on 2026-10-25. These are the selected
source images used by `scripts/build-halloween.py`, converted/resized to TGA
with Pillow. Original game atlases were extracted only into ignored
`build/zombie-design/` for inspection/reference, not added to source control.
Body and head geometry, UV coordinates and animation files remain installed
stock assets. See the adjacent license file for attribution.

## head.png

Reference: `models/players/hud/allied_soldier.tga` from operator-owned `pak0.pk3`.

Prompt: Use case: precise-object-edit. Asset type: ET: Legacy game character head UV diffuse texture, NOT a portrait or 3D render. Edit the supplied square UV atlas in place. Preserve EXACT UV positions, outlines, hair coverage, ears, lips, nose, eyebrows, closed eyelids, and neck area at the bottom. Transform ALL visible human skin, including the entire lower neck, into a convincing undead zombie: pale desaturated grey-green corpse skin, bruised purple eye sockets, fine dark veins, cracked dry skin, a few small dark-red wounds. Keep it readable in a low-poly game, detailed hand-painted realistic game diffuse texture style. Preserve dark hair and all background coverage. No new geometry, no enlarged head, no extra eyes/teeth, no skull protrusions, no stem, no pumpkin. Texture must still fit exactly the same UV mapping and include zombie skin all the way to lower edge. Output a square atlas, same composition, no labels or watermark.

## hands.png

Reference: `models/weapons2/mp40/hand16.jpg` from operator-owned `pak0.pk3`.

Prompt: Use case: precise-object-edit. Asset type: ET: Legacy first-person hand UV texture. Edit the supplied square game texture in place. Keep EXACTLY the same UV layout, shapes, finger silhouettes, black leather glove locations, black background, and lighting. Change ONLY exposed skin patches in lower half, the fingers and wrist skin: pale desaturated grey-green zombie skin with purple bruises, fine dark veins and small dark-red scratches, matching undead face skin. Keep all black glove leather unchanged. This is an unfolded texture atlas, not a photo of a hand; do not rearrange, zoom, add hands, add text or watermark. Square image.

## legs.png

Reference: `models/players/temperate/common/bare_legs.jpg` from operator-owned `pak0.pk3`.

Prompt: Use case: precise-object-edit. Asset type: ET: Legacy looted-corpse exposed legs UV diffuse texture atlas. Keep EXACT original tall 1:2 atlas proportions and UV layout: cloth shorts at top, exposed thigh in upper middle, black boots in bottom half, sole on bottom right, all background black. Change ONLY the exposed thigh skin into pale desaturated grey-green zombie skin with bruised purple veins, cracked dry texture and a few dark-red wounds. Keep shorts cloth and black boots unchanged. Do not draw a whole person, do not rearrange any shapes, no text, no watermark. This must remain the same game UV texture.
