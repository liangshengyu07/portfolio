import requests
import os
import re
import sys
from urllib.parse import urljoin, urlparse

HLS_URL = "https://stream.mux.com/tLkHO1qZoaaQOUeVWo8hEBeGQfySP02EPS02BmnNFyXys.m3u8"
OUTPUT_DIR = "/Users/shengyu/Documents/kimi/workspace/codenest-hero"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "background.mp4")

def download_hls_stream():
    print(f"Fetching master playlist: {HLS_URL}")
    resp = requests.get(HLS_URL, timeout=30)
    resp.raise_for_status()
    master_content = resp.text
    print(f"Master playlist length: {len(master_content)} chars")

    # Find variant playlists (lines that are URLs, not comments, and not .m3u8 header)
    lines = [l.strip() for l in master_content.splitlines() if l.strip() and not l.startswith('#')]
    
    if not lines:
        print("No variant playlists found, treating as media playlist directly.")
        media_url = HLS_URL
    else:
        # Check if it's a master playlist (has .m3u8 references) or already a media playlist
        m3u8_lines = [l for l in lines if l.endswith('.m3u8') or '.m3u8' in l]
        if m3u8_lines:
            # Master playlist - pick the last/highest quality variant
            variant_path = m3u8_lines[-1]
            media_url = urljoin(HLS_URL, variant_path)
            print(f"Selected variant: {media_url}")
        else:
            # Already a media playlist
            media_url = HLS_URL

    # Fetch media playlist
    print(f"Fetching media playlist: {media_url}")
    resp = requests.get(media_url, timeout=30)
    resp.raise_for_status()
    media_content = resp.text
    print(f"Media playlist length: {len(media_content)} chars")

    # Parse media playlist for segments
    base_url = media_url
    segment_urls = []
    for line in media_content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Could be relative or absolute URL
        segment_url = urljoin(base_url, line)
        segment_urls.append(segment_url)

    print(f"Found {len(segment_urls)} segments")
    if not segment_urls:
        print("ERROR: No segments found in media playlist")
        sys.exit(1)

    # Download segments
    temp_dir = os.path.join(OUTPUT_DIR, "segments")
    os.makedirs(temp_dir, exist_ok=True)

    segment_files = []
    for i, seg_url in enumerate(segment_urls):
        seg_path = os.path.join(temp_dir, f"segment_{i:05d}.ts")
        segment_files.append(seg_path)
        if os.path.exists(seg_path) and os.path.getsize(seg_path) > 0:
            print(f"  [{i+1}/{len(segment_urls)}] Already exists: {seg_path}")
            continue
        print(f"  [{i+1}/{len(segment_urls)}] Downloading: {seg_url}")
        try:
            seg_resp = requests.get(seg_url, timeout=30, stream=True)
            seg_resp.raise_for_status()
            with open(seg_path, 'wb') as f:
                for chunk in seg_resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"      Saved: {os.path.getsize(seg_path)} bytes")
        except Exception as e:
            print(f"      ERROR downloading segment: {e}")

    # Concatenate all segments into a single TS file
    concat_file = os.path.join(OUTPUT_DIR, "concatenated.ts")
    print(f"\nConcatenating {len(segment_files)} segments into {concat_file}")
    with open(concat_file, 'wb') as outf:
        for seg_path in segment_files:
            if os.path.exists(seg_path):
                with open(seg_path, 'rb') as inf:
                    outf.write(inf.read())
    
    concat_size = os.path.getsize(concat_file)
    print(f"Concatenated TS size: {concat_size} bytes ({concat_size / (1024*1024):.2f} MB)")

    # Try to convert to MP4 using ffmpeg
    import subprocess
    try:
        ffmpeg_check = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if ffmpeg_check.returncode == 0:
            print(f"\nConverting to MP4: {OUTPUT_FILE}")
            result = subprocess.run([
                'ffmpeg', '-y', '-i', concat_file, 
                '-c', 'copy', '-bsf:a', 'aac_adtstoasc',
                OUTPUT_FILE
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"MP4 created: {OUTPUT_FILE}")
                print(f"Size: {os.path.getsize(OUTPUT_FILE)} bytes")
                # Clean up temp files
                for seg_path in segment_files:
                    os.remove(seg_path)
                os.remove(concat_file)
                os.rmdir(temp_dir)
                return
            else:
                print(f"ffmpeg conversion failed: {result.stderr}")
        else:
            print("ffmpeg not available, keeping as TS file")
    except FileNotFoundError:
        print("ffmpeg not found, keeping as TS file")

    # Fallback: rename TS to MP4 (may work for some players)
    os.rename(concat_file, OUTPUT_FILE)
    print(f"Saved as: {OUTPUT_FILE}")
    print("Note: File is MPEG-TS format. Use ffmpeg to convert to MP4 if needed.")

if __name__ == '__main__':
    download_hls_stream()
