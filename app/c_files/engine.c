#include "engine.h"
#include "../calibration/calibration.h"

uint8_t engine_state = 0;

void engine_init(void) { engine_state = 0; }

void engine_update(uint8_t ignition_switch) {
    engine_state = (ignition_switch == 1) ? 1 : 0;
}
