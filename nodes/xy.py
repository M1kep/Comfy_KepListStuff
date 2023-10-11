import itertools
from typing import List, Any, Optional, Callable, Tuple, Dict


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


# Our any instance wants to be a wildcard string
ANY = AnyType("*")


class UnzippedProductAny:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "X": (ANY, {}),
                "Y": (ANY, {}),
                "X_Label_Fallback": (["str()", "Numbers"], {"default": "str()"}),
                "Y_Label_Fallback": (["str()", "Numbers"], {"default": "str()"}),
                "Z_Label_Fallback": (["str()", "Numbers"], {"default": "str()"}),
            },
            "optional": {
                "Z": (ANY, {}),
                "X_Labels": (ANY, {}),
                "Y_Labels": (ANY, {}),
                "Z_Labels": (ANY, {}),
            },
        }

    RETURN_NAMES, RETURN_TYPES = zip(*{
        "X Values": ANY,
        "X Labels": "STRING",
        "Y Values": ANY,
        "Y Labels": "STRING",
        "Z Values": ANY,
        "Z Labels": "STRING",
        "Total Images": "INT",
        "Split Every": "INT",
    }.items())

    OUTPUT_IS_LIST = (True, True, True, True, True, True, False, False)
    INPUT_IS_LIST = True
    FUNCTION = "to_xy"

    CATEGORY = "List Stuff"

    def to_xy(
        self,
        X: List[Any],
        Y: List[Any],
        X_Label_Fallback: List[str],
        Y_Label_Fallback: List[str],
        Z_Label_Fallback: List[str],
        Z: Optional[List[Any]] = None,
        X_Labels: Optional[List[Any]] = None,
        Y_Labels: Optional[List[Any]] = None,
        Z_Labels: Optional[List[Any]] = None,
    ) -> Tuple[List[Any], List[str], List[Any], List[str], List[Any], List[str], int, int]:
        # region Validation
        if len(X_Label_Fallback) != 1:
            raise Exception("X_Label_Fallback must be a single value")
        if len(Y_Label_Fallback) != 1:
            raise Exception("Y_Label_Fallback must be a single value")
        if len(Z_Label_Fallback) != 1:
            raise Exception("Z_Label_Fallback must be a single value")

        if Z_Labels is not None and Z is None:
            raise Exception("Z_Labels must be None if Z is None")

        # region Labels
        get_x_fallback_labels: Callable[[Any], List[str]]
        if X_Label_Fallback[0] == "str()":
            get_x_fallback_labels = lambda x: [str(i) for i in x]
        else:
            get_x_fallback_labels = lambda x: [str(i) for i in range(len(x))]

        get_y_fallback_labels: Callable[[Any], List[str]]
        if Y_Label_Fallback[0] == "str()":
            get_y_fallback_labels = lambda x: [str(i) for i in x]
        else:
            get_y_fallback_labels = lambda x: [str(i) for i in range(len(x))]

        get_z_fallback_labels: Callable[[Any], List[str]]
        if Z_Label_Fallback[0] == "str()":
            get_z_fallback_labels = lambda x: [str(i) for i in x]
        else:
            get_z_fallback_labels = lambda x: [str(i) for i in range(len(x))]

        if X_Labels is None:
            X_Labels = get_x_fallback_labels(X)
        if Y_Labels is None:
            Y_Labels = get_y_fallback_labels(Y)
        if Z_Labels is None and Z is not None:
            Z_Labels = get_z_fallback_labels(Z)
        # endregion

        xy_product = itertools.product(X, Y)
        X_out_tuple, Y_out_tuple = zip(*xy_product)
        X_out: List[str] = list(X_out_tuple)
        Y_out: List[str] = list(Y_out_tuple)

        Z_out = []
        if Z is not None:
            original_len = len(X_out)
            X_out = X_out * len(Z)
            Y_out = Y_out * len(Z)
            for z in Z:
                Z_out.extend([z] * original_len)


        if Z_Labels is None:
            Z_Labels = []

        return X_out, X_Labels, Y_out, Y_Labels, Z_out, Z_Labels, len(X_out), len(Y)
