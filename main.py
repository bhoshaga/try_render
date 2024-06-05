from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Flight path dictionaries
flight_paths = {
    "flight_1": {
        "origin": "San Francisco (SFO)",
        "destination": "Toronto (YYZ)",
        "flight_time": "4 hours 30 minutes",
        "img_flight_time": "2 hours 15 minutes",
        "img_url": "https://i.pinimg.com/1200x/40/bb/a9/40bba9c6235d52f02f61e4a8ac9d59bb.jpg",
        "progress_bar_completion": "50%",
        "correct_answer": "lakegeneva"
    },
    "flight_2": {
        "origin": "New York (JFK)",
        "destination": "London (LHR)",
        "flight_time": "7 hours",
        "img_flight_time": "4 hours",
        "img_url": "https://i.pinimg.com/originals/bb/18/0d/bb180ddf9e0d9e69f8700c5f7df86dd0.jpg",
        "progress_bar_completion": "57%",
        "correct_answer": "towerbridge"
    },
    "flight_3": {
        "origin": "Los Angeles (LAX)",
        "destination": "Tokyo (NRT)",
        "flight_time": "11 hours 30 minutes",
        "img_flight_time": "6 hours",
        "img_url": "https://i.pinimg.com/originals/13/ca/5c/13ca5cc6ff5ee5537ff5b8bbdb11e1f1.jpg",
        "progress_bar_completion": "52%",
        "correct_answer": "mountfuji"
    },
    "flight_4": {
        "origin": "Sydney (SYD)",
        "destination": "Dubai (DXB)",
        "flight_time": "14 hours",
        "img_flight_time": "7 hours",
        "img_url": "https://i.pinimg.com/originals/23/bb/76/23bb76431ac89d53279d1db8821a71cf.jpg",
        "progress_bar_completion": "50%",
        "correct_answer": "dubai"
    },
    "flight_5": {
        "origin": "Singapore (SIN)",
        "destination": "San Francisco (SFO)",
        "flight_time": "16 hours 30 minutes",
        "img_flight_time": "15 hours 30 minutes",
        "img_url": "https://i.pinimg.com/736x/33/94/25/3394253154be33fabc240f72fcc989a5.jpg",
        "progress_bar_completion": "95%",
        "correct_answer": "sanfrancisco"
    }
}

