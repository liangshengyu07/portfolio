#!/usr/bin/env python3
"""Compress portfolio images and videos for GitHub Pages deployment."""

import os
import subprocess
from PIL import Image

FFMPEG = "/Users/shengyu/Library/Python/3.9/lib/python/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"

def compress_image(input_path, output_path, max_width=1920, quality=85):
    """Compress an image by resizing and/or re-encoding."""
    img = Image.open(input_path)
    original_size = os.path.getsize(input_path)
    
    # Resize if width exceeds max_width
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    # Save as optimized PNG or JPEG based on original format
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.png':
        # Try PNG with optimization; if too large, convert to JPEG
        img = img.convert('RGB')
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
    elif ext == '.jpg' or ext == '.jpeg':
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
    else:
        img.save(output_path, ext.lstrip('.'), optimize=True)
    
    new_size = os.path.getsize(output_path)
    reduction = (1 - new_size / original_size) * 100
    print(f"  {input_path}: {original_size/1024/1024:.2f}MB -> {new_size/1024/1024:.2f}MB ({reduction:.1f}% reduction)")
    return new_size

def compress_video(input_path, output_path, crf=32, preset='fast', max_width=1280):
    """Compress a video using ffmpeg."""
    original_size = os.path.getsize(input_path)
    
    # Get original dimensions
    probe = subprocess.run(
        [FFMPEG, '-i', input_path],
        capture_output=True, text=True
    )
    
    # Use scale filter to limit width while maintaining aspect ratio
    cmd = [
        FFMPEG, '-y', '-i', input_path,
        '-c:v', 'libx264', '-crf', str(crf), '-preset', preset,
        '-vf', f'scale=min({max_width},iw):-2',
        '-c:a', 'aac', '-b:a', '64k',
        '-movflags', '+faststart',
        '-f', 'mp4', output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR compressing {input_path}: {result.stderr[:200]}")
        return original_size
    
    new_size = os.path.getsize(output_path)
    reduction = (1 - new_size / original_size) * 100
    print(f"  {input_path}: {original_size/1024/1024:.2f}MB -> {new_size/1024/1024:.2f}MB ({reduction:.1f}% reduction)")
    return new_size

def main():
    print("=== Compressing images ===")
    
    # Image compression config: (input, output, max_width)
    image_configs = [
        # melos large images
        ('melos/1@2x.png', 'melos/1@2x.png', 1920),
        ('melos/3@2x.png', 'melos/3@2x.png', 1600),
        ('melos/4.1track@2x.png', 'melos/4.1track@2x.png', 1920),
        ('melos/5.2@2x.png', 'melos/5.2@2x.png', 1920),
        ('melos/Frame 77725644@2x.png', 'melos/Frame 77725644@2x.png', 1600),
        ('melos/Frame 77725648@2x.png', 'melos/Frame 77725648@2x.png', 1600),
        ('melos/Frame 77726320@2x.png', 'melos/Frame 77726320@2x.png', 1600),
        ('melos/首页@2x.png', 'melos/首页@2x.png', 1920),
        # idc images
        ('idc1.png', 'idc1.png', 1920),
        ('idc2.png', 'idc2.png', 1920),
        ('idc3.png', 'idc3.png', 1920),
        # dd images (already small, but optimize)
        ('dd1.png', 'dd1.png', 1920),
        ('dd2.png', 'dd2.png', 1920),
        ('dd3.png', 'dd3.png', 1920),
        ('dd4.png', 'dd4.png', 1920),
        ('dd5.png', 'dd5.png', 1920),
        ('dd6.png', 'dd6.png', 1920),
    ]
    
    for inp, out, max_w in image_configs:
        if os.path.exists(inp):
            compress_image(inp, out, max_width=max_w, quality=85)
        else:
            print(f"  SKIP {inp}: not found")
    
    print("\n=== Compressing videos ===")
    
    video_configs = [
        ('videos/hero.mp4', 'videos/hero.mp4', 1280, 32),
        ('videos/part2.mp4', 'videos/part2.mp4', 1280, 32),
        ('videos/part3.mp4', 'videos/part3.mp4', 1280, 32),
        ('part1_hero.mp4', 'part1_hero.mp4', 1280, 32),
    ]
    
    for inp, out, max_w, crf in video_configs:
        if os.path.exists(inp):
            compress_video(inp, out, max_width=max_w, crf=crf)
        else:
            print(f"  SKIP {inp}: not found")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
