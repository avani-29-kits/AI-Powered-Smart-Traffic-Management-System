"""
AI-Powered Smart Traffic Management System 
Author: Avani Mitra 
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime
import time

# ============================================
# AI MODEL
# ============================================

class TrafficPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.training_data = np.array([
            [50, 7, 0], [70, 8, 1], [85, 9, 0], [40, 10, 2],
            [90, 12, 0], [75, 17, 1], [95, 18, 0], [30, 6, 2],
            [80, 19, 1], [65, 15, 0], [55, 13, 2], [88, 20, 1],
            [45, 11, 0], [92, 16, 1], [38, 14, 2]
        ])
        self.congestion_levels = np.array([
            65, 78, 92, 45, 95, 82, 98, 35, 85, 70, 58, 90, 50, 93, 42
        ])
        self.model.fit(self.training_data, self.congestion_levels)
    
    def predict_congestion(self, vehicle_count, time_of_day, weather_condition):
        input_data = np.array([[vehicle_count, time_of_day, weather_condition]])
        prediction = self.model.predict(input_data)[0]
        return max(0, min(100, prediction))


# ============================================
# TRAFFIC LIGHT CONTROLLER
# ============================================

class TrafficLightController:
    def calculate_timings(self, congestion_level):
        if congestion_level >= 80:
            return {
                'green_time': 40, 'yellow_time': 3, 'red_time': 20,
                'action': "🔴 EXTREME CONGESTION",
                'status': "CRITICAL",
                'color': '#ff1744',
                'bg_color': '#ff174420',
                'suggestion': "🚨 Seek alternate routes"
            }
        elif congestion_level >= 60:
            return {
                'green_time': 30, 'yellow_time': 3, 'red_time': 25,
                'action': "🟠 HIGH TRAFFIC",
                'status': "HIGH",
                'color': '#ff9100',
                'bg_color': '#ff910020',
                'suggestion': "⏰ Allow extra time"
            }
        elif congestion_level >= 40:
            return {
                'green_time': 25, 'yellow_time': 3, 'red_time': 30,
                'action': "🟡 MODERATE TRAFFIC",
                'status': "MEDIUM",
                'color': '#ffea00',
                'bg_color': '#ffea0020',
                'suggestion': "✅ Normal driving"
            }
        elif congestion_level >= 20:
            return {
                'green_time': 20, 'yellow_time': 3, 'red_time': 35,
                'action': "🟢 LIGHT TRAFFIC",
                'status': "LOW",
                'color': '#00e676',
                'bg_color': '#00e67620',
                'suggestion': "🚗 Smooth drive"
            }
        else:
            return {
                'green_time': 15, 'yellow_time': 3, 'red_time': 40,
                'action': "✅ VERY LIGHT TRAFFIC",
                'status': "VERY LOW",
                'color': '#00b0ff',
                'bg_color': '#00b0ff20',
                'suggestion': "🏁 Enjoy the ride"
            }


# ============================================
# DATA SIMULATOR
# ============================================

class TrafficDataSimulator:
    def __init__(self):
        self.weather_types = {
            0: "☀️ Clear",
            1: "🌧️ Rainy",
            2: "🌫️ Foggy"
        }
    
    def generate_data(self):
        time_of_day = random.randint(6, 22)
        vehicle_count = random.randint(20, 100)
        weather_condition = random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1], k=1)[0]
        is_peak = time_of_day in [7, 8, 9, 17, 18, 19]
        
        return {
            'vehicle_count': vehicle_count,
            'time_of_day': time_of_day,
            'weather_condition': weather_condition,
            'weather_text': self.weather_types[weather_condition],
            'is_peak_hour': is_peak
        }


# ============================================
# STUNNING GUI
# ============================================

class TrafficManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚦 SMART TRAFFIC MANAGEMENT SYSTEM")
        self.root.geometry("1200x750")
        self.root.configure(bg='#0a0a1a')
        self.root.resizable(False, False)
        
        # Initialize components
        self.predictor = TrafficPredictor()
        self.controller = TrafficLightController()
        self.simulator = TrafficDataSimulator()
        self.history = []
        self.auto_running = False
        
        # Build UI
        self._build_ui()
        
        # Center window
        self._center_window()
        
        # Initial animation
        self._animate_welcome()
    
    def _center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f'1200x750+{x}+{y}')
    
    def _animate_welcome(self):
        self.status_label.config(text="🚀 Welcome to Smart Traffic System!", fg="#00e676")
    
    def _build_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#0a0a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ==========================================
        # HEADER
        # ==========================================
        header = tk.Frame(main_frame, bg='#0a0a1a')
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Title with shadow effect
        title = tk.Label(
            header,
            text="🚦 SMART TRAFFIC MANAGEMENT SYSTEM",
            font=("Segoe UI", 22, "bold"),
            fg="#ffffff",
            bg='#0a0a1a'
        )
        title.pack()
        
        subtitle = tk.Label(
            header,
            text="⚡ AI-Powered Real-time Traffic Control & Congestion Management",
            font=("Segoe UI", 12),
            fg="#6a7a9e",
            bg='#0a0a1a'
        )
        subtitle.pack()
        
        # Decorative line
        line = tk.Frame(main_frame, height=2, bg='#1a2a4a')
        line.pack(fill=tk.X, pady=10)
        
        # ==========================================
        # TOP CONTROLS
        # ==========================================
        controls = tk.Frame(main_frame, bg='#0a0a1a')
        controls.pack(fill=tk.X, pady=(0, 15))
        
        # Button style function
        def create_button(parent, text, command, color, hover_color):
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                font=("Segoe UI", 11, "bold"),
                bg=color,
                fg="#ffffff",
                relief=tk.FLAT,
                cursor='hand2',
                padx=25,
                pady=10,
                borderwidth=0
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Hover effect
            def on_enter(e):
                btn.config(bg=hover_color)
            def on_leave(e):
                btn.config(bg=color)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            return btn
        
        self.simulate_btn = create_button(controls, "🚦 SIMULATE", self.simulate_traffic, '#00b4d8', '#00d4ff')
        self.auto_btn = create_button(controls, "🔄 AUTO", self.toggle_auto, '#f4a261', '#f4c430')
        self.clear_btn = create_button(controls, "🗑️ CLEAR", self.clear_history, '#e63946', '#ff1744')
        
        # Status label
        self.status_label = tk.Label(
            controls,
            text="✅ System Ready",
            font=("Segoe UI", 11),
            fg="#00e676",
            bg='#0a0a1a'
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # ==========================================
        # MAIN CONTENT - TWO COLUMNS
        # ==========================================
        content = tk.Frame(main_frame, bg='#0a0a1a')
        content.pack(fill=tk.BOTH, expand=True)
        
        # LEFT COLUMN
        left = tk.Frame(content, bg='#0a0a1a')
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # --- Card 1: Traffic Data ---
        card1 = self._create_card(left, "📊 REAL-TIME DATA")
        
        data_grid = tk.Frame(card1, bg='#111128')
        data_grid.pack(padx=20, pady=15)
        
        # 2x2 Grid
        items = [
            ("🚗 Vehicles:", "vehicle_label", "#4fc3f7"),
            ("⏰ Time:", "time_label", "#4fc3f7"),
            ("🌤️ Weather:", "weather_label", "#4fc3f7"),
            ("📈 Peak Hour:", "peak_label", "#4fc3f7")
        ]
        
        for i, (label, attr, color) in enumerate(items):
            row = tk.Frame(data_grid, bg='#111128')
            row.pack(fill=tk.X, pady=4)
            
            tk.Label(
                row, text=label, font=("Segoe UI", 12, "bold"),
                fg="#aab", bg='#111128'
            ).pack(side=tk.LEFT, padx=5)
            
            lbl = tk.Label(
                row, text="--", font=("Segoe UI", 14, "bold"),
                fg=color, bg='#111128'
            )
            lbl.pack(side=tk.LEFT, padx=10)
            setattr(self, attr, lbl)
        
        # --- Card 2: AI Prediction ---
        card2 = self._create_card(left, "🧠 AI CONGESTION PREDICTION")
        
        pred_frame = tk.Frame(card2, bg='#111128')
        pred_frame.pack(padx=20, pady=15)
        
        # Big number
        self.congestion_label = tk.Label(
            pred_frame,
            text="--%",
            font=("Segoe UI", 56, "bold"),
            fg="#4fc3f7",
            bg='#111128'
        )
        self.congestion_label.pack(pady=5)
        
        # Status
        self.congestion_status = tk.Label(
            pred_frame,
            text="Waiting for data...",
            font=("Segoe UI", 13),
            fg="#6a7a9e",
            bg='#111128'
        )
        self.congestion_status.pack(pady=5)
        
        # Progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar",
                       background='#4fc3f7',
                       troughcolor='#1a1a3a',
                       bordercolor='#111128',
                       lightcolor='#4fc3f7',
                       darkcolor='#4fc3f7')
        
        self.congestion_bar = ttk.Progressbar(
            pred_frame,
            style="Custom.Horizontal.TProgressbar",
            length=350,
            mode='determinate',
            maximum=100
        )
        self.congestion_bar.pack(pady=10)
        
        # --- Card 3: Traffic Light ---
        card3 = self._create_card(left, "🚦 TRAFFIC LIGHT CONTROL")
        
        action_frame = tk.Frame(card3, bg='#111128')
        action_frame.pack(padx=20, pady=15)
        
        self.action_label = tk.Label(
            action_frame,
            text="⏳ Click Simulate",
            font=("Segoe UI", 16, "bold"),
            fg="#6a7a9e",
            bg='#111128'
        )
        self.action_label.pack(pady=5)
        
        self.timing_label = tk.Label(
            action_frame,
            text="",
            font=("Segoe UI", 12),
            fg="#4fc3f7",
            bg='#111128'
        )
        self.timing_label.pack(pady=5)
        
        self.suggestion_label = tk.Label(
            action_frame,
            text="",
            font=("Segoe UI", 11, "italic"),
            fg="#aab",
            bg='#111128'
        )
        self.suggestion_label.pack(pady=5)
        
        # RIGHT COLUMN
        right = tk.Frame(content, bg='#0a0a1a')
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # --- Card 4: History ---
        card4 = self._create_card(right, "📜 SIMULATION HISTORY")
        
        hist_container = tk.Frame(card4, bg='#111128')
        hist_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(hist_container, bg='#1a1a3a', troughcolor='#0a0a1a')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            hist_container,
            height=8,
            font=("Consolas", 10),
            bg='#0a0a1a',
            fg='#4fc3f7',
            selectbackground='#1a2a4a',
            selectforeground='#ffffff',
            bd=0,
            relief=tk.FLAT,
            yscrollcommand=scrollbar.set
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # FOOTER
        footer = tk.Frame(main_frame, bg='#0a0a1a')
        footer.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(
            footer,
            text="🏫 Karunya Institute of Technology and Sciences  |  👩‍💻 Avani Mitra (URK24CS1090)  |  🚦 2025",
            font=("Segoe UI", 9),
            fg="#3a4a5a",
            bg='#0a0a1a'
        ).pack()
    
    def _create_card(self, parent, title):
        """Create a styled card"""
        card = tk.Frame(
            parent,
            bg='#111128',
            relief=tk.RAISED,
            bd=1
        )
        card.pack(fill=tk.X, pady=5)
        
        # Card header
        header = tk.Frame(card, bg='#1a1a3a')
        header.pack(fill=tk.X, padx=1, pady=1)
        
        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 13, "bold"),
            fg="#6a8aae",
            bg='#1a1a3a'
        ).pack(anchor='w', padx=20, pady=10)
        
        return card
    
    def simulate_traffic(self):
        try:
            self.status_label.config(text="⏳ Processing...", fg="#f4a261")
            self.root.update()
            
            # Generate data
            data = self.simulator.generate_data()
            
            # Predict
            congestion = self.predictor.predict_congestion(
                data['vehicle_count'],
                data['time_of_day'],
                data['weather_condition']
            )
            
            # Get timings
            timings = self.controller.calculate_timings(congestion)
            
            # Update data display
            self.vehicle_label.config(text=str(data['vehicle_count']))
            self.time_label.config(text=f"{data['time_of_day']:02d}:00")
            self.weather_label.config(text=data['weather_text'])
            self.peak_label.config(text="✅ YES" if data['is_peak_hour'] else "❌ NO")
            
            # Update congestion
            self.congestion_label.config(text=f"{congestion:.1f}%")
            self.congestion_bar['value'] = congestion
            
            # Color coding
            color = timings['color']
            self.congestion_label.config(fg=color)
            self.congestion_status.config(text=f"{timings['status']} | {timings['action']}", fg=color)
            
            # Update progress bar
            style = ttk.Style()
            style.configure("Custom.Horizontal.TProgressbar", background=color)
            
            # Update action
            self.action_label.config(text=timings['action'], fg=color)
            self.timing_label.config(
                text=f"🟢 Green: {timings['green_time']}s  🟡 Yellow: 3s  🔴 Red: {timings['red_time']}s  🔄 Cycle: {timings['green_time'] + timings['yellow_time'] + timings['red_time']}s"
            )
            self.suggestion_label.config(text=timings['suggestion'])
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] 🚗{data['vehicle_count']:3d}  ⏰{data['time_of_day']:02d}:00  {data['weather_text']:10}  📊{congestion:5.1f}%  {timings['status']:8}"
            self.history.append(history_entry)
            if len(self.history) > 15:
                self.history.pop(0)
            
            self.history_listbox.delete(0, tk.END)
            for entry in self.history:
                self.history_listbox.insert(tk.END, entry)
            
            self.status_label.config(text="✅ Simulation Complete!", fg="#00e676")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            self.status_label.config(text="❌ Error", fg="#ff1744")
    
    def toggle_auto(self):
        if self.auto_running:
            self.auto_running = False
            self.auto_btn.config(text="🔄 AUTO", bg='#f4a261')
            self.status_label.config(text="⏸️ Paused", fg="#f4a261")
        else:
            self.auto_running = True
            self.auto_btn.config(text="⏹️ STOP", bg='#e63946')
            self.status_label.config(text="🔄 Auto-running...", fg="#4fc3f7")
            self._auto_loop()
    
    def _auto_loop(self):
        if self.auto_running:
            self.simulate_traffic()
            self.root.after(1500, self._auto_loop)
    
    def clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)
        self.status_label.config(text="🗑️ History Cleared", fg="#ff1744")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficManagementGUI(root)
    root.mainloop()