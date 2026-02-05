# -*- mode: python ; coding: utf-8 -*-
# Lumina Studio - CPU Version Spec File
# This version uses CPU-only PyTorch for maximum compatibility

import sys
import os
from pathlib import Path
import safehttpx
import groovy
import gradio

# Get the project root directory
project_root = Path(SPECPATH).parent if hasattr(SPECPATH, 'parent') else os.path.dirname(os.path.abspath(SPECPATH))

# Get version file paths
safehttpx_version_file = os.path.join(os.path.dirname(safehttpx.__file__), 'version.txt')
groovy_version_file = os.path.join(os.path.dirname(groovy.__file__), 'version.txt')

# Get gradio directory
gradio_dir = os.path.dirname(gradio.__file__)

block_cipher = None

# Collect all gradio files (Python + assets)
gradio_files = []
important_extensions = ('.py', '.svg', '.yaml', '.yml', '.json', '.toml', '.txt', 
                        '.md', '.html', '.css', '.js', '.pyi', '.woff', '.woff2', 
                        '.ttf', '.eot', '.png', '.jpg', '.jpeg', '.gif', '.ico')

for root, dirs, files in os.walk(gradio_dir):
    for file in files:
        if file.endswith(important_extensions):
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, gradio_dir)
            gradio_files.append((full_path, os.path.join('gradio', os.path.dirname(relative_path))))

# Main script
a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        # Include all Python modules
        ('core/*.py', 'core'),
        ('ui/*.py', 'ui'),
        ('utils/*.py', 'utils'),
        ('config.py', '.'),
        # Include icon file if exists
        ('icon.ico', '.') if os.path.exists('icon.ico') else None,
        # Include version files
        (safehttpx_version_file, 'safehttpx'),
        (groovy_version_file, 'groovy'),
        # Include all gradio files
    ] + gradio_files,
    hiddenimports=[
        # Core modules
        'core.calibration',
        'core.converter',
        'core.extractor',
        'core.geometry_utils',
        'core.i18n',
        'core.image_processing',
        'core.image_processing_cuda',
        'core.mesh_generators',
        'core.tray',
        'core.vector_engine',
        # UI modules
        'ui.callbacks',
        'ui.layout',
        'ui.layout_new',
        'ui.styles',
        # Utils modules
        'utils.helpers',
        'utils.lut_manager',
        'utils.stats',
        # Third-party packages
        'gradio',
        'gradio.themes',
        'gradio.blocks_events',
        'gradio.component_meta',
        'numpy',
        'cv2',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'trimesh',
        'trimesh.exchange',
        'scipy',
        'scipy.spatial',
        'torch',
        'torchvision',
        'pystray',
        'colormath',
        'colormath.color_objects',
        'colormath.color_conversions',
        'networkx',
        'lxml',
        'pytz',
        'svglib',
        'reportlab',
        'svgelements',
        'shapely',
        'safehttpx',
        'groovy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude CUDA-related modules for CPU version
        'torch.cuda',
        'torch.backends.cuda',
        'torch.backends.cudnn',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LuminaStudio_CPU',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
