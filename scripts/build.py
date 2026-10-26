"""Build removable pumpkin helmets, zombie texture replacements and cloud skies.

No stock game models are copied. Dimensions match the stock head's tag_head space:
forward +X, up +Z. Original player head/body models are never replaced.
"""
import math
import pathlib
import struct
import zipfile
from io import BytesIO
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/pumpkins.pk3'
SHADER = 'studio/halloween/pumpkin'


def text(s, n):
    return s.encode('ascii').ljust(n, b'\0')


def md3(empty=False, helmet=False):
    vertices, uv, triangles = [], [], []
    columns, rows = 40, 20
    for j in range(rows + 1):
        v = j / rows
        phi = math.pi * v
        for i in range(columns + 1):
            u = i / columns
            theta = 2 * math.pi * (u - .5)
            radius = 7.2 * math.sin(phi) * (1 + .065 * math.cos(theta * 10))
            vertices.append((radius * math.cos(theta), radius * math.sin(theta), 4.4 + 7.6 * math.cos(phi)))
            uv.append((u, v))
    for j in range(rows):
        for i in range(columns):
            a = j * (columns + 1) + i
            # Outward winding: theta then phi.
            triangles.extend([(a, a + columns + 1, a + 1), (a + 1, a + columns + 1, a + columns + 2)])
    # Small bent stem, using a solid brown corner of the texture.
    start = len(vertices)
    for z, x, radius in [(11.6, 0, .85), (14.0, -.7, .5)]:
        for i in range(8):
            t = i * math.tau / 8
            vertices.append((x + radius * math.cos(t), radius * math.sin(t), z))
            uv.append((.01, .01))
    for i in range(8):
        a, b = start + i, start + (i + 1) % 8
        triangles.extend([(a, b, a + 8), (b, b + 8, a + 8)])
    for i in range(1, 7):
        triangles.append((start + 8, start + 8 + i, start + 9 + i))
    if helmet:
        # Inverse of the stock head frame-0 tag_mouth transform. The engine
        # attaches the accessory to the original animated mouth tag itself.
        vertices = [(.99994725*(x+.34375)-.01027343*(z-.6875), y,
                     .01027343*(x+.34375)+.99994725*(z-.6875)) for x, y, z in vertices]
    frames = 1 if empty or helmet else 401
    mins = [min(v[i] for v in vertices) for i in range(3)]
    maxs = [max(v[i] for v in vertices) for i in range(3)]
    frame = struct.pack('<10f16s', *mins, *maxs, 0, 0, 0, 16, text('pumpkin helmet', 16))
    tag = struct.pack('<64s12f', text('tag_mouth', 64), 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1)
    surface = b''
    if not empty:
        tris = b''.join(struct.pack('<3i', *t) for t in triangles)
        shader = struct.pack('<64si', text(SHADER, 64), 0)
        coords = b''.join(struct.pack('<2f', *t) for t in uv)
        packed = []
        for x, y, z in vertices:
            normal = (x, y, (z - 4) * .9)
            length = math.sqrt(sum(a*a for a in normal)) or 1
            lat = round(math.acos(max(-1, min(1, normal[2]/length))) * 255 / math.tau) & 255
            lng = round(math.atan2(normal[1], normal[0]) * 255 / math.tau) & 255
            packed.append(struct.pack('<3hH', *(round(a*64) for a in (x, y, z)), (lng << 8) | lat))
        xyz = b''.join(packed) * frames
        a, b, c = 108, 108 + len(tris), 108 + len(tris) + len(shader)
        d = c + len(coords)
        surface = struct.pack('<4s64s10i', b'IDP3', text('head', 64), 0, frames, 1, len(vertices), len(triangles), a, b, c, d, d+len(xyz)) + tris + shader + coords + xyz
    tags_offset = 108 + 56 * frames
    tags = 0 if helmet else 1
    surface_offset = tags_offset + 112 * frames * tags
    header = struct.pack('<4si64s9i', b'IDP3', 15, text('Studio pumpkin helmet', 64), 0, frames, tags, 0 if empty else 1, 0, 108, tags_offset, surface_offset, surface_offset + len(surface))
    return header + frame * frames + tag * frames * tags + surface


def texture():
    size = 512
    # Original opaque painted carving: dark inset eyes/mouth, orange rim.
    pixels = bytearray()
    for y in range(size):
        v = y / (size-1)
        for x in range(size):
            u = x / (size-1)
            t = (u - .5) * math.tau
            rib = .83 + .17 * math.cos(t*10)
            light = .75 + .25 * math.sin(math.pi*v)
            color = (int(235*rib*light), int(104*rib*light), 12)
            eye = any(abs(u-center) < .048 * max(0, 1-abs(v-.40)/.075) for center in [.425, .575])
            nose = abs(u-.5) < .022 * max(0, 1-abs(v-.51)/.05)
            mouth = abs(u-.5)<.12 and .565 < v < .65 - .035*abs((u-.5)/.12)
            tooth = (abs(u-.46)<.013 or abs(u-.54)<.013) and (v<.59 or v>.625)
            if eye or nose or (mouth and not tooth):
                color = (29, 12, 3)
            if u < .025 and v < .025:
                color = (75, 48, 16)
            pixels.extend(reversed(color))
    return struct.pack('<BBBHHBHHHHBB', 0, 0, 2, 0, 0, 0, 0, 0, size, size, 24, 32) + pixels


