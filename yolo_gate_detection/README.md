\# YOLO Gate Detection



\## Overview

This module uses \*\*YOLO11n\*\* to detect racing gates in the Gazebo drone racing simulation.



The model identifies racing gates and returns bounding boxes and confidence scores. It is intended to support the autonomous navigation system.



\## Dataset

\- Environment: Tuwaiq Project 1 Pro Lite racing arena

\- Total images: 1,200

\- Training images: 840

\- Validation images: 180

\- Test images: 180

\- Object class: `gate`

\- Total annotated bounding boxes: 3,287

\- Hard-negative images: 240



The dataset contains different gate distances, viewing angles, heights, and partially occluded gates.



\## Model Training

\- Model: YOLO11n

\- Framework: Ultralytics

\- Input image size: 640

\- Batch size: 8

\- Training device: NVIDIA RTX 4050 Laptop GPU

\- Training configuration: Up to 100 epochs



\## Test Results

\- Precision: 98.5%

\- Recall: 98.1%

\- mAP50: 98.5%

\- mAP50-95: 93.5%



These results were obtained on the held-out test split from the same simulated arena. Performance in new environments or during live drone flight has not yet been verified.



\## Files

\- `weights/best.pt` — Trained gate detection model

\- `results.csv` — Training metrics

\- `results.png` — Training performance plots



\## Installation

```bash

pip install ultralytics

```



\## Run Detection

```bash

yolo detect predict model=weights/best.pt source=path/to/image.jpg imgsz=640

```



Replace `path/to/image.jpg` with an actual image path.



\## Next Steps

1\. Test the model on new racing environments.

2\. Connect YOLO to the live Gazebo camera feed.

3\. Implement gate selection and visual navigation.

4\. Connect navigation commands to PX4 using MAVSDK.



\*\*Note:\*\* YOLO detects gates but does not control drone flight directly.



