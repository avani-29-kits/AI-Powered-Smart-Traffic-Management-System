"""
Traffic Light Control Module
Author: Avani Mitra (URK24CS1090)
"""

class TrafficLightController:
    """Controls traffic light timings based on congestion levels"""
    
    # Constants for traffic light states
    STATE_GREEN = "GREEN"
    STATE_YELLOW = "YELLOW"
    STATE_RED = "RED"
    
    def __init__(self):
        """Initialize traffic light controller with default timings"""
        self.current_state = self.STATE_GREEN
        self.is_active = False
        self.cycle_count = 0
        
        # Base timings (in seconds)
        self.base_green = 25
        self.base_yellow = 3
        self.base_red = 25
        
        # Current timings
        self.green_time = self.base_green
        self.yellow_time = self.base_yellow
        self.red_time = self.base_red
    
    def calculate_timings(self, congestion_level):
        """
        Calculate optimal traffic light timings based on congestion
        
        Args:
            congestion_level (float): Predicted congestion (0-100)
        
        Returns:
            dict: Timing configuration
        """
        if congestion_level >= 80:
            # Critical congestion - Maximum green
            green = 50
            yellow = 3
            red = 15
            action = "🟢 EXTENDED GREEN (50s) - Critical"
            status = "CRITICAL"
            priority = 1
            
        elif congestion_level >= 60:
            # High congestion - Extended green
            green = 40
            yellow = 3
            red = 20
            action = "🟢 EXTENDED GREEN (40s) - High"
            status = "HIGH"
            priority = 2
            
        elif congestion_level >= 40:
            # Medium congestion - Normal timing
            green = 30
            yellow = 3
            red = 25
            action = "🟡 NORMAL GREEN (30s) - Medium"
            status = "MEDIUM"
            priority = 3
            
        elif congestion_level >= 20:
            # Low congestion - Reduced green
            green = 20
            yellow = 3
            red = 35
            action = "🟢 REDUCED GREEN (20s) - Low"
            status = "LOW"
            priority = 4
            
        else:
            # Very low congestion - Minimum green
            green = 15
            yellow = 3
            red = 45
            action = "🟢 MINIMUM GREEN (15s) - Very Low"
            status = "VERY LOW"
            priority = 5
        
        # Store current timings
        self.green_time = green
        self.yellow_time = yellow
        self.red_time = red
        
        return {
            'green_time': green,
            'yellow_time': yellow,
            'red_time': red,
            'action': action,
            'status': status,
            'priority': priority,
            'cycle_time': green + yellow + red,
            'timestamp': None  # Will be set by caller
        }
    
    def get_optimal_cycle(self, congestion_level):
        """
        Get optimal traffic light cycle for given congestion
        
        Args:
            congestion_level (float): Predicted congestion (0-100)
        
        Returns:
            tuple: (green_time, yellow_time, red_time)
        """
        timings = self.calculate_timings(congestion_level)
        return (
            timings['green_time'],
            timings['yellow_time'],
            timings['red_time']
        )
    
    def get_state_timing(self, state):
        """Get timing for a specific state"""
        if state == self.STATE_GREEN:
            return self.green_time
        elif state == self.STATE_YELLOW:
            return self.yellow_time
        elif state == self.STATE_RED:
            return self.red_time
        else:
            return 0
    
    def simulate_cycle(self, congestion_level):
        """
        Simulate a complete traffic light cycle
        
        Args:
            congestion_level (float): Predicted congestion (0-100)
        
        Yields:
            str: Current state and time remaining
        """
        timings = self.calculate_timings(congestion_level)
        
        self.cycle_count += 1
        
        # Green light
        self.current_state = self.STATE_GREEN
        yield f"🟢 GREEN: {timings['green_time']}s remaining"
        
        # Yellow light
        self.current_state = self.STATE_YELLOW
        yield f"🟡 YELLOW: {timings['yellow_time']}s remaining"
        
        # Red light
        self.current_state = self.STATE_RED
        yield f"🔴 RED: {timings['red_time']}s remaining"
        
        # Cycle complete
        yield f"✅ Cycle {self.cycle_count} complete"
    
    def get_recommendation(self, congestion_level):
        """
        Get human-readable recommendation
        
        Args:
            congestion_level (float): Predicted congestion (0-100)
        
        Returns:
            str: Recommendation text
        """
        if congestion_level >= 80:
            return "🔴 EXTREME: Consider alternative routes or public transport"
        elif congestion_level >= 60:
            return "🟠 HIGH: Allow extra travel time"
        elif congestion_level >= 40:
            return "🟡 MODERATE: Normal traffic conditions"
        elif congestion_level >= 20:
            return "🟢 LOW: Good traffic conditions"
        else:
            return "✅ EXCELLENT: Very smooth traffic flow"
    
    def reset_timings(self):
        """Reset to default timings"""
        self.green_time = self.base_green
        self.yellow_time = self.base_yellow
        self.red_time = self.base_red


# ============================================
# UNIT TESTING
# ============================================

def test_controller():
    """Test the traffic light controller"""
    print("=" * 50)
    print("🧪 Testing Traffic Light Controller")
    print("=" * 50)
    
    controller = TrafficLightController()
    
    test_congestion_levels = [90, 70, 50, 30, 10]
    
    print("\n🚦 Traffic Light Timings:")
    print("-" * 60)
    print(f"{'Congestion':>12} | {'Green':>8} | {'Yellow':>8} | {'Red':>8} | {'Cycle':>10}")
    print("-" * 60)
    
    for congestion in test_congestion_levels:
        timings = controller.calculate_timings(congestion)
        print(
            f"{congestion:>11.1f}% | "
            f"{timings['green_time']:>8}s | "
            f"{timings['yellow_time']:>8}s | "
            f"{timings['red_time']:>8}s | "
            f"{timings['cycle_time']:>10}s"
        )
    
    print("-" * 60)
    print(f"\n💡 Recommendations:")
    
    for congestion in test_congestion_levels:
        print(f"  {congestion:>11.1f}% → {controller.get_recommendation(congestion)}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_controller()