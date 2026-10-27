# ColoVision AI backend

## Install
1. Install Python 3.11 and MySQL 8.
2. Create database: `CREATE DATABASE colorectal_ai;`
3. Run `python -m venv .venv`, `.\.venv\Scripts\Activate.ps1`, and `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`, then set your MySQL password and a long JWT secret.
5. Copy your two model files into `models/` with these exact names:
   - `final_segmentation_model.pth`
   - `best_classifier_model_v3.pth`
6. Copy the exact model class definitions plus preprocessing from the training notebook into `app/services/architectures.py`, `segmentation.py`, and `classification.py`.
7. Run `uvicorn app.main:app --reload`.

## Important model rule
This backend never returns mock predictions. `.pth` state dictionaries require the architecture that created them. The current loader supports TorchScript automatically; otherwise it stops at startup with a precise error until you add the exact training architecture. It also marks the temporary 256/224 resize transforms as required replacements.

## First administrator
Create the first `Admin` only in a local one-time setup script, using `hash_password()`; never expose a public admin-registration endpoint.
