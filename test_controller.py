
from hybrid_controller import HybridController
from vehicle_state import VehicleState, DriveMode

class TestDriveModes:
    """Unit tests for hybrid controller drive mode selection"""
    

    def test_ev_mode(self):
        """Test that electric mode works in city"""
        controller = HybridController()
        state = VehicleState(35, 25, 0, 75, 1200, 0)
        result = controller.update(state)
        assert result['mode'] == DriveMode.ELECTRIC_ONLY

    def test_engine_mode(self):
        """Test that engine mode works on highway"""
        controller = HybridController()
        state = VehicleState(110, 45, 0, 60, 1300, 0)
        result = controller.update(state)
        assert result['mode'] == DriveMode.ENGINE_ONLY

    def test_hybrid_mode(self):
        """Test that hybrid mode works when accelerating hard"""
        controller = HybridController()
        state = VehicleState(50, 95, 0, 65, 1250, 0)
        result = controller.update(state)
        assert result['mode'] == DriveMode.HYBRID

    def test_regen_mode(self):
        """Test that regen works when braking"""
        controller = HybridController()
        state = VehicleState(40, 0, 70, 50, 1200, 0)
        result = controller.update(state)
        assert result['mode'] == DriveMode.REGEN


class TestBatteryAndValidation:
    """Unit tests for battery levels and input validation"""
   

    def test_low_battery(self):
        """Test that low battery forces engine mode"""
        controller = HybridController()
        state = VehicleState(50, 40, 0, 15, 1200, 0)
        result = controller.update(state)
        assert result['mode'] == DriveMode.ENGINE_ONLY
        
    def test_invalid_battery(self):
        """Test that invalid battery raises error"""
        controller = HybridController()
        state = VehicleState(50, 40, 0, 150, 1200, 0)  # 150% battery - impossible!
        try:
            controller.update(state)
            assert False, "Should have raised error"
        except ValueError:
            assert True

    def test_steep_hill(self):
        """Test that steep hills use hybrid mode"""
        controller = HybridController()
        state = VehicleState(45, 60, 0, 55, 1400, 8)
        result = controller.update(state)
        assert result['mode'] == DriveMode.HYBRID


    def test_invalid_speed(self):
        """Test that negative speed raises error"""
        controller = HybridController()
        state = VehicleState(-50, 40, 0, 60, 1200, 0)  # negative speed - impossible!
        try:
            controller.update(state)
            assert False, "Should have raised error"
        except ValueError:
            assert True