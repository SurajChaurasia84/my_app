[app]

# (str) Title of your application
title = YouTube Downloader

# (str) Package name
package.name = youtube_downloader

# (str) Package domain (used for namespace)
package.domain = org.example

# (str) Source code directory (relative to spec file)
source.dir = .

# (str) Main Python file (entry point)
source.main = main.py

# (str) Application version (you must set this!)
version = 1.0.0

# (list) Source files to include (separated by comma)
source.include_exts = py,kv,png,jpg,txt,md

# (list) Permissions required by your app
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (bool) Legacy external storage access (needed for Android 10+ file access)
android.use_legacy_storage = 1

# (str) Supported orientation (portrait, landscape, all)
orientation = portrait

# (list) Python packages required (PyPI names)
requirements = python3,kivy,kivymd,yt-dlp

# (bool) Use AndroidX libraries (recommended)
android.enable_androidx = 1

# (int) Android API version to use
android.api = 33

# (int) Minimum supported API
android.minapi = 21

# (int) Target API
android.target = 33

# (bool) Package as APK
android.packaging = apk

# (bool) Include Kivy’s default OpenGL ES 2.0 support
android.opengl_es2 = 1

# (bool) Hide status bar
android.hide_statusbar = 0

# (bool) Run in fullscreen
fullscreen = 0

# (str) Entry point of the app
entrypoint = main.py

# (str) Directory where APK is output
dist.dir = bin

# (bool) Copy libraries (fixes build errors in some CI environments)
copy_libs = 1


[buildozer]

# (int) Log level (1 = error, 2 = warn, 3 = info, 4 = debug, 5 = trace)
log_level = 2

# (bool) Force clean builds each time
rebuild = 0

# (str) Build directory
build_dir = .buildozer

# (str) Output directory for APKs and artifacts
bin_dir = bin

# (bool) Show verbose output in logs
verbose = 1
