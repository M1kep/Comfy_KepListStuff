from typing import Dict, Any, List, Tuple, Optional, Iterator, Union

import PIL.Image
import numpy as np
import torch
from PIL import Image
from torch import Tensor


def validate_list_args(args: Dict[str, List[Any]]) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Checks that if there are multiple arguments, they are all the same length or 1
    :param args:
    :return: Tuple (Status, mismatched_key_1, mismatched_key_2)
    """
    # Only have 1 arg
    if len(args) == 1:
        return True, None, None

    len_to_match = None
    matched_arg_name = None
    for arg_name, arg in args.items():
        if arg_name == 'self':
            # self is in locals()
            continue

        if len(arg) != 1:
            if len_to_match is None:
                len_to_match = len(arg)
                matched_arg_name = arg_name
            elif len(arg) != len_to_match:
                return False, arg_name, matched_arg_name

    return True, None, None

def error_if_mismatched_list_args(args: Dict[str, List[Any]]) -> None:
    is_valid, failed_key1, failed_key2 = validate_list_args(args)
    if not is_valid:
        assert failed_key1 is not None
        assert failed_key2 is not None
        raise ValueError(
            f"Mismatched list inputs received. {failed_key1}({len(args[failed_key1])}) !== {failed_key2}({len(args[failed_key2])})"
        )

def zip_with_fill(*lists: Union[List[Any], None]) -> Iterator[Tuple[Any, ...]]:
    """
    Zips lists together, but if a list has 1 element, it will be repeated for each element in the other lists.
    If a list is None, None will be used for that element.
    (Not intended for use with lists of different lengths)
    :param lists:
    :return: Iterator of tuples of length len(lists)
    """
    max_len = max(len(lst) if lst is not None else 0 for lst in lists)
    for i in range(max_len):
        yield tuple(None if lst is None else (lst[0] if len(lst) == 1 else lst[i]) for lst in lists)

def tensor2pil(image: Tensor) -> PIL.Image.Image:
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


def pil2tensor(image: PIL.Image.Image) -> Tensor:
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)



if __name__ == "__main__":
    # Tests
    validate_list_args({"a": [1, 2, 3], "b": [1, 2, 3]})
    validate_list_args({"a": [1, 2, 3], "b": [1, 2, 3], "c": [1, 2, 3]})
    validate_list_args({"a": [1, 2, 3], "b": [1, 2, 3], "c": [1, 2, 3], "d": [1, 2, 3]})
    validate_list_args({"a": [1, 2, 3], "b": [1, 2, 3], "c": [1, 2, 3], "d": [1, 2, 3], "e": [1, 2, 3]})
    # Fails
    validate_list_args({"a": [1, 2, 3], "b": [1, 2, 3, 4]})

    # Tests
    print(list(zip_with_fill([1], [4, 5, 6], [8])))
