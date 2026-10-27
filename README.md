# Accurate Prediction of Colorectal Cancer Stages Using Deep Learning

## Overview

This project aims to develop a deep learning-based system for analyzing colorectal histopathology images using **image segmentation and tissue classification**. It uses the EBHI-SEG dataset to identify abnormal tissue regions and classify images into six tissue categories.

The objective is to explore how artificial intelligence can assist pathologists in analyzing tissue images and support further research into colorectal cancer assessment.

**Important:** The six tissue categories in EBHI-SEG do not directly represent clinical cancer stages I–IV. Accurate clinical staging requires additional pathological and clinical information.

## Objectives

- Develop a deep learning model for segmenting tissue regions in histopathology images.
- Classify colorectal tissue images into six categories.
- Evaluate model performance using appropriate segmentation and classification metrics.
- Visualize predicted segmentation masks and classification results.
- Develop a foundation for a computer-assisted colorectal cancer analysis system.

## Dataset

**Dataset:** EBHI-SEG (Endoscopic Biopsy Histopathological Image Segmentation)

The dataset contains histopathological images organized into six tissue categories:

| Class | Description |
|---|---|
| Normal | Normal tissue |
| Polyp | Polyp tissue |
| Low-grade IN | Low-grade intraepithelial neoplasia |
| High-grade IN | High-grade intraepithelial neoplasia |
| Serrated adenoma | Serrated adenomatous tissue |
| Adenocarcinoma | Cancerous glandular tissue |

The dataset also provides segmentation annotations for the corresponding images. The exact mask format and annotation conventions should be verified before training.

**Dataset source:** [EBHI-SEG on GitHub / research repositories](https://github.com/) — replace this placeholder with the verified dataset source or original research paper URL.

Note: The dataset's six tissue categories should not be treated as confirmed TNM or Stage I–IV labels.

## Technologies Used

- **Programming language:** Python
- **Deep learning framework:** PyTorch
- **Image processing:** OpenCV, NumPy
- **Data handling:** PyTorch Dataset and DataLoader
- **Visualization:** Matplotlib
- **Model architecture:** U-Net-based segmentation
- **Development environment:** Google Colab / Jupyter Notebook

## System Workflow

```text
EBHI-SEG Dataset
       |
       v
Image and Mask Loading
       |
       v
Preprocessing
(Resize, Normalize, Validate)
       |
       v
U-Net Segmentation
       |
       v
Predicted Tissue Mask
       |
       v
Tissue Region Analysis
       |
       v
Six-Class Tissue Classification
       |
       v
Evaluation and Visualization
```

The segmentation and classification components are separate tasks. The classification component must be trained and evaluated using the six tissue labels. Clinical stage prediction requires additional, appropriately labeled data.

## Project Structure

A suggested repository structure is:

```text
colorectal-cancer-prediction/
├── app.py
├── README.md
├── requirements.txt
├── notebooks/
│   └── ColoreCtal.ipynb
├── src/
│   ├── dataset.py
│   ├── unet_model.py
│   ├── train_segmentation.py
│   ├── classification_model.py
│   └── evaluate.py
├── models/
│   ├── segmentation_model.pth
│   └── classification_model.pth
├── results/
│   ├── segmentation/
│   └── classification/
└── .gitignore
```

*This is a suggested structure; adjust it to match the files actually present in your repository.*

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd colorectal-cancer-prediction
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

Create a `requirements.txt` file with the packages used by your implementation. For the current segmentation notebook, the main dependencies are:

```text
torch
torchvision
numpy
opencv-python
matplotlib
tqdm
scikit-learn
```

Install them using:

```bash
pip install -r requirements.txt
```

For GPU training, install a PyTorch build compatible with your CUDA environment, following the [official PyTorch installation guide](https://pytorch.org/get-started/locally/).

## Running the Project

### Google Colab

1. Open the project notebook.
2. Mount Google Drive if the dataset is stored there.
3. Update the image and mask paths.
4. Run the notebook cells in order.
5. Train the segmentation model.
6. Visualize the input images, ground-truth masks, and predicted masks.
7. Save the trained model weights.

### Running locally

After downloading the dataset and updating the paths, run your training notebook or Python training script.

If `app.py` is a Streamlit application, start it with:

```bash
streamlit run app.py
```

If it is a regular Python script, use:

```bash
python app.py
```

The appropriate command depends on how `app.py` is implemented.

## Model Architecture

### U-Net Segmentation

U-Net is a convolutional neural network architecture designed for pixel-level image segmentation.

Its main components are:

- **Encoder:** Extracts features from the input image.
- **Decoder:** Reconstructs the segmentation mask.
- **Skip connections:** Transfer spatial information from encoder layers to decoder layers.

The current prototype uses PyTorch and a simplified encoder-decoder network. It can be upgraded to a full U-Net with downsampling, upsampling, and skip connections.

### Six-Class Tissue Classification

A separate classification model can predict one of the following tissue categories:

1. Normal
2. Polyp
3. Low-grade IN
4. High-grade IN
5. Serrated adenoma
6. Adenocarcinoma

The classification model should be trained with the appropriate image-level labels and evaluated independently.

## Evaluation Metrics

### Segmentation

- **Dice Score:** Measures the overlap between the predicted mask and the ground-truth mask.
- **Intersection over Union (IoU):** Measures the intersection relative to the union of predicted and actual regions.
- **Pixel Accuracy:** Measures the proportion of correctly classified pixels.

### Classification

- Accuracy
- Precision
- Recall (Sensitivity)
- F1-score
- Confusion matrix

Evaluation should use separate training, validation, and test sets. Results should be calculated on held-out test data rather than the same images used for training.

## Current Status

- [x] EBHI-SEG dataset exploration
- [x] Image and mask loading using PyTorch
- [x] Image resizing and normalization
- [x] Initial simplified segmentation model
- [x] Training loop and model weight saving
- [x] Initial segmentation visualization and metric calculation
- [ ] Full U-Net architecture with skip connections
- [ ] Train/validation/test split
- [ ] Data augmentation
- [ ] Reliable held-out segmentation evaluation
- [ ] Six-class tissue classification model
- [ ] Integration of segmentation and classification
- [ ] Clinical stage prediction using appropriately labeled clinical data
- [ ] Final application integration and testing

## Limitations

- EBHI-SEG tissue categories do not directly provide clinical Stage I–IV labels.
- The initial segmentation implementation is a simplified U-Net prototype.
- Model performance depends on annotation quality, class distribution, preprocessing, and the train/test split.
- Generalization to images from other hospitals and scanners requires further validation.
- Clinical use would require expert review, independent clinical validation, and appropriate regulatory assessment.

## Future Scope

- Implement and optimize a full U-Net segmentation architecture.
- Experiment with Attention U-Net, U-Net++, and other segmentation models.
- Improve six-class tissue classification using transfer learning.
- Integrate explainable AI techniques to visualize regions influencing predictions.
- Combine histopathology images with clinical and pathological data for more reliable cancer staging.
- Evaluate the system on independent datasets and, in future, clinically validated data.

## Medical Disclaimer

This project is intended for educational and research purposes only. It is not a clinically validated diagnostic tool and must not be used to determine a patient's cancer stage or treatment. All clinical decisions must be made by qualified healthcare professionals.

## Author

**Shreyash Gurav**  
B.Tech Computer Science and Engineering

Project: Accurate Prediction of Colorectal Cancer Stages Using Deep Learning
