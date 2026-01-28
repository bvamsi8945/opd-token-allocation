from fastapi import FastAPI, HTTPException
from typing import List, Dict
from enum import IntEnum
from datetime import datetime
from fastapi.responses import RedirectResponse


app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(url="/docs")


class Priority(IntEnum):
    WALK_IN = 1
    ONLINE = 2
    FOLLOW_UP = 3
    PAID = 4
    EMERGENCY = 5


class Token:
    def __init__(self, token_id: int, source: Priority):
        self.token_id = token_id
        self.source = source
        self.created_at = datetime.now()
        self.active = True


class Slot:
    def __init__(self, slot_id: str, capacity: int):
        self.slot_id = slot_id
        self.capacity = capacity
        self.tokens: List[Token] = []

    def sort_tokens(self):
        self.tokens.sort(key=lambda t: (-t.source, t.created_at))

    def add_token(self, token: Token):
        if len(self.tokens) < self.capacity:
            self.tokens.append(token)
            self.sort_tokens()
            return True

        lowest = min(self.tokens, key=lambda t: (t.source, t.created_at))

        if token.source > lowest.source:
            self.tokens.remove(lowest)
            lowest.active = False
            self.tokens.append(token)
            self.sort_tokens()
            return True

        return False


class Doctor:
    def __init__(self, doctor_id: str):
        self.doctor_id = doctor_id
        self.slots: Dict[str, Slot] = {}


doctors: Dict[str, Doctor] = {}
token_counter = 1


@app.post("/doctor/{doctor_id}")
def create_doctor(doctor_id: str, slots: Dict[str, int]):
    doctor = Doctor(doctor_id)
    for slot_id, cap in slots.items():
        doctor.slots[slot_id] = Slot(slot_id, cap)
    doctors[doctor_id] = doctor
    return {"message": f"Doctor {doctor_id} created"}


@app.post("/book")
def book_token(doctor_id: str, slot_id: str, source: Priority):
    global token_counter

    if doctor_id not in doctors:
        raise HTTPException(404, "Doctor not found")

    slot = doctors[doctor_id].slots.get(slot_id)
    if not slot:
        raise HTTPException(404, "Slot not found")

    token = Token(token_counter, source)
    token_counter += 1

    if not slot.add_token(token):
        raise HTTPException(400, "Slot full, lower priority")

    return {"token_id": token.token_id, "status": "confirmed"}


@app.post("/cancel")
def cancel_token(doctor_id: str, slot_id: str, token_id: int):
    slot = doctors[doctor_id].slots.get(slot_id)

    if not slot:
        raise HTTPException(404, "Slot not found")

    for token in slot.tokens:
        if token.token_id == token_id:
            token.active = False
            slot.tokens.remove(token)
            return {"status": "cancelled"}

    raise HTTPException(404, "Token not found")


@app.get("/status/{doctor_id}/{slot_id}")
def slot_status(doctor_id: str, slot_id: str):
    slot = doctors[doctor_id].slots.get(slot_id)

    if not slot:
        raise HTTPException(404, "Slot not found")

    return [
        {
            "token_id": t.token_id,
            "priority": t.source.name,
            "active": t.active
        }
        for t in slot.tokens
    ]
