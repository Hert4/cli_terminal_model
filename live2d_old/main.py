import os
import pygame
import live2d.v3 as live2d
import soundfile as sf
import sounddevice as sd
import numpy as np
import threading
import time

from live2d.v3 import StandardParams


# Load toàn bộ audio buffer
audio_path = "C:\\Users\\ADMIN\\OneDrive\\Máy tính\\cli\\static\\sound\\talk.wav"
data, samplerate = sf.read(audio_path)

# Chuyển stereo -> mono nếu cần
if len(data.shape) > 1:
    data = np.mean(data, axis=1)

# Số frame trên mỗi lần cập nhật miệng (~60fps)
frames_per_update = int(samplerate / 60)

# Tạo danh sách volume per frame
volume_frames = []
for i in range(0, len(data), frames_per_update):
    chunk = data[i : i + frames_per_update]
    rms = np.sqrt(np.mean(chunk**2))
    volume_frames.append(
        min(rms * 10, 1.0)
    )  # Nhân để scale phù hợp với ParamMouthOpenY


def main():
    pygame.init()
    live2d.init()

    display = (300, 400)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Live2D Voice Sync")

    live2d.glInit()

    model = live2d.LAppModel()

    model_path = "C:\\Users\\ADMIN\\OneDrive\\Máy tính\\cli\\static\\Firefly\\Firefly.model3.json"
    model.LoadModelJson(model_path)

    model.Resize(*display)
    model.SetAutoBlinkEnable(True)

    # Phát âm thanh
    threading.Thread(target=lambda: sd.play(data, samplerate), daemon=True).start()

    clock = pygame.time.Clock()
    running = True
    frame_idx = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                model.Drag(*pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                model.StartRandomMotion()

        live2d.clearBuffer()

        if frame_idx < len(volume_frames):
            model.SetParameterValue(
                StandardParams.ParamMouthOpenY, volume_frames[frame_idx]
            )
            frame_idx += 1

        model.Update()
        model.Draw()
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    live2d.dispose()
    pygame.quit()


if __name__ == "__main__":
    main()
