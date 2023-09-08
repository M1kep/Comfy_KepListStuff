import decimal
from typing import Any, Dict, List, Tuple, Iterator, Union, Optional

import torch
from PIL import ImageFont, ImageDraw
import matplotlib.font_manager as fm
from torch import Tensor

from custom_nodes.Comfy_KepListStuff.utils import (
    zip_with_fill,
    error_if_mismatched_list_args,
    tensor2pil,
    pil2tensor,
)


class IntRangeNode:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "start": ("INT", {"default": 0, "min": 0, "max": 4096, "step": 1}),
                "stop": ("INT", {"default": 0, "min": 0, "max": 4096, "step": 1}),
                "step": ("INT", {"default": 0, "min": 0, "max": 4096, "step": 1}),
                "end_mode": (["Inclusive", "Exclusive"], {"default": "Inclusive"}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("range",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "build_range"

    CATEGORY = "List Stuff"

    def build_range(
        self, start: List[int], stop: List[int], step: List[int], end_mode: List[str]
    ) -> Tuple[List[int]]:
        error_if_mismatched_list_args(locals())

        ret = []
        for e_start, e_stop, e_step, e_end_mode in zip_with_fill(
            start, stop, step, end_mode
        ):
            if e_end_mode == "Inclusive":
                e_stop += 1
            ret.extend(list(range(e_start, e_stop, e_step)))

        return (ret,)


class FloatRangeNode:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "start": ("FLOAT", {"default": 0, "min": 0, "max": 4096, "step": 1}),
                "stop": ("FLOAT", {"default": 0, "min": 0, "max": 4096, "step": 1}),
                "step": ("FLOAT", {"default": 0, "min": 0, "max": 4096, "step": 1}),
                "end_mode": (["Inclusive", "Exclusive"], {"default": "Inclusive"}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("range",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "build_range"

    CATEGORY = "List Stuff"

    @staticmethod
    def _decimal_range(
        start: float, stop: float, step: float, inclusive: bool
    ) -> Iterator[float]:
        ret_val = decimal.Decimal(start)
        if inclusive:
            stop = stop + step

        while ret_val < stop:
            yield float(ret_val)
            ret_val += decimal.Decimal(step)

    def build_range(
        self,
        start: List[float],
        stop: List[float],
        step: List[float],
        end_mode: List[str],
    ) -> Tuple[List[float]]:
        error_if_mismatched_list_args(locals())

        ret = []

        for e_start, e_stop, e_step, e_end_mode in zip_with_fill(
            start, stop, step, end_mode
        ):
            ret.extend(
                list(
                    self._decimal_range(
                        e_start, e_stop, e_step, e_end_mode == "Inclusive"
                    )
                )
            )

        return (ret,)


class ImageLabelOverlay:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "images": ("IMAGE",),
            },
            "optional": {
                "float_labels": ("FLOAT", {"forceInput": True}),
                "int_labels": ("INT", {"forceInput": True}),
                "str_labels": ("STR", {"forceInput": True}),
            },
        }

    RELOAD_INST = True
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Images",)
    INPUT_IS_LIST = (True,)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "put_overlay"

    CATEGORY = "List Stuff"

    def put_overlay(
        self,
        images: List[Tensor],
        float_labels: Optional[List[float]] = None,
        int_labels: Optional[List[int]] = None,
        str_labels: Optional[List[str]] = None,
    ) -> Tuple[List[Tensor]]:
        batches = images

        labels_to_check: Dict[str, Union[List[float], List[int], List[str], None]] = {
            "float": float_labels if float_labels is not None else None,
            "int": int_labels if int_labels is not None else None,
            "str": str_labels if str_labels is not None else None
        }

        for l_type, labels in labels_to_check.items():
            if labels is None:
                continue
            if len(batches) != len(labels) and len(labels) != 1:
                raise Exception(
                    f"Non-matching input sizes got {len(batches)} Image Batches, {len(labels)} Labels for label type {l_type}"
                )

        # margin = 15
        # column_label_size = 45
        # row_label_size = 90
        # font = ImageFont.truetype(fm.findfont(fm.FontProperties()), 40)

        # batch_size = images[0].size()[0]
        # cell_width = images[0].size()[1]
        # cell_height = images[0].size()[2]

        # grid_width = cell_width * len(Y_Labels) * batch_size + 2 * margin
        # grid_height = cell_height * len(X_Labels) + 2 * margin
        # print(f"cell_width: {cell_width} | cell_height: {cell_height} | grid_width: {grid_width} | grid_height: {grid_height}")
        # grid_image = Image.new('RGB', (grid_width, grid_height), 'black')
        # draw = ImageDraw.Draw(grid_image)

        # image is list of images
        # images can be batches. When batched
        font = ImageFont.truetype(fm.findfont(fm.FontProperties()), 60)

        ret_images = []
        loop_gen = zip_with_fill(batches, float_labels, int_labels, str_labels)
        for b_idx, (img_batch, float_lbl, int_lbl, str_lbl) in enumerate(loop_gen):
            batch = []
            for i_idx, img in enumerate(img_batch):
                pil_img = tensor2pil(img)
                print(f"Batch: {b_idx} | img: {i_idx}")
                print(img.size())
                draw = ImageDraw.Draw(pil_img)

                y_offset = 0
                for lbl_type, lbl in zip(["float", "int", "str"], [float_lbl, int_lbl, str_lbl]):
                    if lbl is None:
                        continue
                    draw.rectangle((0, 0 + y_offset, 512, 60 + y_offset), fill="#ffff33")
                    draw.text((0, 0 + y_offset), str(lbl), fill="red", font=font)
                    y_offset += 60
                batch.append(pil2tensor(pil_img))

            ret_images.append(torch.cat(batch))

        return (ret_images,)
