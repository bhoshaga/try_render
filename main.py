from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Use this URL when deploying to Render
render_url = "https://try-render-bzt9.onrender.com"

# Use this URL when testing on localhost
localhost_url = "http://localhost:8000"

# Choose the appropriate URL by uncommenting the desired line
# base_url = localhost_url
base_url = render_url

# Image link for the window seat view
image_link = "https://i.pinimg.com/1200x/40/bb/a9/40bba9c6235d52f02f61e4a8ac9d59bb.jpg"

@app.get("/", response_class=HTMLResponse)
async def get_home():
    guess_count = 5
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Window Seat Game</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; }}
            h1 {{ margin-bottom: 0; }}
            h2 {{ margin-top: 5px; }}
            .image {{ max-width: 300px; height: 350px; object-fit: cover; border-radius: 20px; }}
            .guess-box {{ margin-top: 20px; }}
            .wordle-box {{ display: flex; justify-content: center; margin-top: 20px; }}
            .wordle-box input {{ width: 40px; height: 40px; font-size: 24px; text-align: center; margin: 2px; text-transform: uppercase; }}
            .timer {{ font-size: 24px; margin-top: 20px; }}
            .animate__animated {{ animation-duration: 1s; }}
            .correct {{ color: green; font-size: 32px; }}
            .incorrect {{ color: #FF5A5F; font-size: 24px; }}
            .flight-path {{ font-size: 18px; margin-bottom: 20px; }}
            .progress-bar {{ width: 40%; height: 2px; background-color: #f3f3f3; border-radius: 13px; overflow: hidden; margin: 20px auto; }}
            .progress-bar-fill {{ height: 100%; background-color: #4caf50; width: 50%; }} /* Adjust width as needed */
        </style>
    </head>
    <body>
        <h1>Window Seat</h1>
        <h2>Guess the Location</h2>
        <div class="flight-path">
            San Francisco (SFO) --------- ✈ --------- Toronto (YYZ) <br>
            Flight time: 4 hours 30 minutes <br>
            Image taken at 2 hours 15 minutes into the flight
        </div>
        <div class="progress-bar">
            <div class="progress-bar-fill"></div>
        </div>
        <img src="{image_link}" class="image" alt="Window Seat View">
        <form class="guess-box" method="post" action="/guess">
            <div class="wordle-box">
                {''.join([f'<input type="text" name="letter{i}" maxlength="1" oninput="moveFocus(this, {i})" onkeydown="handleKeyDown(event, {i})">' for i in range(10)])}
            </div>
            <input type="hidden" name="guess_count" value="{guess_count}">
            <button type="submit">Submit</button>
        </form>
        <div class="result"></div>
        <div class="timer"></div>
        <div class="guess-counter">Guesses remaining: <span id="guessCount">{guess_count}</span></div>
        <script>
            function moveFocus(currentInput, index) {{
                if (currentInput.value.length >= 1) {{
                    const nextInput = document.querySelector(`input[name='letter${{index + 1}}']`);
                    if (nextInput) {{
                        nextInput.focus();
                    }}
                }}
            }}

            function handleKeyDown(event, index) {{
                const prevInput = document.querySelector(`input[name='letter${{index - 1}}']`);
                const nextInput = document.querySelector(`input[name='letter${{index + 1}}']`);

                if (event.key === "ArrowLeft" && prevInput) {{
                    prevInput.focus();
                }} else if (event.key === "ArrowRight" && nextInput) {{
                    nextInput.focus();
                }} else if (event.key === "Backspace" && event.target.value === "" && prevInput) {{
                    prevInput.focus();
                }}
            }}

            let guessCount = {guess_count};

            function decrementGuessCount() {{
                guessCount--;
                document.getElementById('guessCount').textContent = guessCount;
                if (guessCount <= 0) {{
                    document.querySelector('form').style.display = 'none';
                }}
            }}

            const timer = document.querySelector('.timer');
            let remainingTime = 300; // 5 minutes in seconds

            function updateTimer() {{
                const minutes = Math.floor(remainingTime / 60);
                const seconds = remainingTime % 60;
                timer.textContent = `${{minutes}}:${{seconds.toString().padStart(2, '0')}}`;
                remainingTime--;

                if (remainingTime < 0) {{
                    clearInterval(timerInterval);
                    timer.textContent = "Time's up!";
                    document.querySelector('form').style.display = 'none';
                }}
            }}

            const timerInterval = setInterval(updateTimer, 1000);
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/guess", response_class=HTMLResponse)
async def make_guess(
    letter0: str = Form(""),
    letter1: str = Form(""),
    letter2: str = Form(""),
    letter3: str = Form(""),
    letter4: str = Form(""),
    letter5: str = Form(""),
    letter6: str = Form(""),
    letter7: str = Form(""),
    letter8: str = Form(""),
    letter9: str = Form(""),
    guess_count: int = Form(...)
):
    correct_answer = "lakegeneva"
    guess = f"{letter0}{letter1}{letter2}{letter3}{letter4}{letter5}{letter6}{letter7}{letter8}{letter9}".lower()
    if guess == correct_answer:
        result = "Correct! Congratulations!"
        result_class = "correct animate__animated animate__bounceIn"
        guess_count_message = ""
        timer_interval_clear = "clearInterval(timerInterval);"
        form_display = "none"
    else:
        result = "Incorrect. Try again!"
        result_class = "incorrect animate__animated animate__shakeX"
        guess_count -= 1
        guess_count_message = f"Guesses remaining: <span id='guessCount'>{guess_count}</span>"
        timer_interval_clear = ""
        form_display = "block"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Window Seat Game</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; }}
            h1 {{ margin-bottom: 0; }}
            h2 {{ margin-top: 5px; }}
            .image {{ max-width: 300px; height: 350px; object-fit: cover; border-radius: 20px; }}
            .guess-box {{ margin-top: 20px; }}
            .wordle-box {{ display: flex; justify-content: center; margin-top: 20px; }}
            .wordle-box input {{ width: 40px; height: 40px; font-size: 24px; text-align: center; margin: 2px; text-transform: uppercase; }}
            .timer {{ font-size: 24px; margin-top: 20px; }}
            .animate__animated {{ animation-duration: 1s; }}
            .correct {{ color: green; font-size: 32px; }}
            .incorrect {{ color: #FF5A5F; font-size: 24px; }}
            .flight-path {{ font-size: 18px; margin-bottom: 20px; }}
            .progress-bar {{ width: 40%; height: 2px; background-color: #f3f3f3; border-radius: 13px; overflow: hidden; margin: 20px auto; }}
            .progress-bar-fill {{ height: 100%; background-color: #4caf50; width: 50%; }} /* Adjust width as needed */
        </style>
    </head>
    <body>
        <h1>Window Seat</h1>
        <h2>Guess the Location</h2>
        <div class="flight-path">
            San Francisco (SFO) --------- ✈ --------- Toronto (YYZ) <br>
            Flight time: 4 hours 30 minutes <br>
            Image taken at 2 hours 15 minutes into the flight
        </div>
        <div class="progress-bar">
            <div class="progress-bar-fill"></div>
        </div>
        <img src="{image_link}" class="image" alt="Window Seat View">
        <form class="guess-box" method="post" action="/guess" style="display: {form_display}">
            <div class="wordle-box">
                {''.join([f'<input type="text" name="letter{i}" maxlength="1" oninput="moveFocus(this, {i})" onkeydown="handleKeyDown(event, {i})">' for i in range(10)])}
            </div>
            <input type="hidden" name="guess_count" value="{guess_count}">
            <button type="submit">Submit</button>
        </form>
        <div class="result {result_class}">{result}</div>
        <div class="timer"></div>
        <div class="guess-counter">{guess_count_message}</div>
        <script>
            function moveFocus(currentInput, index) {{
                if (currentInput.value.length >= 1) {{
                    const nextInput = document.querySelector(`input[name='letter${{index + 1}}']`);
                    if (nextInput) {{
                        nextInput.focus();
                    }}
                }}
            }}

            function handleKeyDown(event, index) {{
                const prevInput = document.querySelector(`input[name='letter${{index - 1}}']`);
                const nextInput = document.querySelector(`input[name='letter${{index + 1}}']`);

                if (event.key === "ArrowLeft" && prevInput) {{
                    prevInput.focus();
                }} else if (event.key === "ArrowRight" && nextInput) {{
                    nextInput.focus();
                }} else if (event.key === "Backspace" && event.target.value === "" && prevInput) {{
                    prevInput.focus();
                }}
            }}

            let guessCount = {guess_count};

            function decrementGuessCount() {{
                guessCount--;
                document.getElementById('guessCount').textContent = guessCount;
                if (guessCount <= 0) {{
                    document.querySelector('form').style.display = 'none';
                }}
            }}

            const timer = document.querySelector('.timer');
            let remainingTime = 300; // 5 minutes in seconds

            function updateTimer() {{
                const minutes = Math.floor(remainingTime / 60);
                const seconds = remainingTime % 60;
                timer.textContent = `${{minutes}}:${{seconds.toString().padStart(2, '0')}}`;
                remainingTime--;

                if (remainingTime < 0) {{
                    clearInterval(timerInterval);
                    timer.textContent = "Time's up!";
                    document.querySelector('form').style.display = 'none';
                }}
            }}

            const timerInterval = setInterval(updateTimer, 1000);

            if ("{guess}" !== "{correct_answer}") {{
                decrementGuessCount();
            }} else {{
                {timer_interval_clear}
            }}
        </script>
    </body>
    </html>
    """
    return html_content

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
