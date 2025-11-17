# Hybrid Mode Controller

A Python-based control system for managing hybrid vehicle drive modes.

## Project Structure

```
hybrid-controller/
│
├── vehicle_state.py       # Vehicle state data structures and enums
├── mode_selector.py       # Mode selection logic
├── hybrid_controller.py   # Main controller
├── test_scenarios.py      # Demo scenarios
├── main.py               # Entry point for running scenarios
├── test_controller.py    # Unit tests (pytest)
└── README.md            # This file
```

## Module Descriptions

### `vehicle_state.py`
Defines:
- `DriveMode` enum: The four available drive modes
- `VehicleState` dataclass: Stores vehicle parameters with validation

### `mode_selector.py`
Contains the `ModeSelector` class that implements the decision logic for selecting the optimal drive mode based on:
- Battery level
- Speed
- Throttle/brake position
- Road gradient
- Vehicle load

### `hybrid_controller.py`
The main `HybridController` class that:
- Validates input state
- Coordinates with ModeSelector
- Returns control decisions

### `test_scenarios.py`
Contains 8 predefined test scenarios demonstrating different driving conditions:
1. City Driving
2. Highway Cruise
3. Hard Acceleration
4. Mountain Road
5. Traffic Braking
6. Low Battery Alert
7. Downhill Drive
8. Moving Day (Heavy Load)

### `test_controller.py`
Comprehensive unit tests using pytest framework, organized into test classes:
- `TestDriveModes`: Tests for each drive mode
- `TestBatteryAndValidation`: Battery-related scenarios and Input validation tests


## Installation

No external dependencies required for basic functionality. For testing:

```bash
pip install pytest
```

## Usage

### Run Demo Scenarios

```bash
python main.py
```

This will execute all 8 test scenarios and display the selected drive mode for each.

### Run Unit Tests

```bash
# Run all tests with verbose output
python -m pytest test_controller.py -v

# Run specific test class
python -m pytest test_controller.py::TestDriveModes -v

# Run with coverage
python -m pytest test_controller.py --cov=. --cov-report=html
```

### Use in Your Code

```python
from vehicle_state import VehicleState
from hybrid_controller import HybridController

# Create controller
controller = HybridController()

# Define vehicle state
state = VehicleState(
    speed=50,
    throttle_position=40,
    brake_position=0,
    battery_soc=60,
    load=1300,
    gradient=0
)

# Get control decision
result = controller.update(state)
print(f"Mode: {result['mode'].value}")
print(f"Engine: {'ON' if result['engine_on'] else 'OFF'}")
```

## Drive Mode Selection Logic

The controller prioritizes modes in the following order:

1. **Regenerative Braking** - When braking or descending steep hills
2. **Engine Only** - When battery is critically low
3. **Hybrid** - When maximum power is needed (acceleration, steep hills, heavy load)
4. **Electric Only** - When conditions are optimal (low speed, light throttle, good battery)
5. **Engine Only** - For efficient highway cruising
6. **Hybrid** - Default fallback mode

## Configuration Parameters

Configurable thresholds in `ModeSelector`:

```python
LOW_BATTERY = 20.0         # Battery threshold for engine mode
HIGH_BATTERY = 80.0        # Battery threshold for electric preference
EV_SPEED_LIMIT = 50.0      # Max speed for electric-only mode (km/h)
HIGHWAY_SPEED = 80.0       # Speed for highway engine mode (km/h)
HEAVY_LOAD = 1500.0        # Load threshold (kg)
STEEP_HILL = 5.0           # Uphill gradient threshold (degrees)
STEEP_DOWN = -3.0          # Downhill gradient threshold (degrees)
```

## Testing

The test suite includes:
- ✅ 15+ unit tests covering all drive modes
- ✅ Input validation tests
- ✅ Edge case handling
- ✅ Boundary condition tests
- ✅ Integration tests with realistic scenarios

## License

Educational project for System Integration course.

## Author

Imed Idoudi
