# Credits to "Code with Josh (YT)"
import flet as ft
import os, subprocess
import flet_audio, murf
from typing import Optional, Any
import time, datetime, requests, logging


logging.getLogger(__name__)
MURF_AI_API_KEY_KEY_ID = "MURF_API_KEY" # Key used to identify the API Key


class TextToSpeech:
    def __init__(self, text: str, voice_id: str, audio_duration: Optional[float], encode_as_base_64: Optional[bool]):
        self.text = text
        self.voice_id = voice_id
        self.audio_duration = audio_duration
        self.encode_as_base_64 = encode_as_base_64
        
        self.murf_ai_api_key = os.environ.get(MURF_AI_API_KEY_KEY_ID)
        self.murf_client = murf.Murf(api_key=self.murf_ai_api_key)
    
    def generate(self):
        audio_res = self.murf_client.text_to_speech.generate(
            text=self.text,
            voice_id=self.voice_id,
            audio_duration=self.audio_duration,
            encode_as_base_64=self.encode_as_base_64,
            format="MP3",
            sample_rate=48000.0,
            channel_type="STEREO",
        )
        return audio_res
    
    def save_file(self, audio_url: str):
        if not audio_url:
            audio_url = self.generate().audio_file
        
        try:
            response = requests.get(audio_url, stream=True)
            if response.status_code != 200:
                return False, f"Error getting the audio file. Status code: {response.status_code}"
            
            base_dir = os.path.join("storage", "text_to_audio")
            os.makedirs(base_dir, exist_ok=True) # create directory if it doesn't exist
            file_name = f"Audio_{str(datetime.datetime.now()).strip()}.mp3"
            file_path = os.path.join(base_dir, file_name)
            
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                return True, f"Audio file saved as: {file_path}", file_path
        
        except Exception as e:
            return False, f"Error saving the file: {e}", None
    
    
    @staticmethod
    def get_voice_data_by_id(voice_id: str):
        voices = TextToSpeech.get_all_voices()
        for voice in voices:
            if voice.voice_id == voice_id:
                return voice
        return None
    
    @staticmethod
    def get_all_voices():
        return murf.Murf(api_key=os.environ.get(MURF_AI_API_KEY_KEY_ID)).text_to_speech.get_voices()



