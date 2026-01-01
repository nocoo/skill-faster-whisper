# 🎤 Claude Code Skill - Faster Whisper

> Fast speech-to-text transcription powered by faster-whisper with CTranslate2. Supports 99 languages, multiple output formats, GPU acceleration, and VAD filtering. Zero configuration required.

[![Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.com/claude-code)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

**[简体中文](./README.zh-CN.md) | English**

---

## 📋 Prerequisites

- **Python 3.9+**
- **Virtual environment** (recommended)

## 🚀 Installation

### Step 1: Clone or Download

```bash
git clone https://github.com/nocoo/skill-fast-whisper.git
cd skill-fast-whisper
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install faster-whisper
pip install faster-whisper
```

### Step 3: Configure (Optional)

```bash
cp scripts/config.example.json scripts/config.json
# Edit scripts/config.json to set your preferred defaults
```

## ⚡ Quick Start

```bash
# Basic transcription (auto-detect language)
python scripts/transcribe.py audio.mp3

# With output file
python scripts/transcribe.py audio.mp3 --output transcript.txt

# Generate subtitles
python scripts/transcribe.py video.mp4 --format srt --output video.srt
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🚀 Fast** | Up to 4x faster than openai/whisper |
| **💾 Efficient** | INT8 quantization for low memory usage |
| **🌏 Multi-language** | 99 languages with auto-detection |
| **📝 Timestamps** | Segment and word-level timestamps |
| **🎯 VAD Filter** | Remove silence automatically |
| **📄 Formats** | Text, SRT, JSON output |
| **🎮 GPU Support** | NVIDIA CUDA acceleration |

## 📊 Model Comparison

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 39MB | ⚡⚡⚡ | Basic |
| base | 74MB | ⚡⚡ | Good |
| small | 244MB | ⚡ | Very Good |
| medium | 769MB | ⚡ | Excellent |
| **large-v3** | 1550MB | Best | ★ Best |

## 📖 Usage Examples

```bash
# Basic transcription (auto-detect language)
python scripts/transcribe.py audio.mp3

# Specify language
python scripts/transcribe.py audio.mp3 --language zh

# Save to file
python scripts/transcribe.py audio.mp3 --output transcript.txt

# Generate subtitles
python scripts/transcribe.py video.mp4 --format srt --output video.srt

# Use smaller model (faster)
python scripts/transcribe.py audio.mp3 --model small

# GPU acceleration (NVIDIA)
python scripts/transcribe.py audio.mp3 --device cuda --compute-type float16
```

## ⚙️ Configuration

Copy the example config:

```bash
cp scripts/config.example.json scripts/config.json
```

Edit `scripts/config.json` to set defaults:

```json
{
  "model_size": "large-v3",
  "device": "cpu",
  "compute_type": "int8",
  "language": null,
  "beam_size": 5,
  "vad_filter": true,
  "word_timestamps": false
}
```

## 🎛️ Command-Line Options

```
positional arguments:
  audio_file            Path to audio file

options:
  -h, --help            Show help
  --model MODEL         Model size (default: large-v3)
  --device DEVICE       cpu or cuda (default: cpu)
  --compute-type TYPE   float16, int8, int8_float16 (default: int8)
  --language LANG       Language code or auto (default: auto)
  --task TASK           transcribe or translate (default: transcribe)
  --beam-size N         Beam size (default: 5)
  --vad-filter          Enable VAD filter
  --word-timestamps     Include word timestamps
  --output PATH         Save to file
  --format FMT          text, srt, json, json_full (default: text)
  --verbose             Show detailed progress
```

## 📁 Project Structure

```
skill-fast-whisper/
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md               # This file (English)
├── README.zh-CN.md         # Chinese version
├── SKILL.md                # Skill definition (used by Claude)
├── requirements.txt        # Python dependencies
├── scripts/
│   ├── config.example.json # Configuration template
│   ├── config.json         # Your configuration (not in git)
│   └── transcribe.py       # Core transcription script
└── venv/                   # Virtual environment (not in git)
```

## 📄 Output Formats

### Text (default)
```
[0.00s -> 2.50s] Hello world
[2.50s -> 5.00s] This is a test
```

### SRT (subtitles)
```
1
00:00:00,000 --> 00:00:02,500
Hello world

2
00:00:02,500 --> 00:00:05,000
This is a test
```

### JSON
```json
{
  "language": "en",
  "language_probability": 0.95,
  "duration": 5.0,
  "segments": [...]
}
```

## ⚡ Performance Tips

### For CPU (most users)
- Use `int8` compute type (default)
- Try `small` model for faster results
- Reduce `beam_size` to 1 for speed

### For GPU (NVIDIA)
- Use `--device cuda`
- Use `float16` compute type
- Models process 3-5x faster

## ❓ Troubleshooting

### "faster-whisper not installed"
```bash
pip install faster-whisper
```

### "Out of memory"
- Use smaller model: `--model small`
- Use int8: `--compute-type int8`

### Slow transcription
- Use smaller model
- Reduce beam size: `--beam-size 1`
- Consider GPU if available

### Poor accuracy
- Specify correct language: `--language zh`
- Use larger model: `--model large-v3`
- Check audio quality (16kHz+ recommended)

## 🔧 Technical Details

- **Model**: Based on OpenAI Whisper
- **Engine**: CTranslate2 for efficient inference
- **Audio**: PyAV decodes MP3/WAV/MP4/etc. (no FFmpeg needed)
- **Languages**: 99 languages supported

## 🔢 Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_size` | string | `"large-v3"` | Model size: tiny/base/small/medium/large-v3 |
| `device` | string | `"cpu"` | Device: cpu or cuda |
| `compute_type` | string | `"int8"` | Computation: float16/int8/int8_float16 |
| `language` | string/null | `null` | Language code (null = auto-detect) |
| `beam_size` | int | `5` | Beam search size (1 = greedy) |
| `vad_filter` | boolean | `true` | Enable voice activity detection |
| `word_timestamps` | boolean | `false` | Include word-level timestamps |

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) by SYSTRAN
- [OpenAI Whisper](https://github.com/openai/whisper)
- [CTranslate2](https://github.com/OpenNMT/CTranslate2)
- [Claude Code](https://claude.com/claude-code) - AI programming assistant

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Author

Created by [@nocoo](https://github.com/nocoo)

## 📞 Support

For issues with:
- **This skill**: Check [SKILL.md](SKILL.md)
- **faster-whisper**: Visit [GitHub](https://github.com/SYSTRAN/faster-whisper)
- **Claude Code**: Visit [GitHub](https://github.com/anthropics/claude-code)

---

**[简体中文](./README.zh-CN.md) | English**
