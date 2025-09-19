from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        material = request.form["material"].lower()
        gauge = float(request.form["gauge"])
        total_weight = float(request.form["total_weight"])
        pvc_rate = float(request.form["pvc_rate"])
        margin = float(request.form["margin"])
        rate = 0
        result = {}

        if material == "c":  # Copper
            density = 452
            wires = int(request.form["wires"])
            wire_type = request.form["wire_type"].lower()

            if wire_type == "h":
                copper = (gauge * gauge) * density * wires
                copper = (copper / 1000000) * 0.9
            else:  # Submersible
                copper = (gauge * gauge) * density * wires * 3
                copper = copper / 1000000

            copper = math.floor(copper * 1000) / 1000
            crate = float(request.form["rate"])
            final = math.floor(crate * copper * 1000) / 1000
            pvc = math.floor((total_weight - copper) * 1000) / 1000
            totalpvc = math.floor(pvc * pvc_rate * 1000) / 1000
            rate = math.floor((final + totalpvc) * 1000) / 1000
            rate = math.floor((rate + (0.07 * rate)) * 1000) / 1000
            marginadded = math.floor((rate + (margin/100 * rate)) * 100) / 100

            result = {
                "copper": copper,
                "pvc": pvc,
                "final": final,
                "totalpvc": totalpvc,
                "total_cost": marginadded
            }

        elif material == "a":  # Aluminium
            density = 138
            cores = int(request.form["cores"])
            aluminium = (gauge * gauge) * density * cores
            aluminium = math.floor((aluminium / 1000000) * 1000) / 1000
            arate = float(request.form["rate"])
            final = math.floor(arate * aluminium * 1000) / 1000
            pvc = math.floor((total_weight - aluminium) * 1000) / 1000
            totalpvc = math.floor(pvc * pvc_rate * 1000) / 1000
            rate = math.floor((final + totalpvc) * 1000) / 1000
            rate = math.floor((rate + (0.10 * rate)) * 1000) / 1000
            marginadded = math.floor((rate + (margin/100 * rate)) * 100) / 100

            result = {
                "aluminium": aluminium,
                "pvc": pvc,
                "final": final,
                "totalpvc": totalpvc,
                "total_cost": marginadded
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
