from .nodes import IntRangeNode, FloatRangeNode, ImageLabelOverlay

NODE_CLASS_MAPPINGS = {
    "Range - Int": IntRangeNode,
    "Range - Float": FloatRangeNode,
    "Image Overlay": ImageLabelOverlay,
}
