
from vehicle_state import VehicleState
from hybrid_controller import HybridController


def run_scenario(controller, name, state):
    """Run one test scenario and print results"""
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    print(f"Speed: {state.speed} km/h")
    print(f"Throttle: {state.throttle_position}%")
    print(f"Brake: {state.brake_position}%")
    print(f"Battery: {state.battery_soc}%")
    print(f"Load: {state.load} kg")
    print(f"Road: {state.gradient}° {'(uphill)' if state.gradient > 0 else '(downhill)' if state.gradient < 0 else '(flat)'}")
    
    result = controller.update(state)
    
    print(f"\n→ Selected Mode: {result['mode'].value}")
    print(f"→ Engine: {'ON' if result['engine_on'] else 'OFF'}")
    print()

def run_all_scenarios():
    """Run all the test scenarios"""
    controller = HybridController()
    
    scenarios = [
        (
            "City Driving, Light Load, Good Battery",
            VehicleState(speed=35, throttle_position=25, brake_position=0,
                    battery_soc=75, load=1200, gradient=0)
        )
        ,
        (
            "Highway Driving, Heavy Load, Low Battery",
            VehicleState(speed=110, throttle_position=45, brake_position=0,
                    battery_soc=60, load=1300, gradient=0)
        )
        ,
        (
            " Full acceleration",
            VehicleState(speed=50, throttle_position=95, brake_position=0,
                    battery_soc=65, load=1250, gradient=0)
        )
        ,
        (
            "Climbing steep hill",
            VehicleState(speed=45, throttle_position=60, brake_position=0,
                    battery_soc=55, load=1400, gradient=8)
        )
        ,
        (
            "Braking in traffic",
            VehicleState(speed=40, throttle_position=0, brake_position=70,
                    battery_soc=50, load=1200, gradient=0)
        )
        ,
        (
            "Low Battery Alert", 
            VehicleState(
            speed=50, throttle_position=40, brake_position=0,
                    battery_soc=15, load=1200, gradient=0)
        ),
        (
            "Downhill Drive", 
            VehicleState(
            speed=55, throttle_position=0, brake_position=0,
                    battery_soc=60, load=1300, gradient=-6)
        ),
        (
            "Moving Day (Heavy Load)", 
            VehicleState(
            speed=60, throttle_position=50, brake_position=0,
                    battery_soc=70, load=2200, gradient=0)
        )
    ]
    
    for name, state in scenarios:
        run_scenario(controller, name, state)

    print("="*60)
    print("All tests completed!")
    print("="*60)