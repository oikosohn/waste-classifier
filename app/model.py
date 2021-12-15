import io

from typing import List, Dict, Any, Type, Union
import yaml
from PIL import Image

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import albumentations
import albumentations.pytorch

from src.model import Model


# @st.cache
def get_model() -> Model:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_instance = Model('model/model.yml', verbose=True)
    model_instance.model.load_state_dict(
        torch.load('model/model.pt', map_location=torch.device("cpu"))
    )
    model = model_instance.model
    model = model.to(device)
    
    return model

def _transform_image(image_bytes: bytes):
    transform = albumentations.Compose(
        [
            albumentations.Resize(height=512, width=384),
            albumentations.Normalize(mean=(0.5, 0.5, 0.5), std=(0.2, 0.2, 0.2)),
            albumentations.pytorch.transforms.ToTensorV2(),
        ]
    )
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image_array = np.array(image)
    return transform(image=image_array)["image"].unsqueeze(0)


def predict_from_image_byte(model: Model, image_bytes: bytes, config: Dict[str, Any]) -> List[str]:
    transformed_image = _transform_image(image_bytes)
    outputs = model.forward(transformed_image)
    _, y_hat = outputs.max(1)
    return config["classes"][y_hat.item()]


def get_config(config_path: str = "app/config.yaml"):
    import os
    print(os.getcwd())

    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config