"""Paste the EXACT model classes and training transforms into this file.

A state_dict .pth file cannot be reconstructed without its original model architecture.
Do not substitute a different CNN/UNet: it may load incorrectly or yield invalid results.
"""
def build_segmentation_model():
    raise RuntimeError("Add the exact segmentation architecture from training in services/architectures.py")
def build_classification_model():
    raise RuntimeError("Add the exact classifier architecture from training in services/architectures.py")
