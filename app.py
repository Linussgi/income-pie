import streamlit as st
import plotly.graph_objects as go
from utils.calculators import calculate_income_tax, calculate_nic, calculate_student_loan

st.title("Income Info")

# Sidebar Inputs
st.sidebar.subheader("Inputs")

initial_income = st.sidebar.number_input("Enter Yearly Gross Pay:", min_value=0.0, value=0.0, format="%.2f")
pension_rate = st.sidebar.number_input("Enter your pension rate (%):", min_value=0.0, max_value=100.0, value=0.0, format="%.2f")

has_student_loan = st.sidebar.checkbox("Repay Student Loan")
if has_student_loan:
    st.sidebar.markdown("##### Student Loan Info")
    student_loan_rate = st.sidebar.number_input("Student Loan Rate (%)", min_value=0.0, max_value=100.0, value=9.0, format="%.2f")
    student_loan_threshold = st.sidebar.number_input("Repayment Threshold (£)", min_value=0.0, value=27295.0, format="%.2f")
else:
    student_loan_rate = 0.0
    student_loan_threshold = 0.0

# Calculations
pension_deduction = initial_income * (pension_rate / 100)
gross_income = initial_income - pension_deduction

if initial_income > 0:
    basic_tax, higher_tax, additional_tax = calculate_income_tax(gross_income)
    income_tax = basic_tax + higher_tax + additional_tax

    pt_nic, uel_nic = calculate_nic(gross_income)
    nic = pt_nic + uel_nic

    sl_payment = calculate_student_loan(gross_income, student_loan_rate / 100, student_loan_threshold) if has_student_loan else 0.0

    net_income = gross_income - income_tax - nic - sl_payment
else:
    income_tax = 0.0
    nic = 0.0
    sl_payment = 0.0
    net_income = 0.0

# Sidebar Outputs
st.sidebar.subheader("Results")
st.sidebar.write(f"Pension Deduction: £{pension_deduction:,.2f}")
st.sidebar.write(f"Income Tax: £{income_tax:,.2f}")
st.sidebar.write(f"National Insurance: £{nic:,.2f}")
if has_student_loan:
    st.sidebar.write(f"Student Loan: £{sl_payment:,.2f}")
st.sidebar.write(f"Take Home Pay: £{net_income:,.2f}")

# Pie Chart
labels = ["Pension", "Income Tax", "NIC", "Student Loan", "Take Home"]
values = [pension_deduction, income_tax, nic, sl_payment, net_income]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
fig.update_traces(
    textinfo="label+percent",
    marker=dict(colors=["#6fb6ec", "#f76565", "#f9f1a5", "#f3c623", "#65f779"]),
    domain=dict(x=[0.0, 1.0], y=[0.0, 1.0])
)
fig.update_layout(margin=dict(t=80, b=80, l=80, r=80), height=650)

st.plotly_chart(fig, use_container_width=True)