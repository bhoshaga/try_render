from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Window Seat Game</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        h1 { margin-bottom: 0; }
        h2 { margin-top: 5px; }
        .image { max-width: 600px; height: auto; }
        .guess-box { margin-top: 20px; }
        .wordle-box { display: flex; justify-content: center; margin-top: 20px; }
        .wordle-box input { width: 40px; height: 40px; font-size: 24px; text-align: center; margin: 2px; text-transform: uppercase; }
        .timer { font-size: 24px; margin-top: 20px; }
        .animate__animated { animation-duration: 1s; }
    </style>
</head>
<body>
    <h1>Window Seat</h1>
    <h2>Guess the Location</h2>
    <img src="https://i.pinimg.com/1200x/40/bb/a9/40bba9c6235d52f02f61e4a8ac9d59bb.jpg" class="image" alt="Window Seat View">
    <form class="guess-box" method="post" action="/guess">
        <div class="wordle-box">
            {% for i in range(10) %}
            <input type="text" name="letter{{ i }}" maxlength="1">
            {% endfor %}
        </div>
        <button type="submit">Submit</button>
    </form>
    {% if result %}
        <p class="{% if correct %}animate__animated animate__bounceIn{% endif %}">{{ result }}</p>
    {% endif %}
    <div class="timer"></div>

    <script>
        const timer = document.querySelector('.timer');
        let remainingTime = 300; // 5 minutes in seconds

        function updateTimer() {
            const minutes = Math.floor(remainingTime / 60);
            const seconds = remainingTime % 60;
            timer.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            remainingTime--;

            if (remainingTime < 0) {
                clearInterval(timerInterval);
                timer.textContent = "Time's up!";
                document.querySelector('form').style.display = 'none';
            }
        }

        const timerInterval = setInterval(updateTimer, 1000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_home():
    return html_content

@app.post("/guess", response_class=HTMLResponse)
async def make_guess(request: Request, **kwargs):
    correct_answer = "lakegeneva"
    guess = "".join(kwargs.values()).lower()
    result = "Correct!" if guess == correct_answer else "Try again!"
    correct = result == "Correct!"
    return html_content.replace("{% if result %}", "{% if True %}").replace("{{ result }}", result).replace("{% if correct %}", f"{% if {correct} %}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)