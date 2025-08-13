#ifndef ENGINE_H
#define ENGINE_H
#include <stdint.h>
extern uint8_t engine_state;
void engine_init(void);
void engine_update(uint8_t ignition_switch);
#endif
