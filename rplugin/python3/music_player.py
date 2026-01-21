"""Python code for ``nvim-music-player``."""
from os.path import exists, realpath
from shutil import which
from subprocess import DEVNULL, Popen
from typing import NoReturn, Tuple

import pynvim


@pynvim.plugin
class MusicPlayer:
    """
    Music player Neovim plugin class.

    Parameters
    ----------
    nvim : pynvim.Nvim
        The Neovim instance.

    Attributes
    ----------
    nvim : pynvim.Nvim
        The Neovim instance.
    file : str or None
        The currently playing file path.
    process : subprocess.Popen or None
        The ``mpv`` process.
    """

    nvim: pynvim.Nvim
    process: Popen | None
    file: str | None
    cmd: str | None

    def __init__(self, nvim: pynvim.Nvim):
        self.cmd: str | None = which("mpv")
        self.nvim: pynvim.Nvim = nvim
        self.process: Popen | None = None
        self.file: str | None = None

    @pynvim.command("MusicPlay", nargs=1, complete="file")
    def play(self, args: Tuple[str]) -> NoReturn:
        """Start playing the given music file."""
        if self.cmd is None:
            self.nvim.err_write("🎵 nvim-music-player: Unable to find `mpv` in PATH\n")
            return

        path: str = realpath(args[0].replace('\\ ', ' '))
        if not exists(path):
            self.nvim.err_write(f"🎵 nvim-music-player: ❌ File not found: {path}\n")
            return

        if self.file is not None and self.file == path:
            self.stop()
            return

        self.file = path
        if self.process is not None:
            self.process.terminate()

        self.process = Popen([self.cmd, "--no-video", path], stdout=DEVNULL, stderr=DEVNULL)
        self.nvim.out_write(f"🎵 nvim-music-player: 🎶 Playing: {path}\n")

    @pynvim.command("MusicStop", nargs=0, bang=True)
    def stop(self, bang: bool = False) -> NoReturn:
        """
        Stop the music player.

        Parameters
        ----------
        bang : bool, optional, default=False
            Whether the command was called with a bang (``!``) or not.
        """
        if self.process is None:
            if not bang:
                self.nvim.out_write("🎵 nvim-music-player: Music already stopped\n")

            return

        self.process.terminate()
        self.process = None
        self.file = None
        self.nvim.out_write("🎵 nvim-music-player: ⏹ Music stopped\n")

# vim: set ts=4 sts=4 sw=4 et ai si sta:
