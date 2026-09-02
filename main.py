"""
AI-Powered Smart Traffic Management System
Main Application File
Author: Avani Mitra (URK24CS1090)
Karunya Institute of Technology and Sciences
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.linear_model import LinearRegression
import numpy as np
import time
from datetime import datetime

# ============================================
# AI MODEL - Traffic Congestion Prediction
# ============================================

class TrafficPredictor:
    def __init__(self):
        """Initialize and train the AI model"""
        self.model = LinearRegression()
        self.training_data = np.array([
            [50, 7, 0],   # [vehicles, time, weather] - Clear
            [70, 8, 1],   # - Rainy
            [85, 9, 0],   # - Clear
            [40, 10, 2],  # - Foggy
            [90, 12, 0],  # - Clear
            [75, 17, 1],  # - Rainy
            [95, 18, 0],  # - Clear
            [30, 6, 2],   # - Foggy
            [80, 19, 1],  # - Rainy
            [65, 15, 0],  # - Clear
            [55, 13, 2],  # - Foggy
            [88, 20, 1],  # - Rainy
            [45, 11, 0],  # - Clear
            [92, 16, 1],  # - Rainy
            [38, 14, 2],  # - Foggy
        ])
        self.congestion_levels = np.array([
            65, 78, 92, 45, 95, 82, 98, 35, 85, 70, 58, 90, 50, 93, 42
        ])
        self._train_model()
    
    def _train_model(self):
        """Train the Linear Regression model"""
        try:
            self.model.fit(self.training_data, self.congestion_levels)
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict_congestion(self, vehicle_count, time_of_day, weather_condition):
        """
        Predict congestion level based on input parameters
        
        Args:
            vehicle_count (int): Number of vehicles (0-100)
            time_of_day (int): Hour of day (0-23)
            weather_condition (int): 0=Clear, 1=Rainy, 2=Foggy
        
        Returns:
            float: Predicted congestion level (0-100)
        """
        try:
            input_data = np.array([[vehicle_count, time_of_day, weather_condition]])
            prediction = self.model.predict(input_data)[0]
            # Ensure prediction stays within 0-100 range
            return max(0, min(100, prediction))
        except Exception as e:
            print(f"Prediction error: {e}")
            return 50  # Default fallback


# ============================================
# TRAFFIC LIGHT CONTROLLER
# ============================================

class TrafficLightController:
    """Controls traffic light timing based on congestion levels"""
    
    def __init__(self):
        self.green_time = 20  # Base green time in seconds
        self.yellow_time = 3
        self.red_time = 25
    
    def calculate_timings(self, congestion_level):
        """
        Calculate traffic light timings based on congestion
        
        Args:
            congestion_level (float): Predicted congestion (0-100)
        
        Returns:
            dict: Timing configuration
        """
        if congestion_level >= 80:
            # High congestion - Extended green
            green = 40
            yellow = 3
            red = 20
            action = "🟢 EXTENDED GREEN (40s) - Heavy Traffic"
            status = "CRITICAL"
            
        elif congestion_level >= 60:
            # Medium-high congestion - Extended green
            green = 30
            yellow = 3
            red = 25
            action = "🟢 MODERATE GREEN (30s) - High Traffic"
            status = "HIGH"
            
        elif congestion_level >= 40:
            # Medium congestion - Normal timing
            green = 25
            yellow = 3
            red = 30
            action = "🟡 NORMAL GREEN (25s) - Medium Traffic"
            status = "MEDIUM"
            
        elif congestion_level >= 20:
            # Low-medium congestion - Reduced green
            green = 20
            yellow = 3
            red = 35
            action = "🟢 REDUCED GREEN (20s) - Light Traffic"
            status = "LOW"
            
        else:
            # Very low congestion - Minimum green
            green = 15
            yellow = 3
            red = 40
            action = "🟢 MINIMUM GREEN (15s) - Very Light Traffic"
            status = "VERY LOW"
        
        return {
            'green_time': green,
            'yellow_time': yellow,
            'red_time': red,
            'action': action,
            'status': status,
            'cycle_time': green + yellow + red
        }
    
    def display_timing(self, timings):
        """Format timing information for display"""
        return f"""
