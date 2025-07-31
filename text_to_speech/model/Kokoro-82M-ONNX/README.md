---
license: apache-2.0
library_name: transformers.js
language:
- en
base_model:
- hexgrad/Kokoro-82M
pipeline_tag: text-to-speech
new_version: onnx-community/Kokoro-82M-v1.0-ONNX
---

# Kokoro TTS

Kokoro is a frontier TTS model for its size of 82 million parameters (text in/audio out).

## Table of contents

- [Samples](#samples)
- [Usage](#usage)
  - [JavaScript](#javascript)
  - [Python](#python)
- [Quantizations](#quantizations)

## Samples


> Life is like a box of chocolates. You never know what you're gonna get.


| Voice                    | Nationality | Gender | Sample                                                                                                                                  |
|--------------------------|-------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Default (`af`)           | American    | Female | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/C0_ZUcNSAxvMwpS8QbnKv.wav"></audio> |
| Bella (`af_bella`)       | American    | Female | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/B_q15Z_FXdgBP9-Hk9oKq.wav"></audio> |
| Nicole (`af_nicole`)     | American    | Female | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/sS8U5lQHkhgX7rwTmy-5w.wav"></audio> |
| Sarah (`af_sarah`)       | American    | Female | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/SokkBiqEqwxLLx_pqvf1p.wav"></audio> |
| Sky (`af_sky`)           | American    | Female | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/IzySGHUtl5mYeFxx1oaRf.wav"></audio> |
| Adam (`am_adam`)         | American    | Male   | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/9n6myE6--ZsEuF5xDv5eC.wav"></audio> |
| Michael (`am_michael`)   | American    | Male   | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/EPFciGtTU1YUXu8MAw7DX.wav"></audio> |
| Emma (`bf_emma`)         | British     | Female | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/AGEsXs-gyJq3dsyo7PjHo.wav"></audio> |
| Isabella (`bf_isabella`) | British     | Female | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/JEzrrXYJSDcmlEzI7tE0c.wav"></audio> |
| George (`bm_george`)     | British     | Male   | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/nsv4zKB4MX2TvXRxv504k.wav"></audio> |
| Lewis (`bm_lewis`)       | British     | Male   | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/g_mcBl2xTbQl0sbrpZt48.wav"></audio> |


## Usage

### JavaScript

First, install the `kokoro-js` library from [NPM](https://npmjs.com/package/kokoro-js) using:
```bash
npm i kokoro-js
```

You can then generate speech as follows:

```js
import { KokoroTTS } from "kokoro-js";

const model_id = "onnx-community/Kokoro-82M-ONNX";
const tts = await KokoroTTS.from_pretrained(model_id, {
  dtype: "q8", // Options: "fp32", "fp16", "q8", "q4", "q4f16"
});

const text = "Life is like a box of chocolates. You never know what you're gonna get.";
const audio = await tts.generate(text, {
  // Use `tts.list_voices()` to list all available voices
  voice: "af_bella",
});
audio.save("audio.wav");
```


### Python

```python
import os
import numpy as np
from onnxruntime import InferenceSession

# Tokens produced by phonemize() and tokenize() in kokoro.py
tokens = [50, 157, 43, 135, 16, 53, 135, 46, 16, 43, 102, 16, 56, 156, 57, 135, 6, 16, 102, 62, 61, 16, 70, 56, 16, 138, 56, 156, 72, 56, 61, 85, 123, 83, 44, 83, 54, 16, 53, 65, 156, 86, 61, 62, 131, 83, 56, 4, 16, 54, 156, 43, 102, 53, 16, 156, 72, 61, 53, 102, 112, 16, 70, 56, 16, 138, 56, 44, 156, 76, 158, 123, 56, 16, 62, 131, 156, 43, 102, 54, 46, 16, 102, 48, 16, 81, 47, 102, 54, 16, 54, 156, 51, 158, 46, 16, 70, 16, 92, 156, 135, 46, 16, 54, 156, 43, 102, 48, 4, 16, 81, 47, 102, 16, 50, 156, 72, 64, 83, 56, 62, 16, 156, 51, 158, 64, 83, 56, 16, 44, 157, 102, 56, 16, 44, 156, 76, 158, 123, 56, 4]

# Context length is 512, but leave room for the pad token 0 at the start & end
assert len(tokens) <= 510, len(tokens)

# Style vector based on len(tokens), ref_s has shape (1, 256)
voices = np.fromfile('./voices/af.bin', dtype=np.float32).reshape(-1, 1, 256)
ref_s = voices[len(tokens)]

# Add the pad ids, and reshape tokens, should now have shape (1, <=512)
tokens = [[0, *tokens, 0]]

model_name = 'model.onnx' # Options: model.onnx, model_fp16.onnx, model_quantized.onnx, model_q8f16.onnx, model_uint8.onnx, model_uint8f16.onnx, model_q4.onnx, model_q4f16.onnx
sess = InferenceSession(os.path.join('onnx', model_name))

audio = sess.run(None, dict(
    input_ids=tokens,
    style=ref_s,
    speed=np.ones(1, dtype=np.float32),
))[0]
```

Optionally, save the audio to a file:
```py
import scipy.io.wavfile as wavfile
wavfile.write('audio.wav', 24000, audio[0])
```

## Quantizations

The model is resilient to quantization, enabling efficient high-quality speech synthesis at a fraction of the original model size. 

> How could I know? It's an unanswerable question. Like asking an unborn child if they'll lead a good life. They haven't even been born.


| Model                                          | Size (MB) | Sample                                                                                                                                  |
|------------------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------|
| model.onnx (fp32)                              | 326       | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/njexBuqPzfYUvWgs9eQ-_.wav"></audio> |
| model_fp16.onnx (fp16)                         | 163       | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/8Ebl44hMQonZs4MlykExt.wav"></audio> |
| model_quantized.onnx (8-bit)                   | 92.4      | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/9SLOt6ETclZ4yRdlJ0VIj.wav"></audio> |
| model_q8f16.onnx (Mixed precision)             | 86        | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/gNDMqb33YEmYMbAIv_Grx.wav"></audio> |
| model_uint8.onnx (8-bit & mixed precision)     | 177       | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/tpOWRHIWwEb0PJX46dCWQ.wav"></audio> |
| model_uint8f16.onnx (Mixed precision)          | 114       | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/vtZhABzjP0pvGD7dRb5Vr.wav"></audio> |
| model_q4.onnx (4-bit matmul)                   | 305       | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/8FVn0IJIUfccEBWq8Fnw_.wav"></audio> |
| model_q4f16.onnx (4-bit matmul & fp16 weights) | 154       | <audio controls src="https://cdn-uploads.huggingface.co/production/uploads/61b253b7ac5ecaae3d1efe0c/7DrgWC_1q00s-wUJuG44X.wav"></audio> |