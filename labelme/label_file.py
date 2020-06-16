import base64
import io
import json
import os.path as osp

import PIL.Image

from labelme import __version__
from labelme.logger import logger
from labelme import PY2
from labelme import QT4
from labelme import utils


PIL.Image.MAX_IMAGE_PIXELS = None


class LabelFileError(Exception):
    pass


class LabelFile(object):

    def __init__(self, label_id, save_fn, load_fn, image_load_fn, label_data=None):
        self.label_id = label_id
        self.shapes = []
        self._save_ = save_fn
        self._load_ = load_fn
        self._load_image_ = image_load_fn
        self.imagePath = None
        self.imageData = None
        self.load(label_data)

    def load(self,data=None):
        keys = [
            "version",
            "imageData",
            "imagePath",
            "shapes",  # polygonal annotations
            "flags",  # image level flags
            "imageHeight",
            "imageWidth",
            "label_id",
            "image_id"
        ]
        shape_keys = [
            "label",
            "points",
            "group_id",
            "shape_type",
            "flags",
        ]
        try:
            if data is None:
                success,data = self._load_(self.label_id)
                if not success:
                    raise LabelFileError(f'Load Label:{self.label_id} Error')

            version = data.get("version")
            if version is None:
                logger.warn(
                    "Loading JSON file ({}) of unknown version".format(
                        self.label_id
                    )
                )
            elif version.split(".")[0] != __version__.split(".")[0]:
                logger.warn(
                    "This JSON file ({}) may be incompatible with "
                    "current labelme. version in file: {}, "
                    "current version: {}".format(
                        self.label_id, version, __version__
                    )
                )

            success,imageData = self._load_image_(data['image_id'])
            flags = data.get("flags") or {}
            imagePath = data["imagePath"]
            shapes = [
                dict(
                    label=s["label"],
                    points=s["points"],
                    shape_type=s.get("shape_type", "polygon"),
                    flags=s.get("flags", {}),
                    group_id=s.get("group_id"),
                    other_data={
                        k: v for k, v in s.items() if k not in shape_keys
                    },
                )
                for s in data["shapes"]
            ]
        except Exception as e:
            raise LabelFileError(e)

        otherData = {}
        for key, value in data.items():
            if key not in keys:
                otherData[key] = value

        # Only replace data after everything is loaded.
        self.flags = flags
        self.shapes = shapes
        self.imagePath = imagePath
        self.imageData = imageData
        # self.filename = filename
        self.otherData = otherData


    def save(
        self,
        filename,
        shapes,
        imagePath,
        imageHeight,
        imageWidth,
        imageData=None,
        otherData=None,
        flags=None,
    ):
        if otherData is None:
            otherData = {}
        if flags is None:
            flags = {}
        data = dict(
            version=__version__,
            flags=flags,
            shapes=shapes,
            imagePath=imagePath,
            imageData=None,
            imageHeight=imageHeight,
            imageWidth=imageWidth,
        )
        for key, value in otherData.items():
            assert key not in data
            data[key] = value
        try:
            self._save_(self.label_id,data)
            self.filename = filename
        except Exception as e:
            raise LabelFileError(e)

