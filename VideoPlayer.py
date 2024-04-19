import os
import tkinter as tk
from tkinter import filedialog, ttk
import vlc

class VideoPlayer(tk.Tk):
    vlc_instance = vlc.Instance()

    def __init__(self,video_path=None):
        super().__init__()
        self.title("VLC Video Player")
        self.geometry("600x900")

        self.vlc_instance=vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        self.setup_ui()
        if video_path:
            self.setup_video(video_path)
        

    def play_video(self):
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()

    def rewind_video(self):
        time = self.player.get_time()
        if time > 10000:  # Check to avoid negative set_time
            self.player.set_time(time - 10000)  # Rewind by 10 seconds
            
        else:
            self.player.set_time(0)
        self.setup_slider()

    def setup_slider(self):
        self.after(1000, self.update_duration)  # Delay to ensure media is loaded

    def update_duration(self):
        duration = self.player.get_length() // 1000
        if duration > 0:
            self.slider.config(to=duration)
            self.update_slider()  # Start updating the slider after setting the duration
        else:
            self.after(1000, self.update_duration)  # Retry after delay if duration not ready

    def update_slider(self):
        if not self.slider.is_dragging:
            current_time = self.player.get_time() // 1000
            self.time_var.set(f"Time: {current_time} sec")
            self.slider.set(min(current_time, self.slider.cget('to')))
        self.after(500, self.update_slider)  # Schedule next update

    def on_slider_click(self,event):
        self.slider.is_dragging = True

    def on_slider_release(self,event):
        self.slider.is_dragging = False
        new_time = int(self.slider.get()) * 1000
        if self.player.get_media():
            self.player.set_time(min(new_time, self.player.get_length()))
            self.player.play()  # Resume after releasing the slider

    def setup_video(self,filepath):
        media = self.vlc_instance.media_new(filepath)
        self.player.set_media(media)
        self.player.play()
        self.setup_slider()
    
    def setup_ui(self):

        # Create a frame for the video player
        self.frame = tk.Frame(self, bg='black')
        self.frame.pack(fill='both', expand=True)
        self.player.set_hwnd(self.frame.winfo_id())

        # Time display
        self.time_var = tk.StringVar(value="Time: 0 sec")
        self.time_label = tk.Label(self, textvariable=self.time_var)
        self.time_label.pack(side='top', fill='x')
  

        # Slider for video progress
        self.slider = ttk.Scale(self, from_=0, to=1, orient='horizontal')
        self.slider.is_dragging = False
        self.slider.bind("<ButtonPress-1>", self.on_slider_click)
        self.slider.bind("<ButtonRelease-1>", self.on_slider_release)
        self.slider.pack(side='top', fill='x')

        self.setup_buttons()

    def setup_buttons(self):
        # Buttons for video control
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side='bottom', fill='x')


        btn_play = tk.Button(self.control_frame, text="Play", command=self.play_video)
        btn_play.pack(side='left', fill='x', expand=True)

        btn_pause = tk.Button(self.control_frame, text="Pause", command=self.pause_video)
        btn_pause.pack(side='left', fill='x', expand=True)

        btn_stop = tk.Button(self.control_frame, text="Stop", command=self.stop_video)
        btn_stop.pack(side='left', fill='x', expand=True)

        btn_rewind = tk.Button(self.control_frame, text="Rewind 10s", command=self.rewind_video)
        btn_rewind.pack(side='left', fill='x', expand=True)



#to test video file 
if __name__=="__main__":
    video_path="C:/Users/thefu/Downloads/new proj file/COSC-4P02-Group-Assignment-main (6)/COSC-4P02-Group-Assignment-main/videos/lighthearted/lig3.mp4"
    app=VideoPlayer(video_path)
    app.mainloop()


