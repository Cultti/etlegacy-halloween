"""Write checksums and source provenance for the already built release."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tag')
args = parser.parse_args()
version = (root/'VERSION').read_text().strip()
if args.tag and args.tag != 'v'+version:
    raise SystemExit('Release tag must match VERSION; never move a published tag')
revision = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assets = []
for name in ['zombies.pk3','pumpkins.pk3','halloween-sky.pk3']:
    data = (root/'dist'/name).read_bytes()
    assets.append({'name':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
(root/'dist/SHA256SUMS').write_text(''.join(f"{a['sha256']}  {a['name']}\n" for a in assets))
(root/'dist/manifest.json').write_text(json.dumps({'repository':'Cultti/etlegacy-halloween','version':version,'tag':'v'+version,'revision':revision,'assets':assets},indent=2)+'\n')
