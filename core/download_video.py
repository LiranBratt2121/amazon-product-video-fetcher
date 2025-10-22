import ffmpeg

def download_video(m3u8_url: str, output_file: str = "output.mp4"):
    output_file = output_file if output_file.endswith(".mp4") else output_file + ".mp4"
    
    (
        ffmpeg
        .input(m3u8_url)
        .output(output_file, c='copy')
        .run(overwrite_output=True)
    )
    print(f"Video saved to {output_file}")


