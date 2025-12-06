# Software Architecture

This directory contains documentation for the software components of the Starlink DIY project.

## 🏗️ Architecture Overview

The Starlink DIY software stack consists of three main layers:

```
┌─────────────────────────────────────────┐
│     Application Layer (Ground Station)  │
│  - User Interface                       │
│  - Configuration Management             │
│  - Monitoring & Logging                 │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     Control Layer (Utilities)           │
│  - Satellite Tracking                   │
│  - Signal Processing                    │
│  - Connection Management                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     Hardware Layer (Firmware)           │
│  - Motor Control                        │
│  - RF Control                           │
│  - Sensor Reading                       │
└─────────────────────────────────────────┘
```

## 📦 Components

### 1. Firmware (Embedded)
Low-level control software running on microcontrollers.

**Key Features:**
- Real-time motor control for tracking
- RF power management
- Sensor data acquisition
- Communication protocol handling

**Technologies:**
- C/C++ for embedded systems
- Real-time operating system (RTOS)
- Hardware abstraction layer (HAL)

**Files**: See [/software/firmware](../../software/firmware/)

### 2. Ground Station (Desktop/Server)
Main application for managing the satellite link.

**Key Features:**
- User interface (GUI/CLI)
- Configuration management
- Connection monitoring
- Data logging and analysis
- Remote access capabilities

**Technologies:**
- Python for core application
- Web-based UI (HTML/CSS/JavaScript)
- Database for logging (SQLite)
- REST API for remote control

**Files**: See [/software/ground-station](../../software/ground-station/)

### 3. Utilities (Tools & Libraries)
Supporting tools and libraries for various tasks.

**Key Features:**
- Satellite orbit calculation (TLE processing)
- Doppler shift correction
- Antenna pointing calculator
- Signal strength analyzer
- Configuration validators

**Technologies:**
- Python for scripting
- NumPy/SciPy for calculations
- Matplotlib for visualization

**Files**: See [/software/utilities](../../software/utilities/)

## 🔄 Data Flow

```
Satellite Ephemeris → Tracking Calculator → Pointing Commands
                                ↓
User Configuration → Ground Station → Control Commands → Firmware
                                ↓                           ↓
                        Telemetry ← ─ ─ ─ ─ ─ ─ ─ ─ ─ ← RF Hardware
```

## 🚀 Getting Started

### Development Environment Setup

1. **Install Prerequisites**:
```bash
# Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Embedded toolchain (for firmware)
# Install ARM GCC toolchain or appropriate compiler
```

2. **Clone Repository**:
```bash
git clone https://github.com/AlKhazarof/starlink-diy.git
cd starlink-diy
```

3. **Build Firmware** (if applicable):
```bash
cd software/firmware
make clean && make
```

4. **Run Ground Station**:
```bash
cd software/ground-station
python main.py
```

## 📖 Key Algorithms

### Satellite Tracking
The system uses Two-Line Element (TLE) sets to calculate satellite positions:

1. Parse TLE data
2. Calculate satellite position using SGP4/SDP4 models
3. Convert to local azimuth/elevation coordinates
4. Apply Doppler correction
5. Generate pointing commands

### Signal Processing
Key signal processing tasks:

1. **Doppler Correction**: Compensate for relative motion
2. **Beam Steering**: Point antenna electronically or mechanically
3. **Signal Detection**: Lock onto satellite signal
4. **Quality Monitoring**: Track SNR, BER, packet loss

## 🔧 API Reference

### Ground Station API

```python
# Example: Initialize tracking
from ground_station import SatelliteTracker

tracker = SatelliteTracker()
tracker.load_tle("starlink.tle")
position = tracker.calculate_position(satellite_id, timestamp)
```

### Firmware API

```c
// Example: Control antenna pointing
void set_antenna_position(float azimuth, float elevation) {
    // Implementation
}
```

## 🧪 Testing

### Unit Tests
```bash
# Run Python unit tests
pytest tests/

# Run firmware tests
cd software/firmware/tests
make test
```

### Integration Tests
```bash
# Test complete system
python tests/integration/test_full_system.py
```

### Simulation
Use simulator mode for testing without hardware:
```bash
python ground_station/main.py --simulate
```

## 📊 Performance Considerations

### Real-Time Requirements
- Tracking update rate: 1-10 Hz
- Command latency: < 100ms
- Signal processing: Real-time

### Resource Usage
- CPU: Moderate (tracking calculations)
- Memory: < 1GB for ground station
- Storage: Minimal (logs and configuration)
- Network: Variable (satellite throughput)

## 🔒 Security Considerations

1. **Authentication**: Secure access to control interface
2. **Encryption**: Protect sensitive configuration
3. **Input Validation**: Prevent command injection
4. **Secure Updates**: Verify firmware authenticity

## 📝 Configuration

Example configuration file:
```yaml
# config.yaml
station:
  latitude: 45.0
  longitude: -93.0
  elevation: 300

antenna:
  type: "parabolic"
  diameter: 0.6
  gain: 35

tracking:
  update_rate: 5
  min_elevation: 25
```

## 🐛 Debugging

### Common Issues

**Tracking Errors:**
- Verify TLE data is current
- Check time synchronization (NTP)
- Validate observer location

**Communication Failures:**
- Check serial port connections
- Verify baud rate settings
- Test with loopback

**Performance Issues:**
- Profile code with Python profiler
- Monitor CPU/memory usage
- Optimize hot paths

## 📚 Dependencies

### Python Packages
- `numpy`: Numerical computations
- `scipy`: Scientific algorithms
- `pyorbital`: Satellite orbit calculations
- `pyserial`: Serial communication
- `flask`: Web interface

### Firmware Libraries
- FreeRTOS: Real-time operating system
- HAL: Hardware abstraction
- CMSIS: Cortex microcontroller software

## 🤝 Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

Areas needing contributions:
- Performance optimization
- Additional satellite models
- UI/UX improvements
- Documentation
- Testing coverage

---

**Note**: This software is experimental. Use at your own risk and ensure compliance with all applicable regulations.