╔═══════════════════════════════════════╗
║      TRAFFIC LIGHT TIMINGS            ║
╠═══════════════════════════════════════╣
║ 🟢 Green Light:  {timings['green_time']} seconds
║ 🟡 Yellow Light: {timings['yellow_time']} seconds
║ 🔴 Red Light:    {timings['red_time']} seconds
║ 🔄 Cycle Time:   {timings['cycle_time']} seconds
║ 📊 Status:       {timings['status']}
╚═══════════════════════════════════════╝
        """


# ============================================
# DATA SIMULATOR
# ============================================

class TrafficDataSimulator:
    """Simulates real-time traffic data"""
    
    def __init__(self):
        self.weather_types = {
            0: "☀️ Clear",
            1: "🌧️ Rainy",
            2: "🌫️ Foggy"
        }
        self.peak_hours = [7, 8, 9, 17, 18, 19, 20]
        self.off_peak_hours = [1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15, 16, 21, 22, 23]
    
    def get_vehicle_count(self, time_of_day):
        """Generate realistic vehicle count based on time"""
        if time_of_day in self.peak_hours:
            # Peak hours: 60-100 vehicles
            return random.randint(60, 100)
        elif time_of_day in self.off_peak_hours:
            # Off-peak hours: 10-50 vehicles
            return random.randint(10, 50)
        else:
            # Default: 20-70 vehicles
            return random.randint(20, 70)
    
    def get_weather_condition(self):
        """Generate random weather condition with weights"""
        weather_weights = [0.6, 0.3, 0.1]  # 60% Clear, 30% Rainy, 10% Foggy
        return random.choices([0, 1, 2], weights=weather_weights, k=1)[0]
    
    def get_time_of_day(self):
        """Get current time or simulate time"""
        return random.randint(0, 23)
    
    def generate_data(self):
        """Generate complete traffic data set"""
        time_of_day = self.get_time_of_day()
        vehicle_count = self.get_vehicle_count(time_of_day)
        weather_condition = self.get_weather_condition()
        
        return {
            'vehicle_count': vehicle_count,
            'time_of_day': time_of_day,
            'weather_condition': weather_condition,
            'weather_text': self.weather_types[weather_condition],
            'is_peak_hour': time_of_day in self.peak_hours
        }


# ============================================
# GUI INTERFACE
# ============================================

class TrafficManagementGUI:
    """Main GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚦 AI-Powered Smart Traffic Management System")
        self.root.geometry("850x750")
        self.root.configure(bg='#f0f4f8')
        self.root.resizable(False, False)
        
        # Initialize components
        self.predictor = TrafficPredictor()
        self.controller = TrafficLightController()
        self.simulator = TrafficDataSimulator()
        
        # History tracking
        self.history = []
        self.max_history = 10
        
        # Setup UI
        self._setup_ui()
        
        # Center window on screen
        self._center_window()
    
    def _center_window(self):
        """Center the application window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_ui(self):
        """Setup the user interface"""
        
        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ==========================================
        # HEADER
        # ==========================================
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="🚦 SMART TRAFFIC MANAGEMENT SYSTEM",
            font=("Arial", 18, "bold"),
            foreground="#1a237e"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="AI-Powered Real-time Traffic Control & Congestion Management",
            font=("Arial", 11),
            foreground="#455a64"
        )
        subtitle_label.pack()
        
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # ==========================================
        # CONTROL PANEL
        # ==========================================
        control_frame = ttk.LabelFrame(main_frame, text="🎮 Traffic Simulation Controls", padding=15)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        control_row = ttk.Frame(control_frame)
        control_row.pack(fill=tk.X, pady=5)
        
        self.simulate_btn = ttk.Button(
            control_row,
            text="🚦 SIMULATE TRAFFIC",
            command=self.simulate_traffic,
            style='Custom.TButton'
        )
        self.simulate_btn.pack(side=tk.LEFT, padx=5)
        
        self.auto_simulate_btn = ttk.Button(
            control_row,
            text="🔄 AUTO SIMULATE",
            command=self.toggle_auto_simulate
        )
        self.auto_simulate_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            control_row,
            text="🗑️ CLEAR HISTORY",
            command=self.clear_history
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(
            control_row,
            text="✅ System Ready",
            font=("Arial", 10),
            foreground="green"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # ==========================================
        # DATA DISPLAY PANEL
        # ==========================================
        data_frame = ttk.LabelFrame(main_frame, text="📊 Real-time Traffic Data", padding=15)
        data_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Data Grid
        grid_frame = ttk.Frame(data_frame)
        grid_frame.pack(fill=tk.X)
        
        # Row 1
        row1 = ttk.Frame(grid_frame)
        row1.pack(fill=tk.X, pady=3)
        
        ttk.Label(row1, text="🚗 Vehicles:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        self.vehicle_label = ttk.Label(row1, text="--", font=("Arial", 11))
        self.vehicle_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="⏰ Time:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=20)
        self.time_label = ttk.Label(row1, text="--", font=("Arial", 11))
        self.time_label.pack(side=tk.LEFT, padx=5)
        
        # Row 2
        row2 = ttk.Frame(grid_frame)
        row2.pack(fill=tk.X, pady=3)
        
        ttk.Label(row2, text="🌤️ Weather:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        self.weather_label = ttk.Label(row2, text="--", font=("Arial", 11))
        self.weather_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="📈 Peak Hour:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=20)
        self.peak_label = ttk.Label(row2, text="--", font=("Arial", 11))
        self.peak_label.pack(side=tk.LEFT, padx=5)
        
        # ==========================================
        # AI PREDICTION PANEL
        # ==========================================
        prediction_frame = ttk.LabelFrame(main_frame, text="🧠 AI Congestion Prediction", padding=15)
        prediction_frame.pack(fill=tk.X, pady=(0, 15))
        
        pred_grid = ttk.Frame(prediction_frame)
        pred_grid.pack(fill=tk.X)
        
        # Congestion Level with Progress Bar
        pred_row1 = ttk.Frame(pred_grid)
        pred_row1.pack(fill=tk.X, pady=3)
        
        ttk.Label(pred_row1, text="📊 Congestion Level:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        self.congestion_label = ttk.Label(pred_row1, text="--%", font=("Arial", 14, "bold"))
        self.congestion_label.pack(side=tk.LEFT, padx=5)
        
        # Progress Bar
        self.congestion_bar = ttk.Progressbar(
            pred_grid,
            length=400,
            mode='determinate',
            style='green.Horizontal.TProgressbar'
        )
        self.congestion_bar.pack(pady=5, padx=10, fill=tk.X)
        
        # ==========================================
        # TRAFFIC LIGHT ACTION PANEL
        # ==========================================
        action_frame = ttk.LabelFrame(main_frame, text="🚦 Traffic Light Action", padding=15)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        action_grid = ttk.Frame(action_frame)
        action_grid.pack(fill=tk.X)
        
        self.action_label = ttk.Label(
            action_grid,
            text="⏳ Waiting for simulation...",
            font=("Arial", 13, "bold"),
            foreground="#1a237e"
        )
        self.action_label.pack(pady=5)
        
        # Timings Display
        self.timing_label = ttk.Label(
            action_grid,
            text="",
            font=("Courier", 10),
            justify=tk.LEFT
        )
        self.timing_label.pack(pady=5)
        
        # ==========================================
        # HISTORY PANEL
        # ==========================================
        history_frame = ttk.LabelFrame(main_frame, text="📜 Simulation History", padding=15)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # History Listbox with Scrollbar
        history_container = ttk.Frame(history_frame)
        history_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(history_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            history_container,
            height=5,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # ==========================================
        # FOOTER
        # ==========================================
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        footer_text = f"🏫 Karunya Institute of Technology and Sciences  |  👩‍💻 Avani Mitra (URK24CS1090)"
        ttk.Label(footer_frame, text=footer_text, font=("Arial", 8), foreground="#78909c").pack()
        
        # Auto-simulate flag
        self.auto_simulate_running = False
        self.auto_simulate_id = None
        
        # Configure styles
        self._configure_styles()
    
    def _configure_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        
        # Custom button style
        style.configure('Custom.TButton', font=('Arial', 11, 'bold'))
        
        # Progress bar colors based on value
        style.configure('green.Horizontal.TProgressbar', background='#4caf50')
        style.configure('yellow.Horizontal.TProgressbar', background='#ffc107')
        style.configure('red.Horizontal.TProgressbar', background='#f44336')
    
    def simulate_traffic(self):
        """Simulate traffic data and update display"""
        try:
            # Update status
            self.status_label.config(text="⏳ Processing...", foreground="#ff9800")
            self.root.update()
            
            # Generate simulated data
            traffic_data = self.simulator.generate_data()
            
            # Predict congestion
            congestion_level = self.predictor.predict_congestion(
                traffic_data['vehicle_count'],
                traffic_data['time_of_day'],
                traffic_data['weather_condition']
            )
            
            # Calculate traffic light timings
            timings = self.controller.calculate_timings(congestion_level)
            
            # Update GUI with results
            self._update_display(traffic_data, congestion_level, timings)
            
            # Add to history
            self._add_to_history(traffic_data, congestion_level, timings)
            
            # Update status
            self.status_label.config(text="✅ Simulation Complete", foreground="#4caf50")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during simulation:\n{str(e)}")
            self.status_label.config(text=f"❌ Error: {str(e)}", foreground="#f44336")
    
    def _update_display(self, data, congestion, timings):
        """Update all display elements with new data"""
        
        # Update data display
        self.vehicle_label.config(text=f"{data['vehicle_count']}")
        self.time_label.config(text=f"{data['time_of_day']:02d}:00h")
        self.weather_label.config(text=f"{data['weather_text']}")
        self.peak_label.config(text="✅ Yes" if data['is_peak_hour'] else "❌ No")
        
        # Update congestion display
        self.congestion_label.config(text=f"{congestion:.1f}%")
        self.congestion_bar['value'] = congestion
        
        # Change progress bar color based on congestion level
        style = ttk.Style()
        if congestion >= 70:
            style.configure('green.Horizontal.TProgressbar', background='#f44336')
        elif congestion >= 40:
            style.configure('green.Horizontal.TProgressbar', background='#ffc107')
        else:
            style.configure('green.Horizontal.TProgressbar', background='#4caf50')
        
        # Update action display
        self.action_label.config(
            text=timings['action'],
            foreground='#1a237e'
        )
        
        # Update timing display
        timing_text = f"""
        🟢 Green: {timings['green_time']}s  |  🟡 Yellow: {timings['yellow_time']}s  |  🔴 Red: {timings['red_time']}s  |  🔄 Cycle: {timings['cycle_time']}s
        📊 Status: {timings['status']}
        """
        self.timing_label.config(text=timing_text)
    
    def _add_to_history(self, data, congestion, timings):
        """Add simulation result to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = (
            f"[{timestamp}] 🚗{data['vehicle_count']:3d}  "
            f"⏰{data['time_of_day']:02d}:00  "
            f"{data['weather_text']:8}  "
            f"📊{congestion:5.1f}%  "
            f"⚡{timings['status']:8}"
        )
        
        self.history.append(history_entry)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        self._refresh_history()
    
    def _refresh_history(self):
        """Refresh the history listbox"""
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)
    
    def clear_history(self):
        """Clear simulation history"""
        self.history.clear()
        self._refresh_history()
        self.status_label.config(text="🗑️ History Cleared", foreground="#ff9800")
    
    def toggle_auto_simulate(self):
        """Toggle automatic simulation"""
        if self.auto_simulate_running:
            self.stop_auto_simulate()
        else:
            self.start_auto_simulate()
    
    def start_auto_simulate(self):
        """Start automatic simulation"""
        self.auto_simulate_running = True
        self.auto_simulate_btn.config(text="⏹️ STOP AUTO")
        self.status_label.config(text="🔄 Auto-simulation running...", foreground="#2196f3")
        self._run_auto_simulate()
    
    def stop_auto_simulate(self):
        """Stop automatic simulation"""
        self.auto_simulate_running = False
        if self.auto_simulate_id:
            self.root.after_cancel(self.auto_simulate_id)
            self.auto_simulate_id = None
        self.auto_simulate_btn.config(text="🔄 AUTO SIMULATE")
        self.status_label.config(text="⏸️ Auto-simulation paused", foreground="#ff9800")
    
    def _run_auto_simulate(self):
        """Run one auto-simulation cycle"""
        if not self.auto_simulate_running:
            return
        
        self.simulate_traffic()
        self.auto_simulate_id = self.root.after(2000, self._run_auto_simulate)
    
    def on_closing(self):
        """Handle application closing"""
        if self.auto_simulate_running:
            self.stop_auto_simulate()
        self.root.destroy()


# ============================================
# APPLICATION ENTRY POINT
# ============================================

def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        app = TrafficManagementGUI(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start:\n{str(e)}")

if __name__ == "__main__":
    main()