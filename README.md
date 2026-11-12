# autonomous-drone-racing

## 📡 Vision-to-Control Data Interface
To ensure seamless, decoupled integration between the **Computer Vision module (`vision/`)** and the **Flight Control module (`control/`)**, detected gate data from each camera frame is passed as a standard Python dictionary (`dict`) following the schema below:

### Expected Payload Schema

```json
{
  "detected": true,
  "error_x": 0.15,
  "error_y": -0.08,
  "gate_size": 0.24
}
