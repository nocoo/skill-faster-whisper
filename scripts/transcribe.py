#!/usr/bin/env python3
"""
Faster Whisper Transcription Script

A command-line tool for speech-to-text transcription using faster-whisper.
Supports multiple output formats, languages, and GPU acceleration.
"""

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from faster_whisper import WhisperModel
    from tqdm import tqdm
except ImportError:
    print("Error: faster-whisper not installed.")
    print("Run: pip install faster-whisper")
    sys.exit(1)


@dataclass
class TranscriptionConfig:
    """Configuration for transcription."""
    model_size: str = "large-v3"
    device: str = "cpu"
    compute_type: str = "int8"
    language: Optional[str] = None
    task: str = "transcribe"
    beam_size: int = 5
    vad_filter: bool = False
    vad_parameters: Optional[dict] = None
    word_timestamps: bool = False

    @classmethod
    def from_file(cls, config_path: str) -> "TranscriptionConfig":
        """Load configuration from JSON file."""
        if not os.path.exists(config_path):
            return cls()

        with open(config_path, "r") as f:
            data = json.load(f)

        # Map config keys to dataclass fields
        return cls(
            model_size=data.get("model_size", "large-v3"),
            device=data.get("device", "cpu"),
            compute_type=data.get("compute_type", "int8"),
            language=data.get("language"),
            task=data.get("task", "transcribe"),
            beam_size=data.get("beam_size", 5),
            vad_filter=data.get("vad_filter", False),
            vad_parameters=data.get("vad_parameters"),
            word_timestamps=data.get("word_timestamps", False),
        )


@dataclass
class Segment:
    """A transcribed segment with timing info."""
    start: float
    end: float
    text: str
    words: Optional[list] = None


@dataclass
class TranscriptionResult:
    """Complete transcription result with metadata."""
    language: str
    language_probability: float
    duration: float
    segments: list[Segment]


def format_timestamp(seconds: float) -> str:
    """Format timestamp as HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def format_timestamp_srt(seconds: float) -> str:
    """Format timestamp as SRT format HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def transcribe(
    audio_path: str,
    config: TranscriptionConfig,
    verbose: bool = False
) -> TranscriptionResult:
    """
    Transcribe audio file using faster-whisper.

    Args:
        audio_path: Path to audio file
        config: Transcription configuration
        verbose: Show detailed progress

    Returns:
        TranscriptionResult with segments and metadata
    """
    if verbose:
        print(f"Loading model: {config.model_size}")
        print(f"Device: {config.device}, Compute: {config.compute_type}")

    # Load model
    model = WhisperModel(
        config.model_size,
        device=config.device,
        compute_type=config.compute_type,
    )

    # Set up VAD parameters
    vad_params = config.vad_parameters if config.vad_filter else None

    # Prepare language parameter
    lang = None if config.language == "auto" else config.language

    if verbose:
        print(f"Transcribing: {audio_path}")
        if lang:
            print(f"Language: {lang}")
        else:
            print("Language: auto-detect")

    # Transcribe
    segments_info = model.transcribe(
        audio_path,
        language=lang,
        task=config.task,
        beam_size=config.beam_size,
        vad_filter=config.vad_filter,
        vad_parameters=vad_params,
        word_timestamps=config.word_timestamps,
    )

    segments, info = segments_info

    # Convert to list
    segment_list = list(segments)

    # Build result
    result_segments = []
    for seg in segment_list:
        words = None
        if config.word_timestamps and hasattr(seg, 'words') and seg.words:
            words = [
                {"start": w.start, "end": w.end, "word": w.word, "probability": w.probability}
                for w in seg.words
            ]

        result_segments.append(Segment(
            start=seg.start,
            end=seg.end,
            text=seg.text.strip(),
            words=words,
        ))

    return TranscriptionResult(
        language=info.language,
        language_probability=info.language_probability,
        duration=info.duration,
        segments=result_segments,
    )


