from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import vgg16, resnet50
from tensorflow.keras.models import Model
from PIL import Image
import requests

import numpy as np
from numpy import dot
from numpy.linalg import norm

__all__ = ["FeatureExtractor"]


class FeatureExtractor:
    def __init__(
        self, type: str = "vgg16", weights: str = "imagenet", color_type: str = "RGB"
    ):
        self.model = ImageNet(model=type, weights=weights, color_type=color_type)

    def _convert_url(self, url):
        return Image.open(requests.get(url, stream=True).raw)

    def get_feature(self, url):
        images = self._convert_url(url)
        return self.model.get_extract(images)


class ImageNet:
    """
    이걸 object.classmethod로 만들 수 있을거 같은데
    안되네...
    """

    def __init__(
        self, model: str = "vgg16", weights: str = "imagenet", color_type: str = "RGB"
    ):
        self.select_model = model
        self.model = None
        self.extract_model = self._build_model(weights)
        self.color_type = color_type

    def _build_model(self, weights: str = "imagenet"):
        if self.select_model == "vgg16":
            self.model = vgg16
            base_model = self.model.VGG16(weights=weights)
        elif self.select_model == "resnet50":
            self.model = resnet50
            base_model = self.model.ResNet50(weights=weights)

        return Model(
            inputs=base_model.input, outputs=base_model.get_layer("fc1").output
        )

    def get_extract(self, images):
        images = images.resize((224, 224))
        images = images.convert(self.color_type)

        x = image.img_to_array(images)
        x = np.expand_dims(x, axis=0)
        x = self.model.preprocess_input(x)
        feature = self.extract_model.predict(x)[0]

        return feature / norm(feature)
