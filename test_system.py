"""
System Test Suite
Author: Avani Mitra (URK24CS1090)
"""

import sys
import time
from ai_model import TrafficPredictor
from traffic_control import TrafficLightController
from data_simulator import TrafficDataSimulator

def run_system_test():
    """Run comprehensive system test"""
    
    print("=" * 60)
    print("🔬 SYSTEM INTEGRATION TEST")
    print("=" * 60)
    
    # Initialize components
    print("\n📦 Initializing components...")
    
    print("  🧠 AI Model...", end="")
    predictor = TrafficPredictor()
    print(" ✅")
    
    print("  🚦 Traffic Controller...", end="")
    controller = TrafficLightController()
    print(" ✅")
    
    print("  📊 Data Simulator...", end="")
    simulator = TrafficDataSimulator()
    print(" ✅")
    
    # Run test simulation
    print("\n🔄 Running test simulation...")
    print("-" * 60)
    
    test_results = []
    
    for i in range(10):
        print(f"\n📊 Test {i+1}/10:")
        
        # Generate data
        data = simulator.generate_data()
        print(f"  🚗 Vehicles: {data['vehicle_count']}")
        print(f"  ⏰ Time: {data['time_formatted']}")
        print(f"  🌤️ Weather: {data['weather_icon']} {data['weather_name']}")
        
        # Predict congestion
        congestion = predictor.predict_congestion(
            data['vehicle_count'],
            data['time_of_day'],
            data['weather_code']
        )
        print(f"  📊 Predicted Congestion: {congestion:.1f}%")
        
        # Calculate timings
        timings = controller.calculate_timings(congestion)
        print(f"  🚦 Action: {timings['action']}")
        print(f"  🔄 Cycle: {timings['cycle_time']}s")
        
        test_results.append({
            'congestion': congestion,
            'timings': timings
        })
        
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    avg_congestion = sum(r['congestion'] for r in test_results) / len(test_results)
    print(f"\n📈 Average Congestion: {avg_congestion:.1f}%")
    
    status_counts = {}
    for r in test_results:
        status = r['timings']['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\n📊 Status Distribution:")
    for status, count in status_counts.items():
        print(f"  {status}: {count} times")
    
    print("\n✅ System test completed successfully!")
    print("=" * 60)

def performance_test():
    """Test system performance"""
    
    print("\n" + "=" * 60)
    print("⚡ PERFORMANCE TEST")
    print("=" * 60)
    
    predictor = TrafficPredictor()
    simulator = TrafficDataSimulator()
    
    n_tests = 100
    start_time = time.time()
    
    print(f"\n📊 Running {n_tests} predictions...")
    
    for _ in range(n_tests):
        data = simulator.generate_data()
        _ = predictor.predict_congestion(
            data['vehicle_count'],
            data['time_of_day'],
            data['weather_code']
        )
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = (total_time / n_tests) * 1000  # milliseconds
    
    print(f"\n⏱️ Total time: {total_time:.3f}s")
    print(f"⏱️ Average prediction time: {avg_time:.2f}ms")
    print(f"📊 Throughput: {n_tests / total_time:.1f} predictions/second")
    
    print("\n✅ Performance test completed!")
    print("=" * 60)

def edge_case_test():
    """Test edge cases"""
    
    print("\n" + "=" * 60)
    print("🔍 EDGE CASE TEST")
    print("=" * 60)
    
    predictor = TrafficPredictor()
    controller = TrafficLightController()
    
    test_cases = [
        (0, 0, 0, "Minimum vehicles"),
        (100, 12, 0, "Maximum vehicles"),
        (50, 8, 0, "Peak hour"),
        (50, 3, 2, "Off-peak + foggy"),
        (0, 23, 3, "Night + snow"),
    ]
    
    print("\n📊 Testing edge cases:")
    print("-" * 60)
    
    for vehicles, time, weather, description in test_cases:
        congestion = predictor.predict_congestion(vehicles, time, weather)
        timings = controller.calculate_timings(congestion)
        
        print(f"\n📌 {description}:")
        print(f"  🚗 {vehicles} vehicles at {time:02d}:00")
        print(f"  📊 Congestion: {congestion:.1f}%")
        print(f"  🚦 Action: {timings['action']}")
        print(f"  ✅ Status: {timings['status']}")
    
    print("\n✅ Edge case test completed!")
    print("=" * 60)

def run_all_tests():
    """Run all tests"""
    
    print("\n" + "=" * 60)
    print("🧪 COMPLETE SYSTEM TEST SUITE")
    print("=" * 60)
    
    # Run tests
    run_system_test()
    performance_test()
    edge_case_test()
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()