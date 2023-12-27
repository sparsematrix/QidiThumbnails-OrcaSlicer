# Copyright (c) 2023 Molodos
# The QidiThumbnails plugin is released under the terms of the AGPLv3 or higher.

import argparse
import base64
import platform
from argparse import Namespace
from array import array
from ctypes import CDLL
from os import path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage

import lib_col_pic


class QidiThumbnails:
    """
    QidiThumbnails post processing script
    """

    def __init__(self):
        args: Namespace = self._parse_args()
        self._gcode: str = args.gcode
        self._thumbnail: QImage = self._get_q_image_thumbnail()

    @classmethod
    def _parse_args(cls) -> Namespace:
        """
        Parse arguments from Orca slicer
        """
        # Parse arguments
        parser = argparse.ArgumentParser(
            prog="QidiThumbnails-OrcaSlicer",
            description="A post processing script to add Qidi thumbnails to gcode")

        parser.add_argument("gcode", help="Gcode path provided by Orca Slicer", type=str)
        return parser.parse_args()

    def _get_base64_thumbnail(self) -> str:
        """
        Read the base64 encoded thumbnail from gcode file
        """
        # Try to find thumbnail
        found: bool = False
        base64_thumbnail: str = ""
        with open(self._gcode, "r", encoding="utf8") as file:
            for line in file.read().splitlines():
                if not found and line.startswith("; thumbnail begin "):
                    found = True
                elif found and line == "; thumbnail end":
                    return base64_thumbnail
                elif found:
                    base64_thumbnail += line[2:]

        # If not found, raise exception
        raise Exception(
            "Correct size thumbnail is not present: Make sure, that your slicer generates a thumbnail.")

    def _get_q_image_thumbnail(self) -> QImage:
        """
        Read the base64 encoded thumbnail from gcode file and parse it to a QImage object
        """
        # Read thumbnail
        base64_thumbnail: str = self._get_base64_thumbnail()

        # Parse thumbnail
        thumbnail = QImage()
        thumbnail.loadFromData(base64.decodebytes(bytes(base64_thumbnail, "UTF-8")), "PNG")
        return thumbnail

    def _generate_gcode_prefix(self) -> str:
        """
        Generate a g-code prefix string
        """
        # Parse to g-code prefix
        gcode_prefix: str = ""

        # Generate thumbs. Sizes taken from default Qidi Slicer thumbnail configuration
        gcode_prefix += self._parse_thumbnail_new(self._thumbnail, 380, 380, "gimage")
        gcode_prefix += self._parse_thumbnail_new(self._thumbnail, 210, 210, "simage")

        # Return
        return gcode_prefix

    def add_thumbnail_prefix(self) -> None:
        """
        Adds thumbnail prefix to the gcode file if thumbnail doesn't already exist
        """
        # Get gcode
        g_code: str
        with open(self._gcode, "r", encoding="utf8") as file:
            g_code: str = file.read()

        # Append thumbnail to end of file
        if ';gimage:' not in g_code and ';simage:' not in g_code:
            gcode_prefix: str = self._generate_gcode_prefix()
            with open(self._gcode, "a", encoding="utf8") as file:
                file.write(gcode_prefix)

    @classmethod
    def _parse_thumbnail_new(cls, img: QImage, width: int, height: int, img_type: str) -> str:
        """
        Parse thumbnail to string for new printers
        TODO: Maybe optimize at some time
        """
        img_type = f";{img_type}:"

        result = ""
        b_image = img.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        img_size = b_image.size()
        color16 = array('H')
        try:
            for i in range(img_size.height()):
                for j in range(img_size.width()):
                    pixel_color = b_image.pixelColor(j, i)
                    r = pixel_color.red() >> 3
                    g = pixel_color.green() >> 2
                    b = pixel_color.blue() >> 3
                    rgb = (r << 11) | (g << 5) | b
                    color16.append(rgb)
            output_data = bytearray(img_size.height() * img_size.width() * 10)
            result_int = lib_col_pic.ColPic_EncodeStr(color16, img_size.height(), img_size.width(), output_data,
                                                      img_size.height() * img_size.width() * 10, 1024)

            result += '\r' + img_type
            for i in range(len(output_data)):
                if output_data[i] != 0:
                    result += chr(output_data[i])

        except Exception as e:
            raise e

        return result + '\r'


if __name__ == "__main__":
    """
    Init point of the script
    """
    thumbnail_generator: QidiThumbnails = QidiThumbnails()
    thumbnail_generator.add_thumbnail_prefix()
