from pathlib import Path
import cv2, numpy as np, torch
from PIL import Image
from ..config import settings
from .architectures import build_segmentation_model
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
def load_segmentation_model():
    global model
    path = settings.models_dir / "final_segmentation_model.pth"
    if not path.exists(): raise RuntimeError(f"Segmentation model missing: {path}")
    try: model = torch.jit.load(str(path), map_location=DEVICE)
    except RuntimeError:
        model = build_segmentation_model(); checkpoint = torch.load(path, map_location=DEVICE, weights_only=True); model.load_state_dict(checkpoint.get("model_state_dict", checkpoint))
    model.to(DEVICE).eval()
def preprocess_segmentation(image: Image.Image):
    # REPLACE with exactly the resize/normalization used in training.
    array = np.asarray(image.convert("RGB").resize((256, 256)), dtype=np.float32) / 255.0
    return torch.from_numpy(array.transpose(2, 0, 1)).unsqueeze(0)
def predict_segmentation(image: Image.Image):
    if model is None: raise RuntimeError("Segmentation model is not loaded")
    original = np.asarray(image.convert("RGB")); x = preprocess_segmentation(image).to(DEVICE)
    with torch.no_grad(): output = model(x)
    if isinstance(output, (tuple, list)): output = output[0]
    mask = torch.sigmoid(output)[0, 0].detach().cpu().numpy()  # Change if training used multiclass softmax.
    mask = cv2.resize((mask > 0.5).astype(np.uint8) * 255, (original.shape[1], original.shape[0]), interpolation=cv2.INTER_NEAREST)
    overlay = cv2.addWeighted(original, .65, np.dstack([mask, np.zeros_like(mask), np.zeros_like(mask)]), .35, 0)
    return Image.fromarray(mask), Image.fromarray(overlay), image.convert("RGB")
