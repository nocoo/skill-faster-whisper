---
name: faster-whisper
description: Fast speech-to-text transcription using faster-whisper with CTranslate2. Supports 99 languages, multiple output formats, GPU acceleration, and VAD filtering. Zero configuration required.
---

# Faster Whisper Transcription Skill

**Fast speech-to-text** powered by faster-whisper (CTranslate2 implementation of OpenAI Whisper).

**Zero configuration** - run.py handles everything automatically!

## When to Use This Skill

Trigger when user:
- Wants to transcribe audio/video files to text
- Mentions "transcribe", "speech to text", "convert audio to text"
- Has audio files (MP3, WAV, MP4, M4A, etc.) needing transcription
- Needs subtitles/captions for videos
- Wants to extract speech from recordings
- Asks about "whisper", "speech recognition", "audio transcription"
- Needs timestamps in transcription output
- Wants to transcribe specific languages (Chinese, English, etc.)

## Core Capabilities

| Feature | Description |
|---------|-------------|
| **🚀 Fast** | Up to 4x faster than openai/whisper with same accuracy |
| **🌏 Multi-language** | 99 languages with auto-detection |
| **💾 Memory Efficient** | INT8 quantization for CPU/GPU |
| **📝 Timestamps** | Segment and word-level timestamps |
| **🎯 VAD Filter** | Remove silence automatically |
| **📄 Output Formats** | Text, SRT subtitles, JSON |
| **⚙️ Zero Config** | Automatic venv and dependency management |

## Model Selection

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| `tiny` | 39MB | ⚡⚡⚡ Fastest | Basic | Quick drafts |
| `base` | 74MB | ⚡⚡ Fast | Good | Everyday use |
| `small` | 244MB | ⚡ Medium | Very Good | Balance |
| `medium` | 769MB | ⚡ Slow | Excellent | High quality |
| `large-v3` | 1550MB | 🐢 Slowest | ★ Best | Final output |
| `distil-large-v3` | 1550MB | ⚡ Fast | Near-Best | Speed + quality |

## Critical: Always Use run.py

**NEVER call scripts directly. ALWAYS use `python scripts/run.py`:**

```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py transcribe.py audio.mp3
python scripts/run.py transcribe.py audio.mp3 --language zh

# ❌ WRONG - Never call directly:
python scripts/transcribe.py audio.mp3  # Fails without venv!
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed (first run only)
2. Installs faster-whisper automatically
3. Activates environment
4. Executes script properly

## Quick Reference

```bash
# Basic transcription (auto-detect language)
python scripts/run.py transcribe.py audio.mp3

# Specify language
python scripts/run.py transcribe.py audio.mp3 --language zh
python scripts/run.py transcribe.py audio.mp3 --language en

# Save to file
python scripts/run.py transcribe.py audio.mp3 --output transcript.txt

# Generate SRT subtitles
python scripts/run.py transcribe.py video.mp4 --format srt --output video.srt

# Use smaller model (faster)
python scripts/run.py transcribe.py audio.mp3 --model small

# Faster with beam size 1
python scripts/run.py transcribe.py audio.mp3 --beam-size 1

# Include word timestamps
python scripts/run.py transcribe.py audio.mp3 --word-timestamps
```

## Core Workflow

### Step 1: Run Transcription (That's It!)

```bash
# From any directory, just run:
python ~/.claude/skills/skill-faster-whisper/scripts/run.py transcribe.py /path/to/audio.mp3

# Or if you're in the skill directory:
python scripts/run.py transcribe.py audio.mp3

# First run? No problem! It automatically:
# - Creates virtual environment
# - Installs dependencies
# - Downloads model (first time only)
# - Transcribes your audio
```

### Common Use Cases

```bash
# Transcribe Chinese audio
python scripts/run.py transcribe.py recording.mp3 --language zh

# Generate video subtitles
python scripts/run.py transcribe.py video.mp4 --format srt --output video.srt

# Fast draft (small model, beam=1)
python scripts/run.py transcribe.py meeting.mp3 --model small --beam-size 1

# High quality final output
python scripts/run.py transcribe.py interview.mp3 --model large-v3 --language zh

# Remove silence with VAD
python scripts/run.py transcribe.py recording.mp3 --vad-filter

