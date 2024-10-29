from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/signup/")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db=db, user=user)

@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.username)
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/expenses/")
def read_expenses(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    return crud.get_expenses(db, user_id=1, start_date=start_date, end_date=end_date)

@app.post("/expenses/")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense, user_id=1)