@app.get("/", response_class=HTMLResponse)
async def get_home():
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
            .flight-button { margin: 10px; padding: 10px 20px; font-size: 16px; cursor: pointer; }
            .image { max-width: 300px; height: 350px; object-fit: cover; border-radius: 20px; display: none; margin: 0 auto; }
            .guess-box { margin-top: 20px; }
            .wordle-box { display: flex; justify-content: center; margin-top: 20px; }
            .wordle-box input { width: 40px; height: 40px; font-size: 24px; text-align: center; margin: 2px; text-transform: uppercase; }
            .timer { font-size: 24px; margin-top: 20px; display: none; }
            .animate__animated { animation-duration: 1s; }
            .correct { color: green; font-size: 32px; }
            .incorrect { color: #FF5A5F; font-size: 24px; }
            .flight-path { font-size: 18px; margin-bottom: 20px; display: none; }
            .progress-bar { width: 40%; height: 2px; background-color: #f3f3f3; border-radius: 13px; overflow: hidden; margin: 20px auto; display: none; }
            .progress-bar-fill { height: 100%; background-color: #4caf50; }
            .restart-btn { display: none; margin-top: 20px; padding: 10px 20px; font-size: 16px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Window Seat</h1>
        <h2>Guess the Location</h2>
        <p>Select a flight path and guess the location or structure visible from the window seat.</p>
        <button class="flight-button" onclick="startFlight('flight_1')">Flight 1</button>
        <button class="flight-button" onclick="startFlight('flight_2')">Flight 2</button>
        <button class="flight-button" onclick="startFlight('flight_3')">Flight 3</button>
        <button class="flight-button" onclick="startFlight('flight_4')">Flight 4</button>
        <button class="flight-button" onclick="startFlight('flight_5')">Flight 5</button>
        <div id="flight-details"></div>
        <form class="guess-box" method="post" action="/guess" id="guess-form" style="display: none;">
            <div class="wordle-box" id="wordle-box">
                <!-- Input fields will be inserted here dynamically -->
            </div>
            <input type="hidden" name="guess_count" id="guess_count" value="5">
            <input type="hidden" name="flight_key" id="flight_key" value="">
            <button type="submit">Submit</button>
        </form>
        <div class="result" id="result"></div>
        <div class="timer" id="timer"></div>
        <div class="guess-counter">Guesses remaining: <span id="guessCount">5</span></div>
        <button class="restart-btn" onclick="restartGame()" id="restart-btn">Restart</button>
        <script>
            let flightData = {};
            let timerInterval;
            let remainingTime = 300; // 5 minutes in seconds

            function startFlight(flightKey) {
                flightData = { ...flightPaths[flightKey] };
                document.getElementById("flight-details").innerHTML = `
                    <div class="flight-path">
                        ${flightData.origin} --------- ✈ --------- ${flightData.destination} <br>
                        Flight time: ${flightData.flight_time} <br>
                        Image taken at ${flightData.img_flight_time} into the flight
                    </div>
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: ${flightData.progress_bar_completion};"></div>
                    </div>
                    <img src="${flightData.img_url}" class="image" alt="Window Seat View">
                `;
                document.querySelector('.flight-path').style.display = 'block';
                document.querySelector('.progress-bar').style.display = 'block';
                document.querySelector('.image').style.display = 'block';
                document.getElementById('guess-form').style.display = 'block';
                document.getElementById('flight_key').value = flightKey;
                generateWordleBox(flightData.correct_answer.length);
                startTimer();
            }

            function generateWordleBox(length) {
                const wordleBox = document.getElementById('wordle-box');
                wordleBox.innerHTML = '';
                for (let i = 0; i < length; i++) {
                    wordleBox.innerHTML += `<input type="text" name="letter${i}" maxlength="1" oninput="moveFocus(this, ${i})" onkeydown="handleKeyDown(event, ${i})">`;
                }
            }

            function moveFocus(currentInput, index) {
                if (currentInput.value.length >= 1) {
                    const nextInput = document.querySelector(`input[name='letter${index + 1}']`);
                    if (nextInput) {
                        nextInput.focus();
                    }
                }
            }

            function handleKeyDown(event, index) {
                const prevInput = document.querySelector(`input[name='letter${index - 1}']`);
                const nextInput = document.querySelector(`input[name='letter${index + 1}']`);

                if (event.key === "ArrowLeft" && prevInput) {
                    prevInput.focus();
                } else if (event.key === "ArrowRight" && nextInput) {
                    nextInput.focus();
                } else if (event.key === "Backspace" && event.target.value === "" && prevInput) {
                    prevInput.focus();
                }
            }

            let guessCount = 5;

            function decrementGuessCount() {
                guessCount--;
                document.getElementById('guessCount').textContent = guessCount;
                if (guessCount <= 0) {
                    document.querySelector('form').style.display = 'none';
                    document.getElementById('restart-btn').style.display = 'inline-block';
                }
            }

            function restartGame() {
                window.location.href = "/";
            }

            function startTimer() {
                remainingTime = 300;
                document.getElementById('timer').style.display = 'block';
                clearInterval(timerInterval);
                timerInterval = setInterval(updateTimer, 1000);
            }

            function updateTimer() {
                const minutes = Math.floor(remainingTime / 60);
                const seconds = remainingTime % 60;
                document.getElementById('timer').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
                remainingTime--;

                if (remainingTime < 0) {
                    clearInterval(timerInterval);
                    document.getElementById('timer').textContent = "Time's up!";
                    document.querySelector('form').style.display = 'none';
                    document.getElementById('restart-btn').style.display = 'inline-block';
                }
            }

            const flightPaths = {
                "flight_1": {
                    "origin": "San Francisco (SFO)",
                    "destination": "Toronto (YYZ)",
                    "flight_time": "4 hours 30 minutes",
                    "img_flight_time": "2 hours 15 minutes",
                    "img_url": "https://i.pinimg.com/1200x/40/bb/a9/40bba9c6235d52f02f61e4a8ac9d59bb.jpg",
                    "progress_bar_completion": "50%",
                    "correct_answer": "lakegeneva"
                },
                "flight_2": {
                    "origin": "New York (JFK)",
                    "destination": "London (LHR)",
                    "flight_time": "7 hours",
                    "img_flight_time": "4 hours",
                    "img_url": "https://i.pinimg.com/originals/bb/18/0d/bb180ddf9e0d9e69f8700c5f7df86dd0.jpg",
                    "progress_bar_completion": "57%",
                    "correct_answer": "towerbridge"
                },
                "flight_3": {
                    "origin": "Los Angeles (LAX)",
                    "destination": "Tokyo (NRT)",
                    "flight_time": "11 hours 30 minutes",
                    "img_flight_time": "6 hours",
                    "img_url": "https://i.pinimg.com/originals/13/ca/5c/13ca5cc6ff5ee5537ff5b8bbdb11e1f1.jpg",
                    "progress_bar_completion": "52%",
                    "correct_answer": "mountfuji"
                },
                "flight_4": {
                    "origin": "Sydney (SYD)",
                    "destination": "Dubai (DXB)",
                    "flight_time": "14 hours",
                    "img_flight_time": "7 hours",
                    "img_url": "https://i.pinimg.com/originals/23/bb/76/23bb76431ac89d53279d1db8821a71cf.jpg",
                    "progress_bar_completion": "50%",
                    "correct_answer": "dubai"
                },
                "flight_5": {
                    "origin": "Singapore (SIN)",
                    "destination": "San Francisco (SFO)",
                    "flight_time": "16 hours 30 minutes",
                    "img_flight_time": "15 hours 30 minutes",
                    "img_url": "https://i.pinimg.com/736x/33/94/25/3394253154be33fabc240f72fcc989a5.jpg",
                    "progress_bar_completion": "95%",
                    "correct_answer": "sanfrancisco"
                }
            };
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/guess", response_class=HTMLResponse)
async def make_guess(
    request: Request,
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
    guess_count: int = Form(...),
    flight_key: str = Form("")
):
    correct_answer = flight_paths[flight_key]["correct_answer"]
    guess = f"{letter0}{letter1}{letter2}{letter3}{letter4}{letter5}{letter6}{letter7}{letter8}{letter9}".lower()
    guess = guess[:len(correct_answer)]  # Truncate guess to the correct length
    if guess == correct_answer:
        result = "Correct! Congratulations!"
        result_class = "correct animate__animated animate__bounceIn"
        guess_count_message = ""
        timer_interval_clear = "clearInterval(timerInterval);"
        form_display = "none"
        restart_button_display = "inline-block"
    else:
        result = "Incorrect. Try again!"
        result_class = "incorrect animate__animated animate__shakeX"
        guess_count -= 1
        guess_count_message = f"Guesses remaining: <span id='guessCount'>{guess_count}</span>"
        timer_interval_clear = ""
        form_display = "block"
        restart_button_display = "none"
        if guess_count <= 0:
            form_display = "none"
            restart_button_display = "inline-block"

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
            .image {{ max-width: 300px; height: 350px; object-fit: cover; border-radius: 20px; margin: 0 auto; }}
            .guess-box {{ margin-top: 20px; }}
            .wordle-box {{ display: flex; justify-content: center; margin-top: 20px; }}
            .wordle-box input {{ width: 40px; height: 40px; font-size: 24px; text-align: center; margin: 2px; text-transform: uppercase; }}
            .timer {{ font-size: 24px; margin-top: 20px; }}
            .animate__animated {{ animation-duration: 1s; }}
            .correct {{ color: green; font-size: 32px; }}
            .incorrect {{ color: #FF5A5F; font-size: 24px; }}
            .flight-path {{ font-size: 18px; margin-bottom: 20px; }}
            .progress-bar {{ width: 40%; height: 2px; background-color: #f3f3f3; border-radius: 13px; overflow: hidden; margin: 20px auto; }}
            .progress-bar-fill {{ height: 100%; background-color: #4caf50; width: {flight_paths[flight_key]['progress_bar_completion']}; }} /* Adjust width as needed */
            .restart-btn {{ display: {restart_button_display}; margin-top: 20px; padding: 10px 20px; font-size: 16px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>Window Seat</h1>
        <h2>Guess the Location</h2>
        <div class="flight-path">
            {flight_paths[flight_key]["origin"]} --------- ✈ --------- {flight_paths[flight_key]["destination"]} <br>
            Flight time: {flight_paths[flight_key]["flight_time"]} <br>
            Image taken at {flight_paths[flight_key]["img_flight_time"]} into the flight
        </div>
        <div class="progress-bar">
            <div class="progress-bar-fill"></div>
        </div>
        <img src="{flight_paths[flight_key]['img_url']}" class="image" alt="Window Seat View">
        <form class="guess-box" method="post" action="/guess" style="display: {form_display}">
            <div class="wordle-box">
                {''.join([f'<input type="text" name="letter{i}" maxlength="1" oninput="moveFocus(this, {i})" onkeydown="handleKeyDown(event, {i})">' for i in range(len(flight_paths[flight_key]["correct_answer"]))])}
            </div>
            <input type="hidden" name="guess_count" value="{guess_count}">
            <input type="hidden" name="flight_key" value="{flight_key}">
            <button type="submit">Submit</button>
        </form>
        <div class="result {result_class}">{result}</div>
        <div class="timer" id="timer"></div>
        <div class="guess-counter">{guess_count_message}</div>
        <button class="restart-btn" onclick="restartGame()" id="restart-btn">Restart</button>
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
                    document.getElementById('restart-btn').style.display = 'inline-block';
                }}
            }}

            function restartGame() {{
                window.location.href = "/";
            }}

            const timer = document.getElementById('timer');
            let remainingTime = 300; // 5 minutes in seconds

            function startTimer() {{
                remainingTime = 300;
                document.getElementById('timer').style.display = 'block';
                clearInterval(timerInterval);
                timerInterval = setInterval(updateTimer, 1000);
            }}

            function updateTimer() {{
                const minutes = Math.floor(remainingTime / 60);
                const seconds = remainingTime % 60;
                timer.textContent = `${{minutes}}:${{seconds.toString().padStart(2, '0')}}`;
                remainingTime--;

                if (remainingTime < 0) {{
                    clearInterval(timerInterval);
                    timer.textContent = "Time's up!";
                    document.querySelector('form').style.display = 'none';
                    document.getElementById('restart-btn').style.display = 'inline-block';
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
