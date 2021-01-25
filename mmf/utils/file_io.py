# Copyright (c) Facebook, Inc. and its affiliates.

import os
import shutil
from typing import List, Optional

from iopath.common.file_io import PathManager as ioPathManagerClass


ioPathManager = ioPathManagerClass()

try:
    # [FB only] register internal file IO handlers
    from mmf.utils.fb.file_io_handlers import register_handlers

    register_handlers()
except ImportError:
    pass


class PathManager:
    """
    Wrapper for insulating OSS I/O (using Python builtin operations) from
    ioPath's PathManager abstraction (for transparently handling various
    internal backends). This is adapted from
    `fairseq <https://github.com/pytorch/fairseq/blob/master/fairseq/file_io.py>`.
    """

    @staticmethod
    def open(
        path: str,
        mode: str = "r",
        buffering: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
    ):
        if ioPathManager:
            return ioPathManager.open(
                path=path,
                mode=mode,
                buffering=buffering,
                encoding=encoding,
                errors=errors,
                newline=newline,
            )
        return open(
            path,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    @staticmethod
    def copy(src_path: str, dst_path: str, overwrite: bool = False) -> bool:
        if ioPathManager:
            return ioPathManager.copy(
                src_path=src_path, dst_path=dst_path, overwrite=overwrite
            )
        return shutil.copyfile(src_path, dst_path)

    @staticmethod
    def get_local_path(path: str, **kwargs) -> str:
        if ioPathManager:
            return ioPathManager.get_local_path(path, **kwargs)
        return path

    @staticmethod
    def exists(path: str) -> bool:
        if ioPathManager:
            return ioPathManager.exists(path)
        return os.path.exists(path)

    @staticmethod
    def isfile(path: str) -> bool:
        if ioPathManager:
            return ioPathManager.isfile(path)
        return os.path.isfile(path)

    @staticmethod
    def ls(path: str) -> List[str]:
        if ioPathManager:
            return ioPathManager.ls(path)
        return os.listdir(path)

    @staticmethod
    def mkdirs(path: str) -> None:
        if ioPathManager:
            return ioPathManager.mkdirs(path)
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def rm(path: str) -> None:
        if ioPathManager:
            return ioPathManager.rm(path)
        os.remove(path)

    @staticmethod
    def register_handler(handler) -> None:
        if ioPathManager:
            return ioPathManager.register_handler(handler=handler)
