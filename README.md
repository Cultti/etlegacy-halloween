# ET: Legacy Halloween

Zombie players, worn equipment and removable pumpkin helmets for ET: Legacy.
Download the PK3s from [Releases](https://github.com/Cultti/etlegacy-halloween/releases).

| Archive | Contents |
| --- | --- |
| `zombies.pk3` | Zombie faces/exposed skin, distinct worn uniforms for both teams and all five classes, dirty/rusty equipment. Textures only; no model size, animation or hitbox changes. |
| `pumpkins.pk3` | Removable pumpkin caps/helmets and accessory materials. Recorded helmet-loss events throw the pumpkin and reveal the normal or zombie head underneath. |
| `halloween-sky.pk3` | Procedural cloudy sky textures, for a renderer to reference through map sky shaders. |

The archives are independent. Use zombies alone to retain normal helmets. Pumpkin
helmets are deliberately larger than stock helmets and intended for cinematic
demo rendering. These packs change presentation, not gameplay hit detection.
Neither demos nor production servers need modification for demo rendering.

Equipment currently covers MP40, Thompson, syringe/plunger/liquid, pliers,
both grenades, medical/ammo bags, binoculars and Panzerfaust. Unlisted equipment,
including dynamite, knife and landmine, retains stock textures. Original reflection
and glass alpha masks are preserved. The class damage patterns are authored,
not randomly generated. The source includes the selected artwork and prompts.

## Build

Python 3.12+ and Pillow are sufficient; no Blender, game PK3s, credentials or
network access are needed after installing the dependency.

```sh
python -m pip install -r requirements.txt
python scripts/build.py
python -m unittest discover -s tests -v
python scripts/release.py
```

Publishing an immutable `v<VERSION>` GitHub release builds all three archives,
runs checks and attaches the PK3s, `SHA256SUMS` and `manifest.json` to that release.
No runtime/image-generation dependency is required to use the packs. Verify the
checksums before installing. Highlight Studio vendors a checksummed release for
offline rendering and independently selects zombies, pumpkins and atmosphere.

## Artwork and code licensing

Code is GPL-3.0-or-later; see [LICENSE](LICENSE). Procedural pumpkin geometry,
texture and sky artwork are CC0. Zombie and equipment artwork are AI-assisted
edits referencing original Wolfenstein: Enemy Territory UV layouts; original game
artwork rights remain with their owners. The CC0 dedication does not relicense
game-derived artwork or material masks. See [ASSET-LICENSE.txt](ASSET-LICENSE.txt)
and the prompts under `assets/`. This repository does not include original game
models, base game archives or client/server binaries.
