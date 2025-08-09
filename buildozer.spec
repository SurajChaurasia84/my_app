[app]
# (str) Title of your application
title = YouTubeDownloader

# (str) Package name
package.name = ytdownloader

# (str) Package domain (reverse-domain style)
package.domain = org.example

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (extensions)
source.include_exts = py,kv,png,jpg,atlas,ttf

# (str) Application versioning
version = 0.1

# (str) The main .py file to use as entry point
# default is main.py, which we use
entrypoint = main.py

# (str) Supported orientations: landscape, portrait or all
orientation = portrait

# (str) Requirements
requirements = python3,kivy==2.3.1,kivymd==1.2.0,yt_dlp

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Min API to target (you may change)
android.minapi = 21
android.sdk = 31
android.ndk = 23b

# (str) Application icon (optional)
# icon.filename = %(source.dir)s/assets/icon.png

# (bool) Add a presplash
# presplash.filename = %(source.dir)s/assets/presplash.png

# Buildozer behavior
log_level = 2
warn_on_root = 1