def format_text(result: TranscriptionResult) -> str:
    """Format as plain text with timestamps."""
    lines = [
        f"# Transcription",
        f"# Language: {result.language} (confidence: {result.language_probability:.2%})",
        f"# Duration: {result.duration:.1f} seconds",
        f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    for seg in result.segments:
        lines.append(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")

    return "\n".join(lines)


def format_srt(result: TranscriptionResult) -> str:
    """Format as SRT subtitles."""
    lines = []

    for i, seg in enumerate(result.segments, 1):
        lines.append(str(i))
        lines.append(f"{format_timestamp_srt(seg.start)} --> {format_timestamp_srt(seg.end)}")
        lines.append(seg.text)
        lines.append("")

    return "\n".join(lines)


def format_json(result: TranscriptionResult, full: bool = False) -> str:
    """Format as JSON."""
    data = {
        "language": result.language,
        "language_probability": result.language_probability,
        "duration": result.duration,
        "segments": [
            {
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
            }
            for seg in result.segments
        ],
    }

    if full:
        for i, seg in enumerate(result.segments):
            if seg.words:
                data["segments"][i]["words"] = seg.words

    return json.dumps(data, ensure_ascii=False, indent=2)


def save_output(content: str, output_path: str) -> None:
    """Save transcription to file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using faster-whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audio.mp3
  %(prog)s audio.mp3 --language zh
  %(prog)s audio.mp3 --output transcript.txt
  %(prog)s audio.mp3 --format srt --output video.srt
  %(prog)s audio.mp3 --model small --device cuda
        """,
    )

    parser.add_argument("audio_file", help="Path to the audio file to transcribe")

    parser.add_argument("--config", default="scripts/config.json",
                        help="Path to config file (default: scripts/config.json)")
    parser.add_argument("--model", default=None,
                        choices=["tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3", "distil-large-v3"],
                        help="Model size (overrides config)")
    parser.add_argument("--device", choices=["cpu", "cuda"], default=None,
                        help="Device: cpu or cuda (overrides config)")
    parser.add_argument("--compute-type", dest="compute_type",
                        choices=["float16", "int8", "int8_float16"], default=None,
                        help="Compute type (overrides config)")
    parser.add_argument("--language", default=None,
                        help="Language code (e.g., en, zh, ja) or 'auto' (overrides config)")
    parser.add_argument("--task", choices=["transcribe", "translate"], default=None,
                        help="Task: transcribe or translate to English")
    parser.add_argument("--beam-size", type=int, dest="beam_size", default=None,
                        help="Beam size for decoding (default: 5)")
    parser.add_argument("--vad-filter", action="store_true", default=None,
                        help="Enable VAD filter to remove silence")
    parser.add_argument("--word-timestamps", action="store_true", default=None,
                        help="Include word-level timestamps")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path")
    parser.add_argument("--format", "fmt", choices=["text", "srt", "json", "json_full"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed progress")

    args = parser.parse_args()

    # Check audio file exists
    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file not found: {args.audio_file}")
        sys.exit(1)

    # Load config
    config = TranscriptionConfig.from_file(args.config)

    # Override with command-line args
    if args.model:
        config.model_size = args.model
    if args.device:
        config.device = args.device
    if args.compute_type:
        config.compute_type = args.compute_type
    if args.language:
        config.language = args.language
    if args.task:
        config.task = args.task
    if args.beam_size is not None:
        config.beam_size = args.beam_size
    if args.vad_filter is not None:
        config.vad_filter = args.vad_filter
    if args.word_timestamps is not None:
        config.word_timestamps = args.word_timestamps

    # Transcribe
    try:
        result = transcribe(args.audio_file, config, verbose=args.verbose)
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)

    # Format output
    if args.format == "text":
        output = format_text(result)
    elif args.format == "srt":
        output = format_srt(result)
    elif args.format == "json":
        output = format_json(result, full=False)
    elif args.format == "json_full":
        output = format_json(result, full=True)
    else:
        output = format_text(result)

    # Output
    if args.output:
        save_output(output, args.output)
    else:
        print(output)


if __name__ == "__main__":
    main()
