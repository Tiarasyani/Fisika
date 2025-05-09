from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Fungsi menghitung kapasitor seri dan paralel
def hitung_kapasitor_seri(kapasitor_list):
    try:
        total = sum([1 / c for c in kapasitor_list])
        return 1 / total if total != 0 else 0
    except:
        return 0

def hitung_kapasitor_paralel(kapasitor_list):
    return sum(kapasitor_list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materi')
def materi():
    return render_template('materi.html')

@app.route('/rumus')
def rumus():
    return render_template('rumus.html')

@app.route('/contoh')
def contoh():
    return render_template('contoh.html')

@app.route('/kalkulator', methods=['GET', 'POST'])
def kalkulator():
    total_capacitance = None
    configuration = None
    energy = None
    charge = None
    voltage = None
    capacitors = []

    if request.method == 'POST':
        configuration = request.form.get('configuration')
        voltage = request.form.get('voltage')
        if voltage:
            voltage = float(voltage)

        # Ambil semua input kapasitor yang diisi dan ubah ke float
        capacitors = [float(c) for c in request.form.getlist('capacitor') if c]

        if configuration == 'seri' and capacitors:
            try:
                total_capacitance = 1 / sum(1 / c for c in capacitors)
            except ZeroDivisionError:
                total_capacitance = 0
        elif configuration == 'paralel':
            total_capacitance = sum(capacitors)

        # Hitung energi dan muatan jika data valid
        if total_capacitance and voltage:
            energy = 0.5 * total_capacitance * (voltage ** 2)
            charge = total_capacitance * voltage

    return render_template("kalkulator.html",
                           total_capacitance=total_capacitance,
                           configuration=configuration,
                           capacitors=capacitors,
                           voltage=voltage,
                           energy=energy,
                           charge=charge)

if __name__ == '__main__':
    app.run(debug=True)
