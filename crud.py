from sqlalchemy.orm import Session
from models import User, Expense
from schemas import UserCreate, ExpenseCreate, ExpenseUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_expenses(db: Session, user_id: int, start_date=None, end_date=None):
    query = db.query(Expense).filter(Expense.user_id == user_id)
    if start_date and end_date:
        query = query.filter(Expense.date.between(start_date, end_date))
    return query.all()

def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    db_expense = Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
