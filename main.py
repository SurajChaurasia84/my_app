import os
import re
import threading
import yt_dlp
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivy.utils import platform

# Try to request Android permissions only when running on Android APK
is_android = (platform == "android")
if is_android:
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    except Exception:
        # In some environments (e.g. Pydroid), the permission API may behave differently.
        pass

# Helper to get a sensible default save path
def get_default_save_path():
    if is_android:
        try:
            # try android.storage if available
            from android.storage import primary_external_storage_path
            base = primary_external_storage_path()
            path = os.path.join(base, "Download")
            os.makedirs(path, exist_ok=True)
            return path
        except Exception:
            # fallback common path
            fallback = "/storage/emulated/0/Download"
            try:
                os.makedirs(fallback, exist_ok=True)
            except Exception:
                pass
            return fallback
    else:
        return os.path.join(os.getcwd(), "downloads")  # desktop testing folder

KV = '''
BoxLayout:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(15)
    size_hint: 1, 1

    MDTextField:
        id: url_input
        hint_text: "Enter YouTube URL"
        helper_text: "Paste the video or playlist link"
        helper_text_mode: "on_focus"
        size_hint_y: None
        height: dp(55)
        font_size: app.font_size

    MDRaisedButton:
        text: "Choose Save Folder"
        size_hint_y: None
        height: dp(50)
        on_release: app.file_manager_open()

    MDLabel:
        id: save_path_label
        text: "Save To: " + app.save_path
        halign: "left"
        font_size: app.font_size

    MDLabel:
        text: "Download Type"
        halign: "left"
        font_size: app.font_size
    MDDropDownItem:
        id: type_dropdown
        text: "Video"
        on_release: app.menu_type.open()

    MDLabel:
        text: "Video Quality"
        halign: "left"
        font_size: app.font_size
    MDDropDownItem:
        id: quality_dropdown
        text: "Best"
        on_release: app.menu_quality.open()

    MDRaisedButton:
        text: "Download"
        size_hint_y: None
        height: dp(55)
        md_bg_color: app.theme_cls.primary_color
        on_release: app.start_download_thread()

    MDProgressBar:
        id: progress_bar
        value: 0
        size_hint_y: None
        height: dp(12)
        opacity: 1

    MDLabel:
        id: status_label
        text: "Idle"
        halign: "center"
        theme_text_color: "Secondary"
        font_size: app.font_size
'''

class YouTubeDownloaderApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.save_path = get_default_save_path()
        # Ensure desktop testing folder exists
        if not is_android:
            os.makedirs(self.save_path, exist_ok=True)

        self.font_size = sp(16)
        self.file_manager = MDFileManager(
            exit_manager=self.file_manager_close,
            select_path=self.select_path,
            preview=False
        )
        self.screen = Builder.load_string(KV)

        self.menu_type = MDDropdownMenu(
            caller=self.screen.ids.type_dropdown,
            items=[{"text": t, "on_release": lambda x=t: self.set_type(x)} for t in ["Video", "Audio"]],
            width_mult=3,
        )
        self.menu_quality = MDDropdownMenu(
            caller=self.screen.ids.quality_dropdown,
            items=[{"text": q, "on_release": lambda x=q: self.set_quality(x)} for q in ["360p", "720p", "1080p", "Best"]],
            width_mult=3,
        )

        Window.bind(on_resize=self.adjust_layout)
        # update label text (KV initialized earlier)
        self.screen.ids.save_path_label.text = f"Save To: {self.save_path}"
        return self.screen

    def adjust_layout(self, *args):
        width, height = Window.size
        if width < 500:
            self.font_size = sp(14)
            self.screen.padding = dp(10)
        else:
            self.font_size = sp(16)
            self.screen.padding = dp(20)

    def file_manager_open(self):
        # For Android, MDFileManager will start at /storage; for desktop it will show current dir
        try:
            self.file_manager.show(self.save_path)
        except Exception:
            self.file_manager.show(os.getcwd())

    def file_manager_close(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.save_path = path
        self.screen.ids.save_path_label.text = f"Save To: {path}"
        self.file_manager_close()

    def set_type(self, value):
        self.screen.ids.type_dropdown.set_item(value)
        self.menu_type.dismiss()

    def set_quality(self, value):
        self.screen.ids.quality_dropdown.set_item(value)
        self.menu_quality.dismiss()

    def is_valid_youtube_url(self, url):
        pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        return re.match(pattern, url) is not None

    def update_progress(self, value, status):
        try:
            self.screen.ids.progress_bar.value = value
            self.screen.ids.status_label.text = status
        except Exception:
            pass

    def progress_hook(self, d):
        try:
            status = d.get('status')
            if status == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes', 0)
                percent = int(downloaded / total * 100) if total else 0
                Clock.schedule_once(lambda dt: self.update_progress(percent, f"Downloading... {percent}%"))
            elif status == 'finished':
                Clock.schedule_once(lambda dt: self.update_progress(100, "Finishing..."))
        except Exception:
            pass

    def start_download_thread(self):
        threading.Thread(target=self.start_download, daemon=True).start()

    def start_download(self):
        url = self.screen.ids.url_input.text.strip()

        if not url:
            Clock.schedule_once(lambda dt: self.update_progress(0, "Please enter URL"))
            return

        if not self.is_valid_youtube_url(url):
            Clock.schedule_once(lambda dt: self.update_progress(0, "Invalid URL"))
            return

        download_type = self.screen.ids.type_dropdown.text
        quality = self.screen.ids.quality_dropdown.text

        # Choose formats that avoid merging (prefer mp4 for video, m4a for audio)
        if download_type == "Video":
            format_code = {
                "360p": "best[height<=360][ext=mp4]/best[height<=360]",
                "720p": "best[height<=720][ext=mp4]/best[height<=720]",
                "1080p": "best[height<=1080][ext=mp4]/best[height<=1080]",
                "Best": "best[ext=mp4]/best"
            }.get(quality, "best[ext=mp4]/best")

            ydl_opts = {
                'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
                'format': format_code,
                'progress_hooks': [self.progress_hook],
                'ignoreerrors': True,
                'retries': 5,
                'nocheckcertificate': True
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'progress_hooks': [self.progress_hook],
                'ignoreerrors': True,
                'retries': 5,
                'nocheckcertificate': True
            }

        try:
            self.update_progress(0, "Starting download...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: self.update_progress(100, "Download completed!"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_progress(0, f"Error: {e}"))

if __name__ == "__main__":
    YouTubeDownloaderApp().run()