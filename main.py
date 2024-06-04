from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
from datetime import datetime
import uvicorn

app = FastAPI()

chefs = ["Chef Gordon", "Chef Jamie", "Chef Nigella"]
stoves = [{"dish": None, "order_id": None} for _ in range(4)]
chef_status = {chef: "idle" for chef in chefs}

order_queue = asyncio.Queue()

async def assign_order_to_chef(websocket):
    while True:
        order = await order_queue.get()
        for i, chef in enumerate(chefs):
            if chef_status[chef] == "idle":
                for j, stove in enumerate(stoves):
                    if not stove["dish"]:
                        chef_status[chef] = "cooking"
                        stoves[j]["dish"] = order["dish"]
                        stoves[j]["order_id"] = order["order_id"]
                        asyncio.create_task(cook_dish(websocket, order["dish"], order["order_id"], chef, j))
                        break
                else:
                    continue
                break
        else:
            order_queue.put_nowait(order)
        await asyncio.sleep(1)

async def cook_dish(websocket, dish, order_id, chef, stove_num):
    await websocket.send_text(f"<div><strong>Order {order_id}:</strong> Assigned to {chef} on Stove {stove_num + 1}</div>")
    if dish == 'mee_goreng':
        await cook_mee_goreng(websocket, order_id, chef)
    elif dish == 'butter_chicken':
        await cook_butter_chicken(websocket, order_id, chef)
    elif dish == 'dosa':
        await cook_dosa(websocket, order_id, chef)
    stoves[stove_num]["dish"] = None
    stoves[stove_num]["order_id"] = None
    chef_status[chef] = "idle"
    await websocket.send_text(f"<div><strong>Order {order_id}:</strong> Completed by {chef}</div>")

async def chef_step(step_name: str, duration: int, websocket: WebSocket, chef: str, order_id: str, step_num: int, total_steps: int, color: str):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await websocket.send_text(f"<div style='color: {color};'><strong>Order {order_id} - {chef}:</strong> Step {step_num}/{total_steps} - Started {step_name} at {start_time}.</div>")
    await asyncio.sleep(duration)
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await websocket.send_text(f"<div style='color: {color};'><strong>Order {order_id} - {chef}:</strong> Step {step_num}/{total_steps} - Completed {step_name} at {end_time}.</div>")
    await asyncio.sleep(0.5)  # Half-second delay between steps

async def cook_mee_goreng(websocket: WebSocket, order_id: str, chef: str):
    total_steps = 5
    color = "orange"
    await chef_step("cutting vegetables for Mee Goreng", 3, websocket, chef, order_id, 1, total_steps, color)
    await chef_step("boiling noodles for Mee Goreng", 4, websocket, chef, order_id, 2, total_steps, color)
    await chef_step("frying noodles for Mee Goreng", 5, websocket, chef, order_id, 3, total_steps, color)
    await chef_step("adding sauce for Mee Goreng", 2, websocket, chef, order_id, 4, total_steps, color)
    await chef_step("serving Mee Goreng", 1, websocket, chef, order_id, 5, total_steps, color)

async def cook_butter_chicken(websocket: WebSocket, order_id: str, chef: str):
    total_steps = 5
    color = "green"
    await chef_step("marinating chicken for Butter Chicken", 3, websocket, chef, order_id, 1, total_steps, color)
    await chef_step("cooking chicken for Butter Chicken", 4, websocket, chef, order_id, 2, total_steps, color)
    await chef_step("preparing sauce for Butter Chicken", 5, websocket, chef, order_id, 3, total_steps, color)
    await chef_step("mixing chicken and sauce for Butter Chicken", 2, websocket, chef, order_id, 4, total_steps, color)
    await chef_step("serving Butter Chicken", 1, websocket, chef, order_id, 5, total_steps, color)

