from typing import Any, Dict, List, Tuple

from custom_nodes.Comfy_KepListStuff.utils import AnyType

any_type = AnyType("*")


class StringReplace:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(self) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "String": ("STRING", {"multiline": True}),
                "Old": ("STRING", {"multiline": False}),
                "New": (any_type, {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Strings",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "list_replace"

    CATEGORY = "List Stuff"

    def list_replace(self, String: List[str], Old: List[str], New: List[Any]) -> Tuple[List[str]]:
        if len(Old) != 1:
            raise ValueError("Old does not support multiple values")
        if len(String) != 1:
            raise ValueError("String does not support multiple values")

        returns = []
        for replacement in New:
            returns.append(String[0].replace(Old[0], str(replacement)))
        return (returns,)
