from flask import Flask, request, render_template, redirect, url_for, flash
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

zones = []

@app.route('/')
def index():
    return render_template('index.html', zones=zones)

@app.route('/submit', methods=['POST'])
def submit():
    zone = request.form['zone'].strip()
    priority = int(request.form['priority'])

    # Check for duplicate
    for z, _, _ in zones:
        if z.lower() == zone.lower():
            flash("Zone already exists!", "error")
            return redirect(url_for('index'))

    # 🌟 Call the C program (disaster_management.exe)
    if os.path.exists("disaster_management.exe"):
        try:
            result = subprocess.run(["./dsproject.exe"], capture_output=True, text=True)
            print("C program output:\n", result.stdout)
        except Exception as e:
            print(f"Error running C program: {e}")
    else:
        print("C program not found. Skipping...")

    # Allocate resources based on priority
    if priority >= 8:
        resources = "Medicines, Food, Rescue Team"
    elif priority >= 5:
        resources = "Food, Water"
    else:
        resources = "Water only"

    zones.append((zone, priority, resources))
    zones.sort(key=lambda x: -x[1])  # Sort by descending priority

    flash("Zone added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    zone_to_delete = request.form['zone']

    global zones
    zones = [z for z in zones if z[0] != zone_to_delete]

    flash("Zone deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
