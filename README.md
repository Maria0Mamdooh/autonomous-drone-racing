# autonomous-drone-racing

## 📡 Vision-to-Control Data Interface
To ensure seamless, decoupled integration between the **Computer Vision module (`vision/`)** and the **Flight Control module (`control/`)**, detected gate data from each camera frame is passed as a standard Python dictionary (`dict`) following the schema below:

### Fields Specification

| Key | Type | Range | Technical Description |
| :--- | :--- | :--- | :--- |
| `detected` | `bool` | `True` / `False` | Indicates whether the target racing gate is currently visible within the camera frame. |
| `error_x` | `float` | `[-1.0, 1.0]` | Normalized horizontal offset of the gate center relative to the image center (`0.0` = centered, negative = left, positive = right). |
| `error_y` | `float` | `[-1.0, 1.0]` | Normalized vertical offset of the gate center relative to the image center (`0.0` = centered, negative = up, positive = down). |
| `gate_size` | `float` | `[0.0, 1.0]` | Ratio of the detected gate area to the total frame area; used as a proximity indicator and to confirm gate crossing. |

> **Note:** When `detected` is `False`, the flight controller ignores the numerical offsets and triggers a safe search behavior (hovering in place while performing a slow yaw scan).
