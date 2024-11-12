from flask import Flask, render_template_string, request, url_for 

# Initialize the Flask app
app = Flask(__name__)

# HTML Template with embedded CSS and logo
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uptime Calculator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background-color: #f5f7fa; color: #333; display: flex; justify-content: center; align-items: center; height: 100vh; position: relative; }
        /* Logo styling */
        .logo {
            position: absolute;
            top: 10px;
            left: 10px;
            width: 250px;
            opacity: 0.5;
        }
        .container { background-color: #ffffff; padding: 20px 30px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; max-width: 400px; width: 100%; text-align: center; }
        h1 { font-size: 24px; margin-bottom: 20px; color: #333; }
        label { display: block; margin: 15px 0 5px; font-weight: bold; color: #555; }
        input[type="text"], input[type="number"] { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
        button[type="submit"] { margin-top: 20px; padding: 10px 20px; background-color: #007bff; border: none; border-radius: 4px; color: white; font-size: 16px; cursor: pointer; transition: background-color 0.3s ease; }
        button[type="submit"]:hover { background-color: #0056b3; }
        h2 { margin-top: 20px; font-size: 20px; color: #28a745; }
        h2.error { color: #dc3545; }
    </style>
</head>
<body>
    <img src="{{ url_for('static', filename='308127134_462010532634136_872831273523556089_n.jpg') }}" alt="Transnet Logo" class="logo">
    <div class="container">
        <h1>Uptime Calculator</h1>
        <form method="POST">
            <label for="year">Year:</label>
            <input type="text" id="year" name="year" required>
            <label for="month">Month:</label>
            <input type="text" id="month" name="month" required>
            <label for="downtime">Downtime (minutes):</label>
            <input type="number" id="downtime" name="downtime" required>
            <button type="submit">Calculate Uptime</button>
        </form>
        {% if result %}
            <h2>{{ result }}</h2>
        {% elif error %}
            <h2 class="error">Error: {{ error }}</h2>
        {% endif %}
    </div>
</body>
</html>
"""

# Backend Logic
def get_total_minutes(month, is_leap_year):
    months_minutes = {
        "January": 44640, "February": 41760 if is_leap_year else 40320,
        "March": 44640, "April": 43200, "May": 44640, "June": 43200,
        "July": 44640, "August": 44640, "September": 43200,
        "October": 44640, "November": 43200, "December": 44640
    }
    return months_minutes.get(month, "Invalid month")

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Flask route
@app.route("/", methods=["GET", "POST"])
def uptime_calculator():
    result = None
    error = None

    if request.method == "POST":
        try:
            year = int(request.form["year"])
            month = request.form["month"].capitalize()
            downtime = int(request.form["downtime"])
            
            leap_year = is_leap_year(year)
            total_minutes = get_total_minutes(month, leap_year)
            
            if isinstance(total_minutes, str):  # Error if invalid month
                raise ValueError(total_minutes)
                
            # Calculate uptime
            total_uptime = (total_minutes - downtime) * 100 / total_minutes
            result = f"Total GCOS Uptime for {month} {year}: {total_uptime:.2f}%"
        
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = "An error occurred. Please check your inputs."

    return render_template_string(html_template, result=result, error=error)


app.run(host="0.0.0.0", port=5000)
