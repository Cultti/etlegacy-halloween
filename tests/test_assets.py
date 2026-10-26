import hashlib
from io import BytesIO
import json
from pathlib import Path
import runpy
import unittest
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class AssetTests(unittest.TestCase):
    def test_zombies_are_texture_only_and_cover_all_classes_and_equipment(self):
        with zipfile.ZipFile(ROOT/'dist/zombies.pk3') as archive:
            names = archive.namelist()
            self.assertTrue(all(n.endswith(('.tga','.jpg')) or n == 'STUDIO-ASSET-LICENSE.txt' for n in names))
            for team in ['allied','axis']:
                for role in ['cvops','engineer','field','medic','soldier']:
                    self.assertIn(f'models/players/hud/{team}_{role}.tga',names)
            for name,spec in json.loads((ROOT/'assets/equipment/manifest.json').read_text()).items():
                if spec.get('status'):
                    self.assertNotIn(spec['path'],names)
                    continue
                image = Image.open(BytesIO(archive.read(spec['path'])))
                self.assertEqual(list(image.size),spec['size'])
                if spec.get('alphaSHA256'):
                    self.assertEqual(hashlib.sha256(image.getchannel('A').tobytes()).hexdigest(),spec['alphaSHA256'])

    def test_pumpkin_models_are_removable_accessories_and_sky_is_separate(self):
        import struct
        with zipfile.ZipFile(ROOT/'dist/pumpkins.pk3') as archive:
            self.assertFalse(any(n.startswith('models/players/hud/') or 'clouds_' in n for n in archive.namelist()))
            for team in ['allied','axis']:
                for hat in ['cap','helmet']:
                    model = archive.read(f'models/players/temperate/{team}/{hat}.md3')
                    self.assertEqual(model[:4],b'IDP3')
                    self.assertEqual(struct.unpack_from('<2i',model,76),(1,0))
        with zipfile.ZipFile(ROOT/'dist/halloween-sky.pk3') as archive:
            self.assertEqual(len([n for n in archive.namelist() if 'clouds_' in n]),6)
            self.assertFalse(any(n.startswith('models/') for n in archive.namelist()))

    def test_build_is_byte_reproducible(self):
        files = list((ROOT/'dist').glob('*.pk3'))
        before = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        runpy.run_path(str(ROOT/'scripts/build.py'),run_name='__main__')
        self.assertEqual(before,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})


if __name__ == '__main__':
    unittest.main()
