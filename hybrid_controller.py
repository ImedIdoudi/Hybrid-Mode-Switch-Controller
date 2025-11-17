
from vehicle_state import VehicleState, DriveMode
from mode_selector import ModeSelector


class HybridController:
   
    
    def __init__(self):
        self.selector = ModeSelector()
    
    def update(self, state: VehicleState):
        """Take current car state and decide what mode to use"""

        # Make sure inputs are valid
        state.validate()
        
        # Ask the selector which mode to use
        mode = self.selector.select_mode(state)
        
        # Figure out if engine should be on
        engine_on = (mode == DriveMode.ENGINE_ONLY or mode == DriveMode.HYBRID)
        
        # Return all the informations
        return {
            'mode': mode,
            'engine_on': engine_on,
            'speed': state.speed,
            'battery': state.battery_soc
        }