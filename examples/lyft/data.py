from pathlib import Path

import matplotlib.pyplot as plt
import torchvision
from torch.utils.data import DataLoader

from nncore.core.transforms.albumentation import TRANSFORM_REGISTRY
from nncore.segmentation.datasets import DATASET_REGISTRY
from nncore.segmentation.utils import tensor2cmap
from nncore.utils.getter import get_instance_recursively
from nncore.utils.loading import load_yaml
from nncore.utils.utils import inverse_normalize_batch, tensor2plt

if __name__ == "__main__":
    dataset = DATASET_REGISTRY.get("LyftDataset.from_folder")(
        root="../../../Lyft/",
        mask_folder_name="CameraSeg",
        image_folder_name="CameraRGB",
        test=False,
    )
    transform_cfg = load_yaml("transform.yml")
    transform = get_instance_recursively(transform_cfg, registry=TRANSFORM_REGISTRY)
    dataset.transform = transform["train"]
    im = dataset[0]["input"]
    mask = dataset[0]["mask"]
    dataloader = DataLoader(dataset, batch_size=4, shuffle=False, num_workers=4)
    for data in dataloader:
        im = data["input"]
        target = data["mask"]

        im = inverse_normalize_batch(im)
        target = tensor2cmap(target, label_format="voc")
        im = torchvision.utils.make_grid(im, nrow=2, normalize=True)
        target = torchvision.utils.make_grid(target, nrow=2, normalize=False)
        save_dir = Path("./")

        im = tensor2plt(im, title="inputs")
        target = tensor2plt(target.long(), title="labels")
        plt.show()
        break
