# Antenna Design Guide

## Overview

This guide covers the design and construction of antennas for satellite communication systems. We focus on practical, DIY-friendly designs suitable for home builders.

## Antenna Types

### 1. Parabolic Dish Antenna

#### Description
A parabolic reflector antenna focuses radio waves to a single point (feed).

#### Advantages
- High gain (30-40 dBi achievable)
- Simple design principle
- Well-understood technology
- Cost-effective for single beam

#### Disadvantages
- Requires mechanical tracking
- Wind loading considerations
- Precise surface accuracy needed
- Single beam at a time

#### Design Parameters

**Frequency**: Ku-band (12-18 GHz) is most common
- Downlink: 10.7-12.75 GHz
- Uplink: 14.0-14.5 GHz

**Diameter**: 
- 60 cm (minimum for basic operation)
- 90 cm (better performance)
- 120 cm (optimal for most applications)

**F/D Ratio**: 0.3-0.4 typical
- F = focal length
- D = dish diameter
- Lower F/D = shorter focal length, wider feed pattern

**Surface Accuracy**: λ/16 RMS or better
- At 12 GHz: λ = 25 mm
- Required accuracy: < 1.6 mm RMS

#### Materials

**Reflector**:
- Aluminum sheet (1-2 mm thick)
- Fiberglass with metal coating
- 3D printed sections with metal coating
- Mesh for lower frequencies

**Feed Horn**:
- Copper or brass tube
- Waveguide components
- LNB (Low Noise Block converter) - commercial option

**Mount**:
- Steel or aluminum tubing
- Bearings for smooth rotation
- Weather-resistant hardware

#### Construction Steps

1. **Pattern Development**
   - Calculate parabola profile: z = r²/(4f)
   - Create template segments
   - Mark cutting lines

2. **Reflector Forming**
   - Cut material to size
   - Form parabolic shape (stamping, spinning, or molding)
   - Check surface accuracy

3. **Feed Horn Design**
   - Calculate horn dimensions for optimal illumination
   - Typical: 10-15 dB edge taper
   - Construct or purchase LNB

4. **Mount Assembly**
   - Azimuth bearing base
   - Elevation pivot
   - Motor mounts
   - Cable routing

5. **Testing & Alignment**
   - Sun tracking for initial alignment
   - Signal strength optimization
   - Pattern measurement if possible

### 2. Phased Array Antenna

#### Description
An array of small antennas with electronic phase control to steer the beam.

#### Advantages
- Electronic steering (fast)
- No moving parts
- Multiple simultaneous beams possible
- Weather resistant (flat panel)

#### Disadvantages
- Complex RF design
- Higher component cost
- Requires many elements
- Thermal management

#### Design Parameters

**Array Size**: 
- Minimum 64 elements (8x8)
- Typical 256 elements (16x16)
- Professional systems: 1000+ elements

**Element Spacing**: 
- 0.5λ to 0.7λ typical
- At 12 GHz: 12.5-17.5 mm

**Phase Shifters**:
- 3-bit minimum (45° steps)
- 5-bit better (11.25° steps)
- Analog phase shifters optimal

**Gain Calculation**:
- Array gain = Element gain + 10*log10(N*η)
- N = number of elements
- η = array efficiency (0.5-0.7 typical)

#### Construction Approach

**For Makers**:
A full phased array is very complex. Consider:
1. Start with smaller array (8 elements)
2. Use commercial phase shifter ICs
3. Focus on proof of concept
4. Incremental expansion

**Professional Development**:
1. RF simulation (CST, HFSS)
2. PCB design with controlled impedance
3. Calibration system
4. Thermal analysis

### 3. Helical Antenna

#### Description
A helical coil antenna providing circular polarization.

#### Advantages
- Circular polarization (matches satellite signals)
- Moderate gain (12-18 dBi)
- Relatively simple construction
- Good bandwidth

#### Disadvantages
- Larger than dish for same gain
- Requires ground plane
- Fixed polarization sense

#### Design Formulas

**For axial mode (end-fire)**:
- Circumference C = λ (approximately)
- Spacing S = λ/4
- Number of turns N = 5-15
- Diameter D = λ/(2π)

**Gain**: G ≈ 15N*C²*S/λ³

#### Construction
1. Form helix from copper wire or tubing
2. Create ground plane (1λ diameter minimum)
3. Mount feed point at center
4. Weatherproof assembly

## Feed Systems

### LNB (Low Noise Block Converter)
- Commercial solution
- Converts Ku-band to L-band (950-2150 MHz)
- Low noise figure (< 0.7 dB typical)
- Cost-effective

### Custom Feed Horn
- Optimized performance
- Specific frequency bands
- Learning opportunity
- More complex

## Testing Equipment

### Minimum:
- Satellite finder (signal strength meter)
- Compass and inclinometer
- Multimeter

### Recommended:
- Spectrum analyzer
- Signal generator
- Return loss bridge
- Sun noise measurement

### Professional:
- Network analyzer
- Antenna pattern measurement system
- Near-field scanner

## Performance Optimization

### Alignment
1. Rough alignment using compass/GPS
2. Fine adjustment for maximum signal
3. Polarization optimization
4. Peak and null verification

### Signal Quality
- Monitor Eb/No or SNR
- Check for interference
- Verify polarization match
- Measure return loss

### Troubleshooting
- Low signal: Check alignment, LNB power, cables
- High noise: Check for interference, LNB performance
- Intermittent: Check connections, weather sealing
- No signal: Verify frequency, satellite, line-of-sight

## Safety Considerations

⚠️ **Important Safety Notes**:

1. **RF Exposure**: 
   - Never look into active antenna
   - Maintain safe distance from transmitting antenna
   - Follow MPE guidelines

2. **Installation**:
   - Secure mounting for wind loads
   - Proper grounding for lightning protection
   - Height safety when installing

3. **Legal**:
   - Check local regulations
   - Obtain necessary licenses
   - Respect frequency allocations

## Bill of Materials

### Parabolic Dish (90cm)
- Aluminum sheet: $50-100
- Feed horn/LNB: $30-80
- Mount hardware: $50-150
- Motors and controller: $100-300
- Cables and connectors: $50-100
- **Total**: $280-730

### Small Phased Array (8 elements)
- Antenna elements: $50-100
- Phase shifter ICs: $200-400
- RF PCB: $100-200
- Control electronics: $100-200
- Power supply: $50-100
- **Total**: $500-1000

## Resources

- **Antenna Design Books**: 
  - "Antenna Theory" by Balanis
  - "Satellite Communications" by Pratt
  
- **Online Tools**:
  - Antenna calculators
  - Parabola profile generators
  - Link budget calculators

- **Communities**:
  - Amateur radio clubs
  - Satellite enthusiast forums
  - Maker spaces

## Next Steps

1. Choose antenna type based on requirements and skills
2. Review safety and legal documentation
3. Gather materials and tools
4. Build prototype
5. Test and iterate
6. Document your results!

---

*This is a living document. Contributions and improvements welcome!*
