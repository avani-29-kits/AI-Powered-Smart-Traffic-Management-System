"""
Traffic Data Simulator Module
Author: Avani Mitra (URK24CS1090)
"""

import random
import time
from datetime import datetime
from collections import deque

class TrafficDataSimulator:
    """Simulates real-time traffic data"""
    
    def __init__(self):
        """Initialize the traffic data simulator"""
        self.weather_types = {
            0: {"name": "Clear", "icon": "☀️", "delay_factor": 1.0},
            1: {"name": "Rainy", "icon": "🌧️", "delay_factor": 1.3},
            2: {"name": "Foggy", "icon": "🌫️", "delay_factor": 1.5},
            3: {"name": "Snow", "icon": "❄️", "delay_factor": 1.6}
        }
        
        # Peak hour definitions
        self.peak_hours = {
            "morning": (7, 9),
            "evening": (17, 19)
        }
        
        # Store historical data
        self.history = deque(maxlen=100)
        
        # Current state
        self.current_data = None
    
    def get_vehicle_count(self, time_of_day, is_weekend=False):
        """
        Generate realistic vehicle count based on time and day
        
        Args:
            time_of_day (int): Hour of day (0-23)
            is_weekend (bool): Whether it's weekend
        
        Returns:
            int: Number of vehicles (0-100)
        """
        # Base count
        base = 40
        
        # Peak hour adjustment
        morning_peak_start, morning_peak_end = self.peak_hours["morning"]
        evening_peak_start, evening_peak_end = self.peak_hours["evening"]
        
        peak_factor = 0
        if morning_peak_start <= time_of_day <= morning_peak_end:
            peak_factor = 30
        elif evening_peak_start <= time_of_day <= evening_peak_end:
            peak_factor = 35
        
        # Weekend adjustment
        weekend_factor = -15 if is_weekend else 0
        
        # Night adjustment
        if time_of_day < 6 or time_of_day > 22:
            night_factor = -25
        else:
            night_factor = 0
        
        # Random variation
        random_variation = random.randint(-15, 15)
        
        # Calculate final count
        count = base + peak_factor + weekend_factor + night_factor + random_variation
        
        # Ensure within bounds
        return max(0, min(100, count))
    
    def get_weather_condition(self):
        """
        Generate random weather condition with realistic weights
        
        Returns:
            int: Weather condition code (0-3)
        """
        weights = [0.55, 0.30, 0.10, 0.05]  # Clear, Rainy, Foggy, Snow
        return random.choices([0, 1, 2, 3], weights=weights, k=1)[0]
    
    def get_time_of_day(self):
        """Get current time or simulate random time"""
        # 70% chance of realistic time, 30% chance of random
        if random.random() < 0.7:
            return datetime.now().hour
        else:
            return random.randint(0, 23)
    
    def get_day_type(self):
        """Check if current day is weekend"""
        # Simulate: 70% weekday, 30% weekend
        return random.random() < 0.3
    
    def generate_data(self):
        """
        Generate complete traffic data set
        
        Returns:
            dict: Complete traffic data
        """
        time_of_day = self.get_time_of_day()
        is_weekend = self.get_day_type()
        weather_code = self.get_weather_condition()
        vehicle_count = self.get_vehicle_count(time_of_day, is_weekend)
        
        weather_info = self.weather_types[weather_code]
        
        data = {
            'vehicle_count': vehicle_count,
            'time_of_day': time_of_day,
            'time_formatted': f"{time_of_day:02d}:00",
            'weather_code': weather_code,
            'weather_name': weather_info['name'],
            'weather_icon': weather_info['icon'],
            'delay_factor': weather_info['delay_factor'],
            'is_weekend': is_weekend,
            'is_peak_hour': self.is_peak_hour(time_of_day),
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in history
        self.history.append(data)
        self.current_data = data
        
        return data
    
    def is_peak_hour(self, time_of_day):
        """Check if given time is peak hour"""
        morning_start, morning_end = self.peak_hours["morning"]
        evening_start, evening_end = self.peak_hours["evening"]
        
        return (morning_start <= time_of_day <= morning_end) or \
               (evening_start <= time_of_day <= evening_end)
    
    def get_congestion_factor(self, vehicle_count, weather_code, is_peak):
        """
        Calculate congestion factor based on multiple parameters
        
        Returns:
            float: Congestion factor (0-100)
        """
        # Base factor from vehicle count
        vehicle_factor = vehicle_count * 0.8
        
        # Weather adjustment
        weather_info = self.weather_types[weather_code]
        weather_factor = (weather_info['delay_factor'] - 1.0) * 30
        
        # Peak hour adjustment
        peak_factor = 20 if is_peak else 0
        
        # Combine factors
        congestion = vehicle_factor + weather_factor + peak_factor
        
        # Add small random variation
        congestion += random.uniform(-5, 5)
        
        # Ensure within bounds
        return max(0, min(100, congestion))
    
    def get_history(self, n=10):
        """Get last n data points from history"""
        return list(self.history)[-n:]
    
    def stream_data(self, interval=2, callback=None):
        """
        Continuously generate data at specified interval
        
        Args:
            interval (int): Time between data points in seconds
            callback (function): Function to call with each data point
        """
        while True:
            data = self.generate_data()
            if callback:
                callback(data)
            time.sleep(interval)


# ============================================
# UNIT TESTING
# ============================================

def test_simulator():
    """Test the traffic data simulator"""
    print("=" * 50)
    print("🧪 Testing Traffic Data Simulator")
    print("=" * 50)
    
    simulator = TrafficDataSimulator()
    
    print("\n📊 Generated Traffic Data:")
    print("-" * 60)
    
    for i in range(5):
        data = simulator.generate_data()
        print(
            f"  {data['time_formatted']}  | "
            f"🚗 {data['vehicle_count']:3d}  | "
            f"{data['weather_icon']} {data['weather_name']:6}  | "
            f"{'Peak' if data['is_peak_hour'] else 'Off'}"
        )
    
    print("-" * 60)
    print(f"\n📜 History: {len(simulator.history)} records")
    print("=" * 50)

if __name__ == "__main__":
    test_simulator()