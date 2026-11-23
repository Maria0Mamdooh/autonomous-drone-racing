"""Run local gate detection with an Ultralytics checkpoint."""

import argparse
from contextlib import closing
from pathlib import Path
import sys
from tempfile import mkdtemp


PACKAGE_DIR = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--source", type=Path, help="Path to a local image or video")
    inputs.add_argument("--webcam", type=int, help="Camera index, usually 0")
    parser.add_argument("--weights", type=Path, default=PACKAGE_DIR / "best.pt")
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--show", action="store_true", help="Display annotated frames")
    parser.add_argument("--save", action="store_true", help="Save annotated output")
    args = parser.parse_args()

    weights = args.weights.resolve()
    if weights.suffix.lower() != ".pt" or not weights.is_file():
        parser.error(f"Local .pt checkpoint required. Check the path: {weights}")
    if not 0 <= args.conf <= 1:
        parser.error("--conf must be between 0 and 1")
    if args.source is not None:
        if not args.source.is_file():
            parser.error(f"Input file not found: {args.source}")
        source = str(args.source.resolve())
    else:
        if args.webcam < 0:
            parser.error("--webcam must be a nonnegative camera index")
        source = args.webcam

    show = args.show or not args.save
    try:
        import cv2
        from ultralytics import YOLO
        from ultralytics.data.utils import IMG_FORMATS, VID_FORMATS
    except (ImportError, OSError) as error:
        parser.exit(1, f"Could not import inference dependencies: {error}\n"
                       "Follow the installation steps in README.md.\n")

    extension = args.source.suffix.lower().lstrip(".") if args.source else None
    if extension is not None and extension not in IMG_FORMATS | VID_FORMATS:
        parser.error(f"Unsupported image or video extension: {args.source.suffix}")

    frames = 0
    boxes = 0
    output = None
    window_shown = False
    try:
        model = YOLO(str(weights))
        if model.task != "detect":
            parser.error(f"Expected an object detection checkpoint, got {model.task!r}")
        print(f"Loaded {weights.name}. Classes: {model.names}", flush=True)

        options = {}
        if args.save:
            output_root = Path.cwd() / "outputs"
            output_root.mkdir(exist_ok=True)
            output = Path(mkdtemp(prefix="predict-", dir=output_root))
            options = {"project": str(output.parent), "name": output.name, "exist_ok": True}

        results = model.predict(
            source=source, stream=True, device="cpu", imgsz=640,
            conf=args.conf, save=args.save, verbose=False, **options,
        )
        with closing(results):
            for result in results:
                frames += 1
                boxes += len(result.boxes)
                if show:
                    cv2.imshow("YOLO gate detections", result.plot())
                    window_shown = True
                    delay = 0 if extension in IMG_FORMATS else 1
                    if cv2.waitKey(delay) & 0xFF in (ord("q"), 27):
                        break
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as error:
        parser.exit(1, f"Inference failed: {error}\n")
    finally:
        if window_shown:
            cv2.destroyAllWindows()

    if not frames:
        parser.exit(1, "No frames were processed. Check the input or camera.\n")
    print(f"Processed {frames} frame(s), {boxes} detection(s) at confidence {args.conf:g}.")
    if output is not None:
        if not any(output.iterdir()):
            parser.exit(1, f"No annotated output was written to {output}\n")
        print(f"Annotated output: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
