import requests
import os
from urllib.parse import urljoin

HLS_URL = "https://stream.mux.com/tLkHO1qZoaaQOUeVWo8hEBeGQfySP02EPS02BmnNFyXys.m3u8"
OUTPUT = "/Users/shengyu/Documents/kimi/workspace/videos/hero.mp4"

def download():
    # 1. Master playlist
    master = requests.get(HLS_URL, timeout=30).text
    lines = [l.strip() for l in master.splitlines() if l.strip() and not l.startswith('#')]
    variant_url = urljoin(HLS_URL, lines[0])  # highest quality
    print(f"Variant: {variant_url}")

    # 2. Media playlist
    media = requests.get(variant_url, timeout=30).text
    print("Media playlist:\n", media[:1500])

    base = variant_url

    # 3. Parse init segment and media segments
    init_url = None
    segments = []
    for line in media.splitlines():
        line = line.strip()
        if line.startswith('#EXT-X-MAP:'):
            # Extract URI
            uri = line.split('URI="')[1].split('"')[0]
            init_url = urljoin(base, uri)
        elif line and not line.startswith('#'):
            segments.append(urljoin(base, line))

    print(f"Init: {init_url}")
    print(f"Segments ({len(segments)}): {segments[:5]}...")

    # 4. Download all parts
    parts = []
    if init_url:
        print(f"Downloading init...")
        r = requests.get(init_url, timeout=30)
        r.raise_for_status()
        parts.append(r.content)
        print(f"  Init size: {len(r.content)}")

    for i, seg in enumerate(segments):
        print(f"Downloading segment {i+1}/{len(segments)}: {seg}")
        r = requests.get(seg, timeout=30)
        r.raise_for_status()
        parts.append(r.content)
        print(f"  Size: {len(r.content)}")

    # 5. Concatenate
    total = sum(len(p) for p in parts)
    print(f"\nTotal size: {total / (1024*1024):.2f} MB")

    with open(OUTPUT, 'wb') as f:
        for p in parts:
            f.write(p)
    print(f"Saved to: {OUTPUT}")

    # 6. Verify header
    with open(OUTPUT, 'rb') as f:
        header = f.read(16)
        print(f"File header: {header[:8]}")
        if header[4:8] == b'ftyp':
            print("✅ Looks like a valid MP4 (ftyp found)")
        elif header[4:8] == b'moov':
            print("✅ Looks like a valid MP4 (moov found)")
        else:
            print(f"⚠️ Unexpected header: {header.hex()}")

if __name__ == '__main__':
    download()
