/*
 * Starlink DIY - Antenna Controller Firmware
 * 
 * This firmware controls the antenna positioning system for satellite tracking.
 * It receives commands via serial interface and controls stepper motors for
 * azimuth and elevation control.
 * 
 * Hardware Requirements:
 * - Microcontroller (e.g., Arduino, STM32, ESP32)
 * - Stepper motor drivers (e.g., A4988, DRV8825)
 * - Stepper motors for azimuth and elevation
 * - Position sensors (encoders or limit switches)
 * - Serial interface (USB or UART)
 * 
 * Safety Features:
 * - Position limits to prevent mechanical damage
 * - Watchdog timer for command timeout
 * - Emergency stop capability
 * - Current limiting
 */

#ifndef ANTENNA_CONTROLLER_H
#define ANTENNA_CONTROLLER_H

#include <stdint.h>
#include <stdbool.h>

// Configuration constants
#define AZIMUTH_MIN_ANGLE     0.0f      // Minimum azimuth in degrees
#define AZIMUTH_MAX_ANGLE     360.0f    // Maximum azimuth in degrees
#define ELEVATION_MIN_ANGLE   0.0f      // Minimum elevation in degrees
#define ELEVATION_MAX_ANGLE   90.0f     // Maximum elevation in degrees

#define STEPS_PER_DEGREE_AZ   100       // Steps per degree for azimuth motor
#define STEPS_PER_DEGREE_EL   100       // Steps per degree for elevation motor

#define MAX_SPEED_AZ          1000      // Maximum speed in steps/sec for azimuth
#define MAX_SPEED_EL          1000      // Maximum speed in steps/sec for elevation

#define POSITION_TOLERANCE    0.5f      // Position tolerance in degrees

#define COMMAND_TIMEOUT_MS    5000      // Command timeout in milliseconds

// Error codes
typedef enum {
    ERROR_NONE = 0,
    ERROR_INVALID_POSITION,
    ERROR_MOTOR_FAULT,
    ERROR_TIMEOUT,
    ERROR_LIMIT_SWITCH,
    ERROR_COMMUNICATION
} ErrorCode;

// Motor direction
typedef enum {
    DIRECTION_CW = 0,      // Clockwise
    DIRECTION_CCW = 1      // Counter-clockwise
} Direction;

// System state
typedef enum {
    STATE_IDLE = 0,
    STATE_MOVING,
    STATE_TRACKING,
    STATE_ERROR,
    STATE_EMERGENCY_STOP
} SystemState;

// Position structure
typedef struct {
    float azimuth;      // Current azimuth in degrees
    float elevation;    // Current elevation in degrees
    uint32_t timestamp; // Position timestamp in milliseconds
} Position;

// Command structure
typedef struct {
    float target_azimuth;    // Target azimuth in degrees
    float target_elevation;  // Target elevation in degrees
    float speed_factor;      // Speed multiplier (0.1 to 1.0)
} Command;

// Function prototypes

/**
 * Initialize the antenna controller system
 * @return true if initialization successful
 */
bool antenna_controller_init(void);

/**
 * Set target position for antenna
 * @param azimuth Target azimuth in degrees (0-360)
 * @param elevation Target elevation in degrees (0-90)
 * @return Error code
 */
ErrorCode antenna_set_position(float azimuth, float elevation);

/**
 * Get current antenna position
 * @param position Pointer to position structure to fill
 * @return Error code
 */
ErrorCode antenna_get_position(Position* position);

/**
 * Emergency stop - halt all movement immediately
 */
void antenna_emergency_stop(void);

/**
 * Home the antenna to reference position
 * @return Error code
 */
ErrorCode antenna_home(void);

/**
 * Main control loop - call regularly from main()
 */
void antenna_controller_update(void);

/**
 * Check if antenna is at target position
 * @return true if at target within tolerance
 */
bool antenna_is_at_target(void);

/**
 * Get current system state
 * @return Current state
 */
SystemState antenna_get_state(void);

/**
 * Get last error code
 * @return Last error
 */
ErrorCode antenna_get_last_error(void);

/**
 * Process serial command
 * @param command Command string
 * @return Error code
 */
ErrorCode antenna_process_command(const char* command);

#endif // ANTENNA_CONTROLLER_H

/*
 * Example usage:
 * 
 * void setup() {
 *     Serial.begin(115200);
 *     if (!antenna_controller_init()) {
 *         Serial.println("ERROR: Initialization failed");
 *         return;
 *     }
 *     Serial.println("Antenna controller initialized");
 * }
 * 
 * void loop() {
 *     // Process any incoming serial commands
 *     if (Serial.available()) {
 *         String cmd = Serial.readStringUntil('\n');
 *         ErrorCode error = antenna_process_command(cmd.c_str());
 *         if (error != ERROR_NONE) {
 *             Serial.print("ERROR: ");
 *             Serial.println(error);
 *         }
 *     }
 *     
 *     // Update controller state
 *     antenna_controller_update();
 *     
 *     // Report position periodically
 *     static unsigned long last_report = 0;
 *     if (millis() - last_report > 1000) {
 *         Position pos;
 *         if (antenna_get_position(&pos) == ERROR_NONE) {
 *             Serial.print("Position: Az=");
 *             Serial.print(pos.azimuth);
 *             Serial.print(" El=");
 *             Serial.println(pos.elevation);
 *         }
 *         last_report = millis();
 *     }
 * }
 */
