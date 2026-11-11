"""Check generated assets without an SDK or headset; optionally inspect an APK."""
import binascii
import json
import pathlib
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    assets = pathlib.Path(tmp)
    subprocess.run([sys.executable, str(ROOT / 'generate.py'), tmp], check=True)
    catalogue = ET.parse(assets / 'environment_list.xml').getroot()
    assert catalogue.findtext('environment/packageName') == 'boo.puppy.blackhome'
    assert catalogue.findtext('environment/name') == 'snow'
    descriptor = ET.parse(assets / 'resources/snow/environment_information_jxr.xml').getroot()
    variants = descriptor.findall('environment')
    assert len(variants) == 1
    for variant in variants:
        folder = assets / variant.findtext('path')
        assert (folder / variant.findtext('model')).is_file()
        assert (folder / variant.findtext('thumbnail')).is_file()
        assert variant.findtext('skybox') == 'lighting.zip'
    glb = (assets / 'resources/snow/day/black.glb').read_bytes()
    assert struct.unpack_from('<4sII', glb) == (b'glTF', 2, len(glb))
    length, kind = struct.unpack_from('<I4s', glb, 12)
    assert kind == b'JSON' and length % 4 == 0
    model = json.loads(glb[20:20 + length])
    material = model['materials'][0]
    assert material['doubleSided']
    assert material['pbrMetallicRoughness']['baseColorFactor'] == [0, 0, 0, 1]
    assert 'KHR_materials_unlit' in material['extensions']
    offset = 20 + length
    size, kind = struct.unpack_from('<I4s', glb, offset)
    assert kind == b'BIN\0' and offset + 8 + size == len(glb)
    binary = glb[offset + 8:]
    positions = struct.unpack_from('<24f', binary)
    assert set(positions) == {-50, 50}
    assert max(struct.unpack_from('<36H', binary, 96)) < 8
    for path in assets.rglob('*.png'):
        png = path.read_bytes()
        assert png[:8] == b'\x89PNG\r\n\x1a\n'
        offset, compressed = 8, b''
        while offset < len(png):
            size = struct.unpack_from('>I', png, offset)[0]
            kind, data = png[offset + 4:offset + 8], png[offset + 8:offset + 8 + size]
            crc = struct.unpack_from('>I', png, offset + 8 + size)[0]
            assert crc == binascii.crc32(kind + data) & 0xffffffff
            if kind == b'IDAT':
                compressed += data
            offset += size + 12
        assert zlib.decompress(compressed) == b'\0' * (128 * (1 + 128 * 3))
    if len(sys.argv) > 1:
        with zipfile.ZipFile(sys.argv[1]) as apk:
            assert apk.testzip() is None
            assert not any(name.endswith('.dex') for name in apk.namelist())
            for path in assets.rglob('*'):
                if path.is_file():
                    assert apk.read('assets/' + path.relative_to(assets).as_posix()) == path.read_bytes()
            for entry in apk.infolist():
                if entry.filename.endswith(('.glb', '.png', '.zip')):
                    assert entry.compress_type == zipfile.ZIP_STORED
            with zipfile.ZipFile(__import__('io').BytesIO(apk.read('assets/resources/snow/day/lighting.zip'))) as lighting:
                assert lighting.namelist() and lighting.testzip() is None
print('Asset checks passed.')
