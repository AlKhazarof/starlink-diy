# Control Electronics

This directory contains schematics, PCB designs, and documentation for control electronics.

## Overview

The control electronics system manages:
- Motor control for tracking
- RF signal processing
- Sensor interfacing
- Communication with ground station software
- Power management

## System Architecture

```
┌─────────────────────────────────────────────┐
│         Main Controller (MCU)               │
│  - Command processing                       │
│  - Position calculation                     │
│  - Motor control logic                      │
│  - Sensor reading                           │
└─────────────────────────────────────────────┘
         ↓              ↓              ↓
    ┌────────┐    ┌──────────┐   ┌─────────┐
    │ Motor  │    │    RF    │   │ Sensors │
    │ Drivers│    │ Frontend │   │         │
    └────────┘    └──────────┘   └─────────┘
```

## Main Components

### 1. Main Controller
- **Microcontroller**: Arduino, STM32, or ESP32
- **Responsibilities**:
  - Serial communication
  - Motor control algorithms
  - Position tracking
  - Safety monitoring

### 2. Motor Drivers
- **Stepper Motor Drivers**: A4988, DRV8825, or TMC2209
- **Features**:
  - Microstepping
  - Current limiting
  - Fault detection

### 3. Position Sensors
- **Encoders**: Absolute or incremental
- **Limit Switches**: Home and end positions
- **Potentiometers**: Analog position feedback

### 4. RF Frontend (Optional)
- **LNB**: Low Noise Block converter
- **Power Supply**: Voltage regulation for LNB
- **Signal Interface**: F-connector or SMA

### 5. Power System
- **Main Supply**: 12-24V DC
- **Regulation**: 5V and 3.3V for logic
- **Protection**: Fuses, reverse polarity protection
- **Backup**: Optional battery backup

## Schematics

### Available Designs
- `controller-basic/` - Simple Arduino-based controller
- `controller-advanced/` - Advanced STM32-based system
- `motor-driver/` - Motor driver interface board
- `sensor-board/` - Sensor interface board
- `power-supply/` - Power distribution board

## PCB Designs

PCB designs available in KiCad format:
- 2-layer designs for home etching
- 4-layer designs for professional fabrication
- Gerber files included

## Bill of Materials

### Basic Controller (~$100)
- Arduino Mega 2560: $15
- 2× A4988 Stepper drivers: $10
- Position sensors: $20
- Power supply (12V, 5A): $15
- Connectors and components: $20
- PCB: $20

### Advanced Controller (~$200)
- STM32F4 Development board: $25
- 2× TMC2209 Stepper drivers: $20
- Absolute encoders: $60
- Professional power supply: $30
- Higher quality components: $40
- Professional PCB: $25

## Firmware

Firmware source code available in:
- `/software/firmware/`

Features:
- Position control
- Serial command interface
- Safety monitoring
- Error handling

See [Firmware Documentation](../../docs/software/README.md)

## Assembly Instructions

1. **PCB Assembly**
   - Solder components following BOM
   - Test power supply voltages
   - Verify continuity

2. **Motor Connection**
   - Connect stepper motors
   - Configure current limit
   - Test motor operation

3. **Sensor Integration**
   - Install position sensors
   - Calibrate sensors
   - Test feedback

4. **System Integration**
   - Connect to antenna mount
   - Cable management
   - Weatherproofing

## Testing Procedures

### Power-On Tests
1. Measure all supply voltages
2. Check for shorts
3. Verify polarity

### Functional Tests
1. Serial communication
2. Motor operation (both axes)
3. Sensor reading
4. Limit switch operation
5. Emergency stop

### Integration Tests
1. Command interface
2. Position accuracy
3. Tracking performance
4. Error handling

## Calibration

### Motor Calibration
1. Home to reference position
2. Move to known angles
3. Verify position accuracy
4. Adjust steps-per-degree if needed

### Sensor Calibration
1. Zero position calibration
2. Full range verification
3. Linearity check

## Troubleshooting

### Common Issues

**Motors not moving**:
- Check power supply
- Verify motor connections
- Check driver enable pin
- Test with simple code

**Position errors**:
- Calibrate sensors
- Check for mechanical backlash
- Verify steps-per-degree setting

**Communication issues**:
- Verify baud rate
- Check TX/RX connections
- Test with loopback

## Safety Features

### Hardware Protection
- Fuses on power inputs
- Reverse polarity protection
- Overvoltage protection
- Current limiting

### Software Safety
- Position limits enforcement
- Watchdog timer
- Emergency stop function
- Error detection and reporting

## Contributing

Contribute improvements:
- Circuit optimizations
- PCB layout improvements
- New features
- Bug fixes
- Documentation

See [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Resources

- KiCad project files
- Gerber files for fabrication
- BOM spreadsheets
- Assembly diagrams
- Test procedures

## Support

For questions and discussions:
- Open an issue on GitHub
- Check existing documentation
- Join community forums
