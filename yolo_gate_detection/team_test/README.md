# YOLO gate detection for Windows

This folder runs inference on an image, video, or webcam using the CPU. It works independently of PX4, Gazebo, ROS 2, and the drone simulation. The trained YOLO11 checkpoint (`best.pt`) and a sample image are included.

## Get the package

With Git for Windows installed, run these commands in PowerShell from the folder where you want the repository. If you already have an up-to-date checkout of `main`, open its `yolo_gate_detection\team_test` folder instead.

```powershell
git clone --branch main https://github.com/Maria0Mamdooh/autonomous-drone-racing.git
Set-Location .\autonomous-drone-racing\yolo_gate_detection\team_test
Get-FileHash -LiteralPath .\best.pt -Algorithm SHA256
```

The expected SHA-256 is `c8c3b258d35bb5e93c294254ae2cafc334a09eae0eec9d28104a1f0b87e790f8`.

## Install on Windows

Install 64-bit Python 3.12 with the Windows Python launcher, then open PowerShell in this folder. These commands use a local virtual environment and the CPU builds of PyTorch and TorchVision.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Ultralytics installs the remaining runtime libraries, including OpenCV. [PyTorch installation reference](https://pytorch.org/get-started/locally/)

## Test

Save detections on the bundled held-out image from the `new_arena_full` gate dataset.

```powershell
.\.venv\Scripts\python.exe infer.py --source sample_gate.png --save
```

A successful run prints the loaded checkpoint and class names, reports one processed frame and the detection count, and writes an annotated image to a new `outputs\predict-*` folder under your current directory. The Linux CPU smoke test returned five gate detections at the default confidence threshold of 0.25. Open the saved image to inspect the boxes. A count of zero means the model returned zero boxes at the selected confidence threshold.

To preview an image, annotate a video, or preview the default webcam, run the matching command.

```powershell
.\.venv\Scripts\python.exe infer.py --source "C:\Videos\gate.jpg" --show
.\.venv\Scripts\python.exe infer.py --source "C:\Videos\gate.mp4" --save
.\.venv\Scripts\python.exe infer.py --webcam 0 --show
```

Press **Q** or **Esc** in the preview to stop, or **Ctrl+C** in PowerShell. Combine `--show` and `--save` to preview and save in the same run. Use `--conf 0.15` to test a lower threshold or `--weights "C:\path\to\best.pt"` to load a checkpoint from another folder. If the webcam fails to open, check Windows camera permissions and close other apps using the camera. [Ultralytics prediction reference](https://docs.ultralytics.com/modes/predict/)
