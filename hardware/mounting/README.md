# Mounting Systems

This directory contains designs for antenna mounting and positioning systems.

## Overview

Proper mounting is critical for:
- Structural stability
- Accurate pointing
- Weather resistance
- Safety

## Mounting Types

### Fixed Mount
For stationary installations with manual adjustment.

**Use Cases**:
- Geostationary satellites
- Fixed pointing applications
- Simple installations

### Tracking Mount (Az-El)
Azimuth-elevation tracking system with motor control.

**Use Cases**:
- LEO satellite tracking
- Automatic satellite following
- Multiple satellite access

### Portable Mount
Lightweight, portable mounting system.

**Use Cases**:
- Mobile operations
- Temporary installations
- Field testing

## Design Considerations

### Structural
- Wind loading calculations
- Material selection (aluminum, steel)
- Corrosion resistance
- Weight capacity

### Mechanical
- Bearing selection
- Motor sizing
- Gear ratios
- Backlash elimination

### Electrical
- Motor control
- Position sensors (encoders, potentiometers)
- Limit switches
- Cable management

## Components

### Common Parts
- Bearings (thrust and radial)
- Stepper or servo motors
- Motor drivers
- Position sensors
- Structural tubing
- Fasteners and hardware
- Weatherproofing materials

## Assembly Instructions

Detailed assembly guides available in:
- `fixed-mount/assembly.md`
- `tracking-mount/assembly.md`
- `portable-mount/assembly.md`

## Testing

### Structural Tests
- Load testing
- Wind resistance
- Vibration testing

### Functional Tests
- Position accuracy
- Tracking speed
- Repeatability
- Limit switch operation

## Safety

⚠️ **Important Safety Considerations**:

1. **Working at Height**
   - Use proper fall protection
   - Secure tools and components
   - Check weather conditions

2. **Structural**
   - Verify structural calculations
   - Use appropriate fasteners
   - Account for dynamic loads

3. **Electrical**
   - Ground all equipment
   - Protect cables from damage
   - Install lightning protection

See [Safety Documentation](../../docs/safety/LEGAL.md)

## Contributing

Contribute your mounting designs:
- Share CAD files
- Document your build
- Provide test results
- Improve existing designs

## Resources

- Structural calculations
- CAD files (STEP, STL formats)
- Bill of materials
- Assembly photos
