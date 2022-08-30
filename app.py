from flask import Flask, render_template, redirect, request, url_for, flash
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = uuid4().hex

calculation_log = list()

@app.route("/", methods=["GET"])
def index():
    global calculation_log
    return render_template('index.html', result=None, log=calculation_log)

@app.route("/math_operations", methods=["POST"])
def math_operations():
    valid_operations = ["add", "sub", "mul", "div", "exp", "sqrt", "sq"]

    if request.form.get("operation") in valid_operations[:-1]:
        if request.form.get("a") and request.form.get("b"):
            return redirect(f'/{request.form.get("operation")}?a={request.form.get("a")}&b={request.form.get("b")}')
        else:
            flash("** ERROR: two args required to use calculator! **")
            return redirect(url_for("index"))
    elif request.form.get("operation") in valid_operations[-1]:
        if request.form.get("a"):
            return redirect(f'/sq?a={request.form.get("a")}')
        else:
            flash("** ERROR: value for A required for calculation! **")
            return redirect(url_for("index"))
    else:
        return redirect("/")

@app.route("/add")
def add():
    try:
        a, b = float(request.args.get("a")), float(request.args.get("b"))
    except ValueError as e:
        flash("** ERROR: non-integer values were passed into calculator! **")
        return redirect(url_for('index'))
    except TypeError as e:
        flash("** ERROR: non-integer values were passed into calculator! **")
        return redirect(url_for('index'))
    else:
        sum = a + b
        global calculation_log
        calculation_log.append({"time": str(datetime.utcnow()), "a": a, "b": b, "operation": "addition", "operator": "+", "result": sum})
        print(f"Sum = {sum}")
        return render_template("index.html", result=str(round(sum, 2)), log=calculation_log)

@app.route("/sub")
def sub():
    try:
        a, b = float(request.args.get("a")), float(request.args.get("b"))
    except ValueError as e:
        flash("** ERROR: non-integer values were passed into calculator! **")
        return redirect(url_for('index'))
    else:
        diff = a - b
        global calculation_log
        calculation_log.append({"time": str(datetime.utcnow()), "a": a, "b": b, "operation": "square", "operator": "-", "result": diff})
        return render_template("index.html", result=str(round(diff, 2)), log=calculation_log)

@app.route("/mul")
def mul():
    try:
        a, b = float(request.args.get("a")), float(request.args.get("b"))
    except ValueError as e:
        flash("** ERROR: non-integer values were passed into calculator! **")
        return redirect(url_for('index'))
    else:
        product = a * b
        global calculation_log
        calculation_log.append({"time": str(datetime.utcnow()), "a": a, "b": b, "operation": "square", "operator": "*", "result": product})
        return render_template("index.html", result=str(round(product, 2)), log=calculation_log)

@app.route("/div")
def div():
    try:
        a, b = float(request.args.get("a")), float(request.args.get("b"))
        quotient = a / b
    except ValueError as e:
        flash("** ERROR: non-integer values were passed into calculator! **")
        return redirect(url_for('index'))
    except ZeroDivisionError as e:
        flash("** ERROR: cannot divide by zero! **")
        return redirect(url_for('index'))
    else:
        global calculation_log
        calculation_log.append({"time": str(datetime.utcnow()), "a": a, "b": b, "operation": "square", "operator": "/", "result": quotient})
        return render_template("index.html", result=str(round(quotient, 2)), log=calculation_log)

@app.route("/exp")
def exp():
    try:
        a, b = float(request.args.get("a")), float(request.args.get("b"))
    except ValueError as e:
        flash("** ERROR: non-integer values were passed into calculator! **")
        return redirect(url_for('index'))
    else:
        product = a ** b
        global calculation_log
        calculation_log.append({"time": str(datetime.utcnow()), "a": a, "b": b, "operation": "square", "operator": "**", "result": product})
        return render_template("index.html", result=str(round(product, 2)), log=calculation_log)

@app.route("/sq")
def sq():
    try:
        a, b = float(request.args.get("a")), 2
    except ValueError as e:
        flash("** ERROR: non-integer values were passed into calculator! **")
        return redirect(url_for('index'))
    else:
        product = a ** b
        global calculation_log
        calculation_log.append({"time": str(datetime.utcnow()), "a": a, "b": b, "operation": "square", "operator": "**", "result": product})
        return render_template("index.html", result=str(round(product, 2)), log=calculation_log)

@app.route('/clear', methods=['GET'])
def clear():
    global calculation_log
    calculation_log.clear()
    return redirect('/')
