from custom_nodes.Comfy_KepListStuff.nodes.deprecated import StackImages
from custom_nodes.Comfy_KepListStuff.nodes.images import (
    ImageLabelOverlay,
    EmptyImages,
)
from custom_nodes.Comfy_KepListStuff.nodes.list_utils import (
    ListLengthNode,
    JoinFloatLists,
    JoinImageLists,
)
from custom_nodes.Comfy_KepListStuff.nodes.range_nodes import (
    IntRangeNode,
    FloatRangeNode,
    IntNumStepsRangeNode,
    FloatNumStepsRangeNode,
)

NODE_CLASS_MAPPINGS = {
    "Range(Step) - Int": IntRangeNode,
    "Range(Num Steps) - Int": IntNumStepsRangeNode,
    "Range(Step) - Float": FloatRangeNode,
    "Range(Num Steps) - Float": FloatNumStepsRangeNode,
    "List Length": ListLengthNode,
    "Image Overlay": ImageLabelOverlay,
    "Stack Images": StackImages,
    "Empty Images": EmptyImages,
    "Join Image Lists": JoinImageLists,
    "Join Float Lists": JoinFloatLists,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Stack Images": "Stack Images(Deprecated)",
}
