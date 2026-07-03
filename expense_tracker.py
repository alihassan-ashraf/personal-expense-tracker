import streamlit as st


class ExpenseTracker:

    def add_expense(self, expenses, expense_id, date, category, description, amount):
        expense = {
            "Expense ID": expense_id,
            "Date": str(date),
            "Category": category,
            "Description": description,
            "Amount": amount
        }

        expenses.append(expense)

    def search_expense(self, expenses, expense_id):
        for expense in expenses:
            if expense["Expense ID"] == expense_id:
                return expense
        return None

    def delete_expense(self, expenses, expense_id):
        expense = self.search_expense(expenses, expense_id)

        if expense is not None:
            expenses.remove(expense)
            return True
        else:
            return False

    def calculate_total_expense(self, expenses):
        total = 0

        for expense in expenses:
            total = total + expense["Amount"]

        return total

    def calculate_category_total(self, expenses, category):
        total = 0

        for expense in expenses:
            if expense["Category"] == category:
                total = total + expense["Amount"]

        return total


tracker = ExpenseTracker()

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰")

st.title("💰 Personal Expense Tracker")
st.write("A simple Python Streamlit app to record and manage daily expenses.")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Add Expense",
        "View All Expenses",
        "Search Expense",
        "Delete Expense",
        "Total Expenses",
        "Category Summary"
    ]
)

if menu == "Add Expense":
    st.subheader("Add New Expense")

    expense_id = st.text_input("Enter Expense ID")
    date = st.date_input("Select Date")
    category = st.selectbox(
        "Select Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education",
            "Other"
        ]
    )
    description = st.text_input("Enter Description")
    amount = st.number_input("Enter Amount", min_value=0.0, value=0.0)

    if st.button("Add Expense"):
        if expense_id == "" or description == "":
            st.warning("Please fill all required fields.")
        elif amount <= 0:
            st.warning("Amount must be greater than zero.")
        else:
            existing_expense = tracker.search_expense(st.session_state.expenses, expense_id)

            if existing_expense is not None:
                st.error("Expense ID already exists.")
            else:
                tracker.add_expense(
                    st.session_state.expenses,
                    expense_id,
                    date,
                    category,
                    description,
                    amount
                )
                st.success("Expense added successfully!")

elif menu == "View All Expenses":
    st.subheader("All Expenses")

    if len(st.session_state.expenses) == 0:
        st.info("No expenses available.")
    else:
        st.table(st.session_state.expenses)

elif menu == "Search Expense":
    st.subheader("Search Expense")

    expense_id = st.text_input("Enter Expense ID to Search")

    if st.button("Search"):
        expense = tracker.search_expense(st.session_state.expenses, expense_id)

        if expense is not None:
            st.success("Expense found!")
            st.write("Expense ID:", expense["Expense ID"])
            st.write("Date:", expense["Date"])
            st.write("Category:", expense["Category"])
            st.write("Description:", expense["Description"])
            st.write("Amount:", expense["Amount"])
        else:
            st.error("Expense not found.")

elif menu == "Delete Expense":
    st.subheader("Delete Expense")

    expense_id = st.text_input("Enter Expense ID to Delete")

    if st.button("Delete"):
        deleted = tracker.delete_expense(st.session_state.expenses, expense_id)

        if deleted:
            st.success("Expense deleted successfully!")
        else:
            st.error("Expense not found.")

elif menu == "Total Expenses":
    st.subheader("Total Expenses")

    total = tracker.calculate_total_expense(st.session_state.expenses)

    st.write("Total Expenses:", total)

elif menu == "Category Summary":
    st.subheader("Category-wise Expense Summary")

    category = st.selectbox(
        "Select Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education",
            "Other"
        ]
    )

    category_total = tracker.calculate_category_total(st.session_state.expenses, category)

    st.write("Selected Category:", category)
    st.write("Total Expense in this Category:", category_total)