async def cook_dosa(websocket: WebSocket, order_id: str, chef: str):
    total_steps = 5
    color = "blue"
    await chef_step("soaking rice and lentils for Dosa", 3, websocket, chef, order_id, 1, total_steps, color)
    await chef_step("grinding batter for Dosa", 2, websocket, chef, order_id, 2, total_steps, color)
    await chef_step("fermenting batter for Dosa", 5, websocket, chef, order_id, 3, total_steps, color)
    await chef_step("making dosa on pan", 3, websocket, chef, order_id, 4, total_steps, color)
    await chef_step("adding fillings to Dosa", 2, websocket, chef, order_id, 5, total_steps, color)

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Cooking Progress</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; display: flex; }
                h1, h2 { color: #333; }
                button { margin: 5px; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
                #progress, .orders { padding: 20px; border: 1px solid #ccc; border-radius: 5px; background: #f9f9f9; }
                #progress { flex: 1; margin-right: 20px; overflow-y: auto; max-height: 400px; }
                .step { margin: 10px 0; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background: #fff; }
                .orders { width: 30%; }
                .orders ul { list-style-type: none; padding: 0; }
                .orders li { margin: 5px 0; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background: #fff; }
                .stoves { display: flex; justify-content: space-around; margin-top: 20px; }
                .stove { width: 150px; height: 150px; border: 2px solid #333; border-radius: 5px; background: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: bold; }
                .stove .dish { font-size: 14px; margin-top: 5px; }
                .chef-status { margin-top: 20px; }
                .chef-status p { margin: 5px 0; }
            </style>
        </head>
        <body>
            <div>
                <h1>Cooking Progress</h1>
                <button onclick="startCooking('mee_goreng')">Start Mee Goreng</button>
                <button onclick="startCooking('butter_chicken')">Start Butter Chicken</button>
                <button onclick="startCooking('dosa')">Start Dosa</button>
                <div id="progress"></div>
                <div class="stoves">
                    <div class="stove" id="stove1">
                        <div>Stove 1</div>
                        <div class="dish" id="stove1-dish"></div>
                    </div>
                    <div class="stove" id="stove2">
                        <div>Stove 2</div>
                        <div class="dish" id="stove2-dish"></div>
                    </div>
                    <div class="stove" id="stove3">
                        <div>Stove 3</div>
                        <div class="dish" id="stove3-dish"></div>
                    </div>
                    <div class="stove" id="stove4">
                        <div>Stove 4</div>
                        <div class="dish" id="stove4-dish"></div>
                    </div>
                </div>
                <div class="chef-status">
                    <h2>Chef Status</h2>
                    <p><strong>Chef Gordon:</strong> <span id="chef-gordon-status">idle</span></p>
                    <p><strong>Chef Jamie:</strong> <span id="chef-jamie-status">idle</span></p>
                    <p><strong>Chef Nigella:</strong> <span id="chef-nigella-status">idle</span></p>
                </div>
            </div>
            <div class="orders">
                <h2>Order Queue</h2>
                <ul id="order-queue"></ul>
                <h2>Completed Orders</h2>
                <ul id="completed-orders"></ul>
            </div>
            <script>
                let ws = new WebSocket("wss://try-render-bzt9.onrender.com/ws");
                let orderCounters = {
                    mee_goreng: 0,
                    butter_chicken: 0,
                    dosa: 0
                };

                function startCooking(dish) {
                    orderCounters[dish] += 1;
                    const orderId = `${dish.toUpperCase()}-${String(orderCounters[dish]).padStart(3, '0')}`;
                    document.getElementById('order-queue').innerHTML += `<li id="${orderId}">${orderId}</li>`;
                    ws.send(JSON.stringify({ dish, orderId }));
                }

                ws.onmessage = function(event) {
                    const progressDiv = document.getElementById('progress');
                    const stepDiv = document.createElement('div');
                    stepDiv.className = 'step';
                    stepDiv.innerHTML = event.data;
                    progressDiv.insertBefore(stepDiv, progressDiv.firstChild);

                    // Move to completed orders if final step
                    if (event.data.includes("Completed by")) {
                        const orderId = event.data.match(/Order (.+?):/)[1];
                        const orderElem = document.getElementById(orderId);
                        if (orderElem) {
                            orderElem.parentNode.removeChild(orderElem);
                            document.getElementById('completed-orders').innerHTML += `<li>${orderId}</li>`;
                        }
                    }

                    // Update stove status
                    if (event.data.includes("Assigned to")) {
                        const stoveNum = event.data.match(/Stove (\d+)/)[1];
                        const orderId = event.data.match(/Order (.+?):/)[1];
                        document.getElementById(`stove${stoveNum}-dish`).textContent = orderId;
                    }

                    // Clear stove status when completed
                    if (event.data.includes("Completed by")) {
                        const orderId = event.data.match(/Order (.+?):/)[1];
                        for (let i = 1; i <= 4; i++) {
                            const stoveDish = document.getElementById(`stove${i}-dish`);
                            if (stoveDish.textContent === orderId) {
                                stoveDish.textContent = "";
                                break;
                            }
                        }
                    }

                    // Update chef status
                    if (event.data.includes("Chef Gordon")) {
                        document.getElementById('chef-gordon-status').textContent = event.data.includes("Started") ? "cooking" : "idle";
                    } else if (event.data.includes("Chef Jamie")) {
                        document.getElementById('chef-jamie-status').textContent = event.data.includes("Started") ? "cooking" : "idle";
                    } else if (event.data.includes("Chef Nigella")) {
                        document.getElementById('chef-nigella-status').textContent = event.data.includes("Started") ? "cooking" : "idle";
                    }
                };
            </script>
        </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    asyncio.create_task(assign_order_to_chef(websocket))
    try:
        while True:
            data = await websocket.receive_json()
            dish = data['dish']
            order_id = data['orderId']
            await order_queue.put({"dish": dish, "order_id": order_id})
    except WebSocketDisconnect:
        print("Client disconnected")

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)