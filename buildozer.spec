[app]

# (str) Title of your application
title = YouTube Downloader

# (str) Package name
package.name = youtube_downloader

# (str) Package domain (used for namespace)
package.domain = org.example

# (str) Source code file (main entry point)
source.main = main.py

# (list) Source files to include (relative to your .spec)
source.include_exts = py,kv,png,jpg,atlas

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (bool) Android: request legacy external storage access (for Android 10+)
android.use_legacy_storage = 1

# (str) Supported orientation (portrait|landscape|all)
orientation = portrait

# (list) Application requirements
# These must match PyPI package names.
requirements = python3,kivy,kivymd,yt-dlp

# (str) Presplash screen image (optional)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported Android API
android.api = 33

# (str) Minimum API your APK supports
android.minapi = 21

# (str) Target API your APK supports
android.target = 33

# (bool) Enable AndroidX
android.enable_androidx = 1

# (bool) Package as an APK
android.packaging = apk

# (bool) Include SQLite3
sqlite3 = true

# (bool) Include kivy GLSurfaceView
android.opengl_es2 = True

# (bool) Fullscreen
fullscreen = 0

# (bool) Hide the statusbar
android.hide_statusbar = 0

# (str) Entry point
entrypoint = main.py

# (str) Directory where the .apk will be placed
dist.dir = bin

# (bool) Copy library instead of symlink
copy_libs = 1


[buildozer]

# (str) Log level (1 = error, 2 = warn, 3 = info, 4 = debug, 5 = trace)
log_level = 2

# (bool) Whether to clean up on rebuild
# Set to 1 to force fresh builds during CI
rebuild = 0

# (str) Build folder (default = .buildozer)
build_dir = .buildozer

# (str) Output directory
bin_dir = bin

# (bool) Enable verbose output
verbose = 1

# (str) Custom build command line (useful for CI/CD)
# command = buildozer android debug

