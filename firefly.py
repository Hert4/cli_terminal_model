import os
import pygame
import live2d.v3 as live2d
from live2d.v3 import StandardParams
import numpy as np
import threading
import soundfile as sf
import sounddevice as sd
from text_to_speech.kokoro_client import KokoroTTS


class Live2DSpeaker:
    def __init__(
        self,
        tts_model_dir="C:\\Users\\ADMIN\\OneDrive\\Máy tính\\cli\\text_to_speech\\model\\Kokoro-82M-ONNX",
        model_path="C:\\Users\\ADMIN\\OneDrive\\Máy tính\\cli\\static\\Firefly\\Firefly.model3.json",
    ):
        self.tts_model_dir = tts_model_dir
        self.model_path = model_path
        self.model = None
        self.tts = None
        self.display_size = (300, 400)

    def load(self):
        # Khởi tạo TTS
        self.tts = KokoroTTS(model_dir=self.tts_model_dir)

        # Setup Live2D
        pygame.init()
        live2d.init()
        pygame.display.set_mode(self.display_size, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("Live2D Voice Sync")
        live2d.glInit()

        self.model = live2d.LAppModel()
        self.model.LoadModelJson(self.model_path)
        self.model.Resize(*self.display_size)
        self.model.SetAutoBlinkEnable(True)

    def _extract_volume_frames(self, audio, samplerate=24000):
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        frames_per_update = int(samplerate / 60)
        volume_frames = []

        for i in range(0, len(audio), frames_per_update):
            chunk = audio[i : i + frames_per_update]
            rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0
            volume_frames.append(min(rms * 10, 1.0))

        return volume_frames

    def speak(self, text):
        try:
            tokens, ref_s = self.tts.prepare_inputs(text)
            audio = self.tts.synthesize(tokens, ref_s)[0]
            volume_frames = self._extract_volume_frames(audio)

            # Phát audio song song
            threading.Thread(
                target=lambda: sd.play(audio, samplerate=24000), daemon=True
            ).start()

            clock = pygame.time.Clock()
            frame_idx = 0

            while frame_idx < len(volume_frames) or sd.get_stream().active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                volume = (
                    volume_frames[frame_idx] if frame_idx < len(volume_frames) else 0
                )
                self.model.SetParameterValue(StandardParams.ParamMouthOpenY, volume)
                frame_idx += 1

                live2d.clearBuffer()
                self.model.Update()
                self.model.Draw()
                pygame.display.flip()
                clock.tick(60)

        except Exception as e:
            print(f"Error in speak(): {str(e)}")


# live = Live2DSpeaker()

# live.load()

# live.speak("AAAAAAAA")
