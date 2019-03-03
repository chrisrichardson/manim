import numpy as np
from pydub import AudioSegment
import shutil
import subprocess
import os

from manimlib.constants import FFMPEG_BIN
from manimlib.constants import VIDEO_DIR
from manimlib.utils.config_ops import digest_config
from manimlib.utils.file_ops import guarantee_existence
from manimlib.utils.file_ops import add_extension_if_not_present
from manimlib.utils.file_ops import get_sorted_integer_files
from manimlib.utils.sounds import get_full_sound_file_path


class SceneFileWriter(object):
    CONFIG = {
        "write_to_movie": False,
        "movie_file_extension": ".mp4",
        "file_name": None,
        "output_directory": None,
    }

    def __init__(self, camera, **kwargs):
        digest_config(self, kwargs)

        pixel_height = camera.pixel_height
        frame_rate = camera.frame_rate

        movie_directory = "{}p{}".format(pixel_height, frame_rate)
        self.init_output_directories(movie_directory)

        self.init_audio()

    # Output directories and files
    def init_output_directories(self, movie_directory):

        if self.write_to_movie:
            movie_dir = guarantee_existence(os.path.join(
                VIDEO_DIR,
                self.output_directory,
                movie_directory,
            ))
            self.movie_file_path = os.path.join(
                movie_dir,
                add_extension_if_not_present(
                    self.file_name, self.movie_file_extension
                )
            )
            self.partial_movie_directory = guarantee_existence(os.path.join(
                movie_dir,
                self.get_partial_movie_directory(),
                self.file_name,
            ))

    def get_image_directory(self):
        return "images"

    def get_partial_movie_directory(self):
        return "partial_movie_files"

    # Directory getters
    def get_image_file_path(self):
        return self.image_file_path

    def get_next_partial_movie_path(self, n):
        result = os.path.join(
            self.partial_movie_directory,
            "{:05}{}".format(n, self.movie_file_extension))

        return result

    def get_movie_file_path(self):
        return self.movie_file_path

    # Sound
    def init_audio(self):
        self.includes_sound = False

    def create_audio_segment(self):
        self.audio_segment = AudioSegment.silent()

    def add_audio_segment(self, new_segment,
                          time=None,
                          gain_to_background=None):
        if not self.includes_sound:
            self.includes_sound = True
            self.create_audio_segment()
        segment = self.audio_segment
        curr_end = segment.duration_seconds
        if time is None:
            time = curr_end
        if time < 0:
            raise Exception("Adding sound at timestamp < 0")

        new_end = time + new_segment.duration_seconds
        diff = new_end - curr_end
        if diff > 0:
            segment = segment.append(
                AudioSegment.silent(int(np.ceil(diff * 1000))),
                crossfade=0,
            )
        self.audio_segment = segment.overlay(
            new_segment,
            position=int(1000 * time),
            gain_during_overlay=gain_to_background,
        )

    def add_sound(self, sound_file, time=None, gain=None, **kwargs):
        file_path = get_full_sound_file_path(sound_file)
        new_segment = AudioSegment.from_file(file_path)
        if gain:
            new_segment = new_segment.apply_gain(gain)
        self.add_audio_segment(new_segment, time, **kwargs)

    # Writers
    def begin_animation(self, camera, n, allow_write=False):
        if self.write_to_movie and allow_write:
            self.open_movie_pipe(camera, n)

    def end_animation(self, allow_write=False):
        if self.write_to_movie and allow_write:
            self.close_movie_pipe()

    def write_frame(self, frame):
        if self.write_to_movie:
            self.writing_process.stdin.write(frame.tostring())

    def save_image(self, image):
        file_path = self.get_image_file_path()
        image.save(file_path)
        self.print_file_ready_message(file_path)

    def finish(self, indices):
        if self.write_to_movie:
            if hasattr(self, "writing_process"):
                self.writing_process.terminate()
            self.combine_movie_files(indices)

    def open_movie_pipe(self, camera, n):
        file_path = self.get_next_partial_movie_path(n)
        temp_file_path = file_path.replace(".", "_temp.")

        self.partial_movie_file_path = file_path
        self.temp_partial_movie_file_path = temp_file_path

        fps = camera.frame_rate
        height = camera.get_pixel_height()
        width = camera.get_pixel_width()

        command = [
            FFMPEG_BIN,
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', '%dx%d' % (width, height),  # size of one frame
            '-pix_fmt', 'rgba',
            '-r', str(fps),  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-c:v', 'h264_nvenc',
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
        ]
        if self.movie_file_extension == ".mov":
            # This is if the background of the exported video
            # should be transparent.
            command += [
                '-vcodec', 'qtrle',
                # '-vcodec', 'png',
            ]
        else:
            command += [
                '-vcodec', 'libx264',
                '-pix_fmt', 'yuv420p',
            ]

        command += [temp_file_path]
        self.writing_process = subprocess.Popen(command, stdin=subprocess.PIPE)

    def close_movie_pipe(self):
        self.writing_process.stdin.close()
        self.writing_process.wait()
        shutil.move(
            self.temp_partial_movie_file_path,
            self.partial_movie_file_path,
        )

    def combine_movie_files(self, indices):
        # Manim renders the scene as many smaller movie files
        # which are then concatenated to a larger one.  The reason
        # for this is that sometimes video-editing is made easier when
        # one works with the broken up scene, which effectively has
        # cuts at all the places you might want.  But for viewing
        # the scene as a whole, one of course wants to see it as a
        # single piece.
        kwargs = {
            "remove_non_integer_files": True,
            "extension": self.movie_file_extension,
        }

        partial_movie_files = get_sorted_integer_files(
            self.partial_movie_directory,
            min_index = indices[0],
            max_index = indices[1])

        if len(partial_movie_files) == 0:
            print("No animations in this scene")
            return

        # Write a file partial_file_list.txt containing all
        # partial movie files
        file_list = os.path.join(self.partial_movie_directory,
                                 "partial_movie_file_list.txt")

        with open(file_list, 'w') as fp:
            for pf_path in partial_movie_files:
                if os.name == 'nt':
                    pf_path = pf_path.replace('\\', '/')
                fp.write("file \'{}\'\n".format(pf_path))

        movie_file_path = self.get_movie_file_path()
        commands = [
            FFMPEG_BIN,
            '-y',  # overwrite output file if it exists
            '-f', 'concat',
            '-safe', '0',
            '-i', file_list,
            '-c', 'copy',
            '-loglevel', 'error',
            movie_file_path
        ]
        if not self.includes_sound:
            commands.insert(-1, '-an')

        combine_process = subprocess.Popen(commands)
        combine_process.wait()

        if self.includes_sound:
            sound_file_path = movie_file_path.replace(
                self.movie_file_extension, ".wav"
            )
            # Makes sure sound file length will match video file
            self.add_audio_segment(AudioSegment.silent(0))
            self.audio_segment.export(
                sound_file_path,
                bitrate='312k',
            )
            temp_file_path = movie_file_path.replace(".", "_temp.")
            commands = [
                "ffmpeg",
                "-i", movie_file_path,
                "-i", sound_file_path,
                '-y',  # overwrite output file if it exists
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "320k",
                # select video stream from first file
                "-map", "0:v:0",
                # select audio stream from second file
                "-map", "1:a:0",
                '-loglevel', 'error',
                # "-shortest",
                temp_file_path,
            ]
            subprocess.call(commands)
            shutil.move(temp_file_path, movie_file_path)
            subprocess.call(["rm", sound_file_path])

        self.print_file_ready_message(movie_file_path)

    def print_file_ready_message(self, file_path):
        print("\nFile ready at {}\n".format(file_path))