# Save to file
python scripts/run.py transcribe.py audio.mp3 --output transcript.txt
```

## Command Reference

```bash
python scripts/run.py transcribe.py AUDIO_FILE [OPTIONS]

positional arguments:
  AUDIO_FILE             Path to audio file to transcribe

options:
  --model MODEL         Model size: tiny, base, small, medium, large-v3, distil-large-v3
  --device DEVICE       Device: cpu or cuda
  --compute-type TYPE   float16, int8, int8_float16
  --language LANG       Language code (en, zh, ja, etc.) or auto
  --beam-size N         Beam size for decoding (1=faster, 5=accurate)
  --output PATH         Save output to file
  --format FMT          Output format: text, srt, json, json_full
  --vad-filter          Enable voice activity detection (remove silence)
  --word-timestamps     Include word-level timestamps
  --verbose, -v         Show detailed progress
```

## Language Codes

Common languages:
- `en` - English
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `es` - Spanish
- `fr` - French
- `de` - German
- `auto` - Auto-detect (default)

## Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `text` | Plain text with timestamps | Reading, documentation |
| `srt` | SubRip subtitle format | Video captions |
| `json` | Structured data | Programmatic processing |
| `json_full` | With word timestamps | Detailed analysis |

## Configuration (Optional)

Create `scripts/config.json` for defaults:

```json
{
  "model_size": "large-v3",
  "device": "cpu",
  "compute_type": "int8",
  "language": null,
  "task": "transcribe",
  "beam_size": 5,
  "vad_filter": true,
  "vad_parameters": {
    "min_silence_duration_ms": 500
  },
  "word_timestamps": false
}
```

## GPU Acceleration (NVIDIA)

If you have NVIDIA GPU:

```bash
# CUDA with FP16 (fastest)
python scripts/run.py transcribe.py audio.mp3 --device cuda --compute-type float16

# Memory-efficient GPU
python scripts/run.py transcribe.py audio.mp3 --device cuda --compute-type int8_float16
```

## Performance Tips

### For Speed
- Use smaller model: `--model small` or `--model base`
- Reduce beam size: `--beam-size 1`
- Disable VAD: remove `--vad-filter`

### For Accuracy
- Use larger model: `--model large-v3`
- Specify language: `--language zh`
- Increase beam size: `--beam-size 5` (default)

### For Memory (CPU)
- Use INT8: `--compute-type int8` (default)
- Use smaller model
- Reduce beam size

### For Memory (GPU)
- Use `--compute-type int8_float16`
- Use smaller model with CUDA

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Always use `run.py` wrapper |
| Out of memory on CPU | Use `--model small` |
| Slow transcription | Use `--model small`, `--beam-size 1` |
| Poor accuracy | Specify `--language`, use `--model large-v3` |
| Wrong language detected | Use `--language zh` |
| Long silences in output | Enable `--vad-filter` |

## Output Examples

### Text Format
```
# Transcription
# Language: zh (confidence: 98.50%)
# Duration: 125.3 seconds

[0.00s -> 2.50s] 你好
[2.50s -> 5.00s] 我是第一次见到你
```

### SRT Format
```
1
00:00:00,000 --> 00:00:02,500
你好

2
00:00:02,500 --> 00:00:05,000
我是第一次见到你
```

### JSON Format
```json
{
  "language": "zh",
  "language_probability": 0.985,
  "duration": 125.3,
  "segments": [
    {"start": 0.0, "end": 2.5, "text": "你好"}
  ]
}
```

## Best Practices

1. **Always use run.py** - Handles environment automatically
2. **Specify language** for better accuracy: `--language zh`
3. **Use small model** for drafts, `large-v3` for final
4. **Enable VAD** for recordings with long silences
5. **Save output** with `--output` to avoid losing results

## Environment Management

The virtual environment is automatically managed:
- First run creates `.venv` automatically
- Dependencies install automatically
- Everything isolated in skill directory
- No manual setup required

## Technical Details

- **Audio decoding**: PyAV (no FFmpeg required)
- **Model engine**: CTranslate2 for efficient inference
- **Supported formats**: MP3, WAV, M4A, FLAC, OGG, MP4, etc.
- **Sample rate**: Auto-resampled to 16kHz
- **Channels**: Auto-converted to mono

## Resources

- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [OpenAI Whisper Paper](https://arxiv.org/abs/2212.04356)
- [CTranslate2 Documentation](https://opennmt.net/CTranslate2/)
