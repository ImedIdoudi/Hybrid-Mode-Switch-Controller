
from vehicle_state import VehicleState, DriveMode


class ModeSelector:
    """
    This is the brain of our system - it decides which mode to use
    """
    
    def __init__(self):
        # Battery limits
        self.LOW_BATTERY = 20.0      # Below this, we need the engine
        self.HIGH_BATTERY = 80.0     # Above this, use electric more
        
        # Speed limits
        self.EV_SPEED_LIMIT = 50.0   # Max speed for electric only (km/h)
        self.HIGHWAY_SPEED = 80.0    # Above this, engine is better
        
        # Environment limits
        self.HEAVY_LOAD = 1500.0     # Heavy car (kg)
        self.STEEP_HILL = 5.0        # Steep uphill (degrees)
        self.STEEP_DOWN = -3.0       # Steep downhill (degrees)
    
    def select_mode(self, state: VehicleState):
        """
        Look at the car's state and pick the best mode
        We check things in order of priority
        """
        
        # First priority: braking? Use regen!
        if self._should_use_regen(state):
            return DriveMode.REGEN
        
        # Second priority: Battery almost dead? Must use engine
        if state.battery_soc < self.LOW_BATTERY:
            return DriveMode.ENGINE_ONLY
        
        # Third priority: Need lots of power? Use both
        if self._need_max_power(state):
            return DriveMode.HYBRID
        
        # Fourth priority: Good conditions for electric?
        if self._can_go_electric(state):
            return DriveMode.ELECTRIC_ONLY
        
        # Fifth priority: Highway driving? Engine is efficient
        if self._prefer_engine(state):
            return DriveMode.ENGINE_ONLY
        
        # Default: Use hybrid - it's safe
        return DriveMode.HYBRID
    
    def _should_use_regen(self, state):
        """Check if we should use regenerative braking"""
        # We're braking and moving
        braking = state.brake_position > 10 and state.speed > 5
        # Or going downhill fast
        downhill = state.gradient < self.STEEP_DOWN and state.speed > 5
        # And battery isn't full
        battery_ok = state.battery_soc < 90
        
        return (braking or downhill) and battery_ok
    
    def _can_go_electric(self, state):
        """Check if conditions are good for electric only"""
        # Not too fast
        speed_ok = state.speed < self.EV_SPEED_LIMIT
        # Not pressing gas too hard
        gentle = state.throttle_position < 30
        # Battery has enough charge
        battery_ok = state.battery_soc > 30
        # Not going uphill
        flat_road = state.gradient < 3
        # Car isn't too heavy
        light = state.load < self.HEAVY_LOAD
        
        return speed_ok and gentle and battery_ok and flat_road and light
    
    def _prefer_engine(self, state):
        """Check if engine is better right now"""
        # Cruising on highway
        highway = state.speed > self.HIGHWAY_SPEED and state.throttle_position < 60
        return highway
    
    def _need_max_power(self, state):
        """Check if we need both engine and motor"""
        # Flooring the gas pedal
        full_throttle = state.throttle_position > 70
        # Climbing a steep hill
        steep = state.gradient > self.STEEP_HILL
        # Car is really heavy
        heavy = state.load > self.HEAVY_LOAD
        
        return full_throttle or steep or heavy