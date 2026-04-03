from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from models.record import FinancialRecord

def get_summary(db: Session):
    records = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    ).all()

    total_income = sum(r.amount for r in records if r.type == "income")
    total_expense = sum(r.amount for r in records if r.type == "expense")
    net_balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "total_records": len(records)
    }

def get_category_wise(db: Session):
    records = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    ).all()

    category_totals = {}
    for record in records:
        if record.category not in category_totals:
            category_totals[record.category] = {
                "income": 0,
                "expense": 0
            }
        category_totals[record.category][record.type] += record.amount

    return category_totals

def get_monthly_trends(db: Session):
    records = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    ).all()

    monthly = {}
    for record in records:
        key = record.date.strftime("%Y-%m")
        if key not in monthly:
            monthly[key] = {"income": 0, "expense": 0}
        monthly[key][record.type] += record.amount

    # sort by month
    sorted_monthly = dict(sorted(monthly.items()))
    return sorted_monthly

def get_recent_activity(db: Session, limit: int = 10):
    records = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    ).order_by(FinancialRecord.created_at.desc()).limit(limit).all()
    return records