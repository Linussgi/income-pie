from boundaries import IT_B1, IT_B2, IT_B3, IT_B4, NIC_B1, NIC_B2


def calculate_income_tax(income: float) -> float:
    basic_rate = 0.2
    higher_rate = 0.4
    additional_rate = 0.45

    if income <= IT_B3:
        allowance = IT_B1
    elif income < IT_B4:
        allowance = max(0, IT_B1 - (income - IT_B3) / 2)
    else:
        allowance = 0

    taxable_income = income - allowance

    basic_band = max(0, min(taxable_income, IT_B2 - IT_B1))
    higher_band = max(0, min(taxable_income - basic_band, IT_B4 - IT_B2))
    additional_band = max(0, taxable_income - basic_band - higher_band)

    basic_tax = (basic_band * basic_rate)
    higher_tax = (higher_band * higher_rate)
    additional_tax = (additional_band * additional_rate)

    return basic_tax, higher_tax, additional_tax


def calculate_nic(income: float) -> float:
    pt_rate = 0.08
    uel_rate = 0.02

    pt_band = max(0, min(income, NIC_B2) - NIC_B1)
    uel_band = max(0, income - NIC_B2)

    pt_nic = pt_band * pt_rate
    uel_nic = uel_band * uel_rate

    return pt_nic, uel_nic


def calculate_student_loan(income: float, sl_rate, sl_boundary) -> float:
    return max(0, income - sl_boundary) * sl_rate

