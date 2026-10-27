import numpy as np, torch
from PIL import Image
from ..config import settings
from .architectures import build_classification_model
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASSES = ["Adenocarcinoma", "High-grade IN", "Low-grade IN", "Normal", "Polyp", "Serrated Adenoma"]
model = None
def load_classification_model():
    global model
    path = settings.models_dir / "best_classifier_model_v3.pth"
    if not path.exists(): raise RuntimeError(f"Classification model missing: {path}")
    try: model = torch.jit.load(str(path), map_location=DEVICE)
    except RuntimeError:
        model = build_classification_model(); checkpoint = torch.load(path, map_location=DEVICE, weights_only=True); model.load_state_dict(checkpoint.get("model_state_dict", checkpoint))
    model.to(DEVICE).eval()
def preprocess_classification(image: Image.Image):
    # REPLACE this with the exact crop/resize/normalization used while training.
    array = np.asarray(image.convert("RGB").resize((224, 224)), dtype=np.float32) / 255.0
    return torch.from_numpy(array.transpose(2, 0, 1)).unsqueeze(0)
def predict_classification(image: Image.Image):
    if model is None: raise RuntimeError("Classification model is not loaded")
    with torch.no_grad(): logits = model(preprocess_classification(image).to(DEVICE))
    if isinstance(logits, (tuple, list)): logits = logits[0]
    probabilities = torch.softmax(logits, dim=1)[0].detach().cpu().tolist()
    if len(probabilities) != 6: raise RuntimeError(f"Expected 6 classifier outputs, received {len(probabilities)}")
    index = int(np.argmax(probabilities)); return {"predicted_class": CLASSES[index], "confidence": probabilities[index], "probabilities": probabilities}