def build():
    files = {'studio/halloween/pumpkin.tga': texture(),
             'scripts/studio_halloween.shader': (SHADER+'\n{\n cull disable\n {\n map studio/halloween/pumpkin.tga\n rgbGen lightingDiffuse\n }\n}\n').encode()}
    def zombie(name, size):
        image = Image.open(ROOT/f'assets/zombie/{name}.png').convert('RGB').resize(size, Image.Resampling.LANCZOS)
        result = BytesIO()
        image.save(result, format='TGA', compression=None)
        return result.getvalue()
    head = zombie('head', (512, 512))
    hands = zombie('hands', (256, 256))
    legs = zombie('legs', (256, 512))
    zombie_files = {}
    zombie_files['models/weapons2/mp40/hand16.tga'] = hands
    for suffix in ['', '_2']:
        zombie_files[f'models/players/temperate/common/bare_legs{suffix}.tga'] = legs
    # Continuous world-direction cloud field, sampled onto all six cube faces.
    # Original procedural CC0 sky: no downloads and no baked map-specific light.
    for face in ['rt', 'lf', 'ft', 'bk', 'up', 'dn']:
        size = 256
        pixels = bytearray()
        for j in range(size):
            for i in range(size):
                u, v = 2*i/(size-1)-1, 1-2*j/(size-1)
                direction = {'rt': (1, -u, v), 'lf': (-1, u, v),
                             'bk': (u, 1, v), 'ft': (-u, -1, v),
                             'up': (-v, -u, 1), 'dn': (v, -u, -1)}[face]
                length = math.sqrt(sum(x*x for x in direction))
                x, y, z = [a/length for a in direction]
                cloud = sum(math.sin((x*2.7+y*1.9+z*4.3)*f + math.sin(y*f*2.1-x*f)) / f
                            for f in [2, 4, 8, 16])
                cloud = max(0, min(1, .5+cloud*.65)) ** 1.5
                color = (int(12+cloud*32), int(20+cloud*36), int(34+cloud*43))
                pixels.extend(reversed(color))
        files[f'studio/halloween/clouds_{face}.tga'] = struct.pack('<BBBHHBHHHHBB', 0, 0, 2, 0, 0, 0, 0, 0, size, size, 24, 32) + pixels
    for team in ['allied', 'axis']:
        for role in ['cvops', 'engineer', 'field', 'medic', 'soldier']:
            zombie_files[f'models/players/hud/{team}_{role}.tga'] = head
        for hat in ['cap', 'helmet']:
            files[f'models/players/temperate/{team}/{hat}.md3'] = md3(helmet=True)
        for role in ['cvops', 'engineer', 'fieldops', 'medic', 'soldier']:
            hat = 'cap' if role == 'cvops' else 'helmet'
            files[f'models/players/temperate/{team}/{hat}_{role}.skin'] = f'head, "{SHADER}"\n'.encode()
    for hat in ['rank_cap', 'rank_helmet']:
        files[f'models/players/temperate/common/{hat}.md3'] = md3(empty=True)
    # Texture-only archive: no shaders, skins, geometry, scripts or executable code.
    import json
    uniforms = ROOT/'assets/zombie/uniforms'
    for name, spec in json.loads((uniforms/'manifest.json').read_text()).items():
        image = Image.open(uniforms/f'{name}.png').convert('RGB').resize(tuple(spec['size']), Image.Resampling.LANCZOS)
        result = BytesIO()
        if spec['path'].endswith('.jpg'):
            image.save(result, format='JPEG', quality=95, subsampling=0)
        else:
            image.save(result, format='TGA', compression=None)
        zombie_files[spec['path']] = result.getvalue()
    # Equipment is part of the texture-only zombie treatment. Original alpha
    # masks are authored inputs; no proprietary pak0 is needed at build time.
    equipment = ROOT/'assets/equipment'
    for name, spec in json.loads((equipment/'manifest.json').read_text()).items():
        if spec.get('status', '').startswith('blocked:'):
            continue
        image = Image.open(equipment/f'{name}.png').convert('RGB').resize(tuple(spec['size']), Image.Resampling.LANCZOS)
        if spec.get('alphaSHA256'):
            import hashlib
            mask = Image.open(equipment/'alpha'/f'{name}.png').convert('L')
            assert mask.size == image.size
            assert hashlib.sha256(mask.tobytes()).hexdigest() == spec['alphaSHA256']
            image.putalpha(mask)
        result = BytesIO()
        if spec['path'].endswith('.jpg'):
            image.save(result, format='JPEG', quality=95, subsampling=0)
        else:
            image.save(result, format='TGA', compression=None)
        zombie_files[spec['path']] = result.getvalue()
    license = (ROOT/'ASSET-LICENSE.txt').read_bytes()
    for destination, entries in [(OUT, files), (OUT.with_name('zombies.pk3'), zombie_files), (OUT.with_name('halloween-sky.pk3'), {n:b for n,b in files.items() if n.startswith('studio/halloween/clouds_')})]:
        if destination == OUT:
            entries = {n:b for n,b in entries.items() if not n.startswith('studio/halloween/clouds_')}
        entries['STUDIO-ASSET-LICENSE.txt'] = license
        destination.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted(entries.items()):
                info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data)
        print(destination)


if __name__ == '__main__':
    build()
