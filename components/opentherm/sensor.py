from typing import Any, Dict

import esphome.config_validation as cv
from esphome.components import sensor

from . import schema, validate, generate, CONF_OPENTHERM_ID, OpenthermHub

DEPENDENCIES = [ "opentherm" ]
COMPONENT_TYPE = "sensor"

def get_entity_validation_schema(entity: schema.SensorSchema) -> cv.Schema:
    return sensor.sensor_schema(
        unit_of_measurement = entity["unit_of_measurement"] if "unit_of_measurement" in entity else sensor._UNDEF,
        accuracy_decimals = entity["accuracy_decimals"],
        device_class=entity["device_class"] if "device_class" in entity else sensor._UNDEF,
        icon = entity["icon"] ,#if "icon" in entity else sensor._UNDEF,
        state_class = entity["state_class"]
    )

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(validate.create_validation_schema(schema.SENSORS, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

async def to_code(config: Dict[str, Any]) -> None:
    await generate.generic_to_code(
        COMPONENT_TYPE, 
        sensor.Sensor, 
        lambda _, conf: sensor.new_sensor(conf), 
        config
    )
