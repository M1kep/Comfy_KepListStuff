from typing import Any, Dict, List, Tuple

from torch import Tensor

from custom_nodes.Comfy_KepListStuff.utils import AnyType

any_type = AnyType("*")


class ListLengthNode:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(self) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {"In": (any_type, {})},
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("Length",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (False,)
    FUNCTION = "get_len"

    CATEGORY = "List Stuff"

    def get_len(self, In: List[Any]) -> Tuple[int]:
        return (len(In),)


class JoinFloatLists:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(self) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "In1": ("FLOAT", {"forceInput": True}),
                "In2": ("FLOAT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("Joined",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "join_lists"

    CATEGORY = "List Stuff"

    def join_lists(self, In1: List[float], In2: List[float]) -> Tuple[List[float]]:
        return (In1 + In2,)

class JoinImageLists:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(self) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "In1": ("IMAGE",),
                "In2": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("Joined", "Sizes")
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "join_lists"

    CATEGORY = "List Stuff"

    def join_lists(self, In1: List[Tensor], In2: List[Tensor]) -> Tuple[List[Tensor], List[int]]:
        sizes = [len(In1), len(In2)]
        return In1 + In2, sizes