class TextToAudioPage(ft.Column):
    """ TextToAudio page of the application. """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.adaptive = True
        self.page.title = f"Flet Demo Apps - Text to Audio"
        
        # custom consts (shared fields dimensions)
        self.FIELD_WIDTH = 500
        self.FIELD_BORDER_WIDTH = 0.3
        self.FIELD_BORDER_RADIUS = 5
    
    def build(self):
        self.page.update()
        
        if not self.api_key_exists_in_environ:
            return self.display_api_key_form()
        return self.build_content()
    
    
    def build_content(self):
        self.page.update()
        
        # check for right API Key.
        self._check_api_validity()
        
        
        # text input field
        self.text_to_convert = ft.TextField(
            label="Enter the text to convert",
            autofocus=True,
            multiline=True,
            min_lines=3,
            max_lines=10,
            width=self.FIELD_WIDTH,
            border=ft.InputBorder.OUTLINE,
            border_width=self.FIELD_BORDER_WIDTH,
            border_radius=self.FIELD_BORDER_RADIUS,
            expand=True,
        )
        
        # choose voice options
        self.voice_options = ft.Dropdown(
            label="Choose a voice",
            editable=True,
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            leading_icon=ft.Icons.SEARCH,
            width=self.FIELD_WIDTH,
            options=[
                ft.DropdownOption(key=voice.voice_id, text=voice.display_name + f" {voice.locale}", data=voice)
                for voice in TextToSpeech.get_all_voices()
            ]
        )
        
        
        # save audio if checked
        self.should_save_audio = ft.Switch(label="Save audio file", value=True, width=self.FIELD_WIDTH, adaptive=True)
        
        
        self.progress_display = ft.Column(visible=False)
        
        self.submit_button = ft.ElevatedButton(
            text="Generate",
            icon=ft.Icons.CHANGE_CIRCLE,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.ZOOM_OUT),
            on_click=self.convert_text_to_audio,
        )
        
        self.audio_container = ft.Column()
        
        
        self.form_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Convert Text to Audio using Murf AI", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    self.voice_options,
                    self.should_save_audio,
                    self.text_to_convert,
                    self.progress_display,
                    self.submit_button,
                    self.audio_container,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ), # End Column,
            padding=30,
            width=600,
            border_radius=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(blur_radius=0, color=ft.Colors.BLACK12),
        )
        
        self.converter_area = ft.Column(
            controls=[self.form_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(self.converter_area))
        self.page.update()
    
    
    def _check_api_validity(self):
        """ Try to connect to the API. If connection refused due to API-Key, then redirect the user to setting a valid API Key """
        try:
            TextToSpeech.get_all_voices()
        
        except murf.errors.BadRequestError as e:
            error_details = e.args[0]
            error_message = error_details.get("errorMessage", "No error message provided")
            msg = f"Unable to connect to the API with the given key ({error_message})"
            
            self.page.open(ft.AlertDialog(title=ft.Text("Invalid API Key"), content=ft.Text(msg)))
            self.page.update()
            return self.display_api_key_form()
        
        except Exception as e:
            error_message = e.args[0].get("errorMessage", "No error message provided")
            msg = f"Unable to connect to the API with the given Key. Please set a new one. Error: {error_message}"
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(msg)))
            self.page.update()
            return self.display_api_key_form()
    
    
    def display_api_key_form(self):
        # no need to check if api exists here. Because it's possible to set a new one
        self.ask_api_key = ft.TextField(
            label="Enter Your API Key",
            autofocus=True,
            width=self.FIELD_WIDTH,
            border=ft.InputBorder.OUTLINE,
            border_width=self.FIELD_BORDER_WIDTH,
            border_radius=self.FIELD_BORDER_RADIUS,
            expand=True,
        )
        
        self.api_key_success_msg = ft.Text(visible=False)
        
        self.submit_api_key = ft.ElevatedButton(
            text="Save API Key",
            icon=ft.Icons.SAVE,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.ZOOM_OUT),
            on_click=self._save_api_key_to_environ,
        )
        
        self.form_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Convert Text to Audio using Murf AI", 
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        value="Your Murf AI API Key is missing. Enter it in the field below to save it in your environment variables.",
                        weight=ft.FontWeight.NORMAL,
                        # text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        value="Don't worry, no one can access it. Feel free to read the docs (or the source code) for more.",
                        weight=ft.FontWeight.NORMAL,
                        color=ft.Colors.GREY_700,
                        font_family="italic",
                        # text_align=ft.TextAlign.CENTER
                    ),
                    self.ask_api_key,
                    self.api_key_success_msg,
                    self.submit_api_key,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ), # End Column,
            padding=30,
            width=600,
            border_radius=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(blur_radius=0, color=ft.Colors.BLACK12),
        )
        
        self.api_key_form_area = ft.Column(
            controls=[self.form_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(self.api_key_form_area))
    
    
    def _set_env_var_based_on_platform(self, key: str, val: Any):
        """ Execute a sub cmd to save the env var based on the operating system """
        try:
            os.environ[key] = val
            # os.environ.setdefault(key=key, value=val)
            
            if self.page.platform == ft.PagePlatform.MACOS:
                command = f"export {key}={val}"
            elif self.page.platform == ft.PagePlatform.WINDOWS:
                command = f"set {key}={val}"
            elif self.page.platform == ft.PagePlatform.LINUX:
                command = f"export {key}={val}"
            else:
                return False, "Platform (or OS) not supported yet"
            
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return True, "Key saved successfully!"
            
            return False, result.stderr.decode()
        except Exception as e:
            return False, f"Error saving key into environment variables: {e}"
    
    
    def _save_api_key_to_environ(self, e):
        submited_api_key = self.ask_api_key.value.strip()
        
        if not submited_api_key or submited_api_key == "":
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Please enter a key (not empty string)")))
            self.page.update()
            return
        
        saved, msg = self._set_env_var_based_on_platform(key=MURF_AI_API_KEY_KEY_ID, val=submited_api_key)
        
        if not saved:
            self.api_key_success_msg.value = str(msg)
            self.api_key_success_msg.color = ft.Colors.RED
            self.api_key_success_msg.visible = True
            self.page.update()
        
        else: # key saved
            self.api_key_success_msg.value = "API Key added to environment successfully!"
            self.api_key_success_msg.color = ft.Colors.GREEN
            self.api_key_success_msg.visible = True
            self.page.update()
            
            time.sleep(1.5) # just for vusual stuffs
            
            # hide the current area
            self.api_key_form_area.controls.clear()
            
            # display the main content now
            self.build()
    
    
    @property
    def api_key_exists_in_environ(self):
        # do not use the "MURF_AI_API_KEY" const because its value could be null from the start. Just try to get the newest one
        return os.environ.get(MURF_AI_API_KEY_KEY_ID) is not None
    
    def convert_text_to_audio(self, e):
        text_value = self.text_to_convert.value.strip()
        selected_voice = self.voice_options.value
        
        if not selected_voice:
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Please select a voice to convert the text.")))
            self.page.update()
            return
        
        if selected_voice not in (voice.voice_id for voice in TextToSpeech.get_all_voices()):
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"Please select a valid voice ({selected_voice} isn't valid).")))
            self.page.update()
            return
        
        if not text_value or text_value == "":
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Please enter the text to convert.")))
            self.page.update()
            return
        
        try:
            audio_duration = None
            encode_as_base_64 = False
            tts = TextToSpeech(text=text_value, voice_id=selected_voice, audio_duration=audio_duration, encode_as_base_64=encode_as_base_64)
            
            # displaying progress
            progress_text = ft.Text(value="Converting text to audio …")
            progress = ft.ProgressRing(width=16, height=16, stroke_width=2)
            
            self.progress_display.controls.clear()
            self.progress_display.controls.append(ft.Row([progress, progress_text], alignment=ft.MainAxisAlignment.CENTER))
            self.progress_display.visible = True
            self.progress_display.update()
            
            # converting
            audio_res = tts.generate()
            
            # conversion terminated
            progress.color = ft.Colors.GREEN
            progress_text.value = "Text converted succesffully!"
            progress_text.color = ft.Colors.GREEN
            progress.update()
            progress_text.update()
            
            time.sleep(1) # pause for 1s
            
            audio_player = flet_audio.Audio(src=audio_res.audio_file, autoplay=True)
            self.audio_container.controls.clear()
            self.audio_container.controls.append(audio_player)
            self.page.overlay.append(audio_player)
            
            # hide progress_display
            self.progress_display.visible = False
            self.progress_display.update()
            
            # saving the file
            if self.should_save_audio.value:
                # save the audio file
                saved, msg, file_path = tts.save_file(audio_url=audio_res.audio_file)
                if saved:
                    self.page.open(ft.AlertDialog(title=ft.Text("Success"), content=ft.Text(f"Audio file saved as: '{file_path}'", color=ft.Colors.GREEN)))
                else:
                    self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"Unable to save the audio file: {msg}", color=ft.Colors.RED)))
                    # self.download_audio(tts=tts, audio_url=audio_res.audio_file)
            
            # whole page update
            self.page.update()
        
        except Exception as e:
            logging.error(f"Error converting text to audio: {e}")
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"Error converting text to audio: {e}")))
        
        self.page.update()
