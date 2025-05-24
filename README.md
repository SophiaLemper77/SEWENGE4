# YouTube RTMP Live Streaming App for Streamlit

This application allows you to stream directly to YouTube using RTMP protocol. It provides a user-friendly interface to configure your stream settings, monitor metrics, and manage your live stream.

## Features

- YouTube RTMP stream configuration with stream key and URL inputs
- Video input selection (webcam, screen capture, or video file)
- Stream quality and resolution settings
- Stream control panel (start, stop, monitoring)
- Stream status monitoring with key metrics
- Secure credential handling with masked inputs
- Custom stream title, description, and privacy settings
- Real-time video preview of the stream content

## Requirements

- Python 3.7+
- FFmpeg installed on your system
- YouTube account with live streaming enabled
- Streamlit
- OpenCV
- Other dependencies listed in requirements.txt

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Make sure FFmpeg is installed on your system:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - macOS: Install using Homebrew with `brew install ffmpeg`
   - Linux: Install using your package manager, e.g., `apt-get install ffmpeg`

## Usage

1. Run the Streamlit app:

```
streamlit run app.py
```

2. Access the URL provided by Streamlit (typically http://localhost:8501)
3. Configure your stream settings:
   - Enter your YouTube RTMP URL and Stream Key
   - Set your desired resolution and bitrate
   - Choose your video source (webcam, screen, or file upload)
4. Click "Start Streaming" to go live on YouTube

## Stream Configuration

- **RTMP URL**: Usually `rtmp://a.rtmp.youtube.com/live2` for YouTube
- **Stream Key**: Your private YouTube stream key (keep this secret!)
- **Resolution**: 360p, 480p, 720p, or 1080p
- **Video Bitrate**: Ranges from 1000 to 5000 kbps
- **Audio Bitrate**: Ranges from 64 to 192 kbps

## Security Notes

- Your Stream Key is sensitive information. The app masks this input and never stores it permanently.
- Always test your connection before going live
- Be mindful of YouTube's community guidelines and copyright policies

## Troubleshooting

- **Stream fails to start**: Ensure FFmpeg is properly installed and accessible in your PATH
- **No video from webcam**: Check that your webcam is not being used by another application
- **Poor stream quality**: Try lowering the resolution or bitrate, or check your internet connection
- **Audio issues**: Ensure your microphone is properly connected and selected as the default input device

## License

This project is licensed under the MIT License - see the LICENSE file for details.