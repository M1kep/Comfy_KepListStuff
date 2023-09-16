import itertools
from typing import List, Any


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


# Our any instance wants to be a wildcard string
ANY = AnyType("*")


class UnzippedProductAny:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "X": (ANY, {}),
                "Y": (ANY, {}),
                "X_Label_Fallback": (["str()", "Numbers"], {"default": "str()", "name": "X Label Fallback"}),
                "Y_Label_Fallback": (["str()", "Numbers"], {"default": "str()", "name": "Y Label Fallback"})
            },
            "optional": {"X_Labels": (ANY, {"name": "X Labels"}), "Y_Labels": (ANY, {"name": "Y Labels"})},
        }

    RETURN_TYPES = (ANY, "STRING", ANY, "STRING", "INT", "INT")
    RETURN_NAMES = ("X Values", "X Labels", "Y Values", "Y Labels", "Total Images", "Split Every")
    OUTPUT_IS_LIST = (True, True, True, True, False, False)
    INPUT_IS_LIST = True
    FUNCTION = "to_xy"

    CATEGORY = "List Stuff"

    def to_xy(self, X: List[Any], Y: List[Any], X_Label_Fallback: List[str], Y_Label_Fallback: List[str], X_Labels: List[Any] = None, Y_Labels: List[Any] = None):
        #region Validation
        if len(X_Label_Fallback) != 1:
            raise Exception("X_Label_Fallback must be a single value")
        if len(Y_Label_Fallback) != 1:
            raise Exception("Y_Label_Fallback must be a single value")

        #region Labels
        if X_Label_Fallback[0] == "str()":
            get_x_fallback_labels = lambda x: [str(i) for i in x]
        else:
            get_x_fallback_labels = lambda x: list(range(len(x)))

        if Y_Label_Fallback[0] == "str()":
            get_y_fallback_labels = lambda x: [str(i) for i in x]
        else:
            get_y_fallback_labels = lambda x: list(range(len(x)))

        if X_Labels is None:
            X_Labels = get_x_fallback_labels(X)
        if Y_Labels is None:
            Y_Labels = get_y_fallback_labels(Y)
        #endregion

        product = itertools.product(X, Y)
        X_out, Y_out = zip(*product)
        X_out = list(X_out)
        Y_out = list(Y_out)

        return (X_out, X_Labels, Y_out, Y_Labels, len(X_out), len(Y))
