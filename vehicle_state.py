
from dataclasses import dataclass
from enum import Enum



class DriveMode(Enum):
    """The different modes our hybrid car can use"""

    ELECTRIC_ONLY = "Electric Only"
    ENGINE_ONLY = "Engine Only"
    HYBRID = "Hybrid"
    REGEN = "Regenerative Braking"

@dataclass
class VehicleState:
    """Stores all the info about what the car is doing right now"""
    
    speed: float                    # How fast tha car is going (km/h)
    throttle_position: float        # How much gas pedal is pressed (0-100%)
    brake_position: float           # How much brake is pressed (0-100%)
    battery_soc: float              # Battery percentage (0-100%)
    load: float                     # How heavy the car is (kg)
    gradient: float                 # How steep the road is (degrees, + is uphill)
    current_mode: DriveMode = DriveMode.ELECTRIC_ONLY
    
    def validate(self):
        """Make sure all the values make sense"""
        if self.battery_soc < 0 or self.battery_soc > 100:
            raise ValueError(f"Battery can't be {self.battery_soc}%")
        
        if self.speed < 0:
            raise ValueError(f"Speed can't be negative: {self.speed}")
        
        if self.throttle_position < 0 or self.throttle_position > 100:
            raise ValueError(f"Throttle must be 0-100%, not {self.throttle_position}")
        
        if self.brake_position < 0 or self.brake_position > 100:
            raise ValueError(f"Brake must be 0-100%, not {self.brake_position}")
        
        return True
