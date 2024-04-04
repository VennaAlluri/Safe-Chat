# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Strt.py'],
    pathex=[],
    binaries=[],
    datas=[('Grp_Server.py', '.'), ('Grp_Client.py', '.'), ('Personal_Server.py', '.'), ('Personal_Client.py', '.'), ('AES.py', '.'), ('Decryption.py', '.'), ('Encryption.py', '.'), ('KeysExpansion.py', '.'), ('RSA.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Strt',
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
)
