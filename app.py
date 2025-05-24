import sys
import subprocess
import threading
import time
import os
import streamlit.components.v1 as components
import gdown

# Install dependencies
try:
    import streamlit as st
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

def run_ffmpeg(video_path, stream_key, is_shorts, log_callback):
    output_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
    scale = "-vf scale=720:1280" if is_shorts else ""
    cmd = [
        "ffmpeg", "-re", "-stream_loop", "-1", "-i", video_path,
        "-c:v", "libx264", "-preset", "veryfast", "-b:v", "2500k",
        "-maxrate", "2500k", "-bufsize", "5000k",
        "-g", "60", "-keyint_min", "60",
        "-c:a", "aac", "-b:a", "128k",
        "-f", "flv"
    ]
    if scale:
        cmd += scale.split()
    cmd.append(output_url)
    log_callback(f"Menjalankan: {' '.join(cmd)}")
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            log_callback(line.strip())
        process.wait()
    except Exception as e:
        log_callback(f"Error: {e}")
    finally:
        log_callback("Streaming selesai atau dihentikan.")


def download_from_drive(drive_url, output_filename="drive_video.mp4"):
    try:
        file_id = None
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[-1].split("&")[0]
        elif "file/d/" in drive_url:
            file_id = drive_url.split("file/d/")[1].split("/")[0]
        if file_id:
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output_filename, quiet=False)
            return output_filename
        else:
            return None
    except Exception as e:
        st.error(f"Gagal mengunduh dari Google Drive: {e}")
        return None


def main():
    st.title("YouTube Live Streamer dari File Lokal / Google Drive")

    st.write("### Pilih video dari lokal:")
    video_files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.flv'))]
    selected_video = st.selectbox("Pilih video", video_files) if video_files else None

    uploaded_file = st.file_uploader("Atau upload video baru (mp4/flv)", type=['mp4', 'flv'])

    st.write("### Atau masukkan link Google Drive (public share):")
    drive_url = st.text_input("Google Drive Link")

    video_path = None
    if uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        st.success("Video berhasil diupload!")
        video_path = uploaded_file.name
    elif selected_video:
        video_path = selected_video
    elif drive_url:
        st.info("Mengunduh dari Google Drive...")
        video_path = download_from_drive(drive_url)
        if video_path:
            st.success(f"Video berhasil diunduh: {video_path}")
        else:
            st.error("Gagal mengunduh video dari Google Drive!")

    stream_key = st.text_input("Stream Key", type="password")
    is_shorts = st.checkbox("Mode Shorts (720x1280)")

    log_placeholder = st.empty()
    logs = []
    streaming = st.session_state.get('streaming', False)

    def log_callback(msg):
        logs.append(msg)
        try:
            log_placeholder.text("\n".join(logs[-20:]))
        except:
            print(msg)

    if 'ffmpeg_thread' not in st.session_state:
        st.session_state['ffmpeg_thread'] = None

    if st.button("Jalankan Streaming"):
        if not video_path or not stream_key:
            st.error("Video dan stream key harus diisi!")
        else:
            st.session_state['streaming'] = True
            st.session_state['ffmpeg_thread'] = threading.Thread(
                target=run_ffmpeg, args=(video_path, stream_key, is_shorts, log_callback), daemon=True)
            st.session_state['ffmpeg_thread'].start()
            st.success("Streaming dimulai!")

    if st.button("Stop Streaming"):
        st.session_state['streaming'] = False
        os.system("pkill ffmpeg")
        st.warning("Streaming dihentikan!")

    log_placeholder.text("\n".join(logs[-20:]))


if __name__ == '__main__':
    main()
