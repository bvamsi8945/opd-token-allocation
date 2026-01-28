🏥 OPD Token Allocation Engine
📌 Overview

This project is a backend service for hospital OPD token management, built using FastAPI.
It simulates how hospitals allocate OPD tokens to patients while handling real-world scenarios such as:

Limited doctor capacity per time slot

Multiple booking sources

Priority patients (Paid / Emergency)

Token cancellations

Dynamic replacement of low-priority tokens

The system exposes APIs that can be tested and verified using Swagger UI.

🎯 Problem Statement

Hospitals run OPDs in fixed time slots (for example: 9–10 AM).
Each doctor can handle only a limited number of patients per slot.

Patients can arrive through different channels:

Walk-in

Online booking

Follow-up visits

Paid priority patients

Emergency patients

The challenge is to:

Respect slot capacity

Prioritize critical patients

Replace low-priority tokens when emergencies arrive

Handle cancellations cleanly

🧠 Solution Approach
Key Design Decisions

Each Doctor has multiple Slots

Each Slot has a fixed capacity

Each booking creates a Token

Tokens are sorted by:

Priority

Arrival time

Priority Order

From lowest to highest:

WALK_IN

ONLINE

FOLLOW_UP

PAID

EMERGENCY

When a slot is full:

A higher-priority token can replace the lowest-priority existing token

If priority is lower, booking is rejected

⚙️ Technology Stack

Python

FastAPI

Uvicorn

Swagger UI

No database is used — data is stored in memory for simplicity and clarity.

🚀 Features

Create doctors with slot capacities

Book tokens with priority logic

Emergency override handling

Token cancellation

Slot status inspection

Automatic Swagger UI documentation

📂 Project Structure
opd-token-allocation/
├── opd.py
├── README.md
├── screenshots/
│   ├── swagger_ui.png
│   ├── create_doctor.png
│   ├── emergency_override.png
│   └── status_output.png

▶️ How to Run the Project
1️⃣ Install Dependencies
pip install fastapi uvicorn

2️⃣ Start the Backend Server
python -m uvicorn opd:app --reload


You should see:

Uvicorn running on http://127.0.0.1:8000

3️⃣ Open Swagger UI

Open your browser and go to:

http://127.0.0.1:8000


You will be automatically redirected to:

http://127.0.0.1:8000/docs

🧪 API Usage (Step-by-Step)
1️⃣ Create a Doctor

POST /doctor/{doctor_id}

Example:

{
  "9-10": 3
}


Creates a doctor with a slot from 9–10 AM having capacity 3.

2️⃣ Book a Token

POST /book

Parameters:

doctor_id

slot_id

source (priority)

Example:

doctor_id: D1
slot_id: 9-10
source: ONLINE

3️⃣ Emergency Override

When the slot is full:

source: EMERGENCY


The system automatically removes the lowest-priority token.

4️⃣ View Slot Status

GET /status/{doctor_id}/{slot_id}

Returns all active tokens ordered by priority.

5️⃣ Cancel a Token

POST /cancel

Example:

doctor_id: D1
slot_id: 9-10
token_id: 2

📸 Screenshots

All API executions and outputs are documented in the screenshots/ folder:

Swagger UI interface

Doctor creation

Emergency override

Slot status output

These screenshots help validate the system behavior visually.

🧩 Edge Cases Handled

Booking when slot is full
Emergency replacing walk-in tokens
Cancelling already removed tokens
Accessing invalid doctor or slot
Preventing server crashes using proper error handling






