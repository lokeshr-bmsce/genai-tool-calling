from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain_groq import ChatGroq


@tool
def get_salary_info(position: str) -> str:
    """
    Get salary information for a given position.
    """

    salary_data = {
        "software engineer": "$100,000 - $150,000",
        "data scientist": "$90,000 - $140,000",
        "product manager": "$110,000 - $160,000"
    }

    return f"Salary information for {position}: {salary_data.get(position.lower(), 'Position not found')}"

@tool
def remove_currency_format(salary: str) -> float:
    """
    Remove currency format from salary string and convert to float.
    """

    return float(salary.replace("$", "").replace(",", "").split("-")[0].strip())

@tool
def calculate_local_tax(income: str) -> str:
    """
    Calculate local tax based on income.
    """

    income = float(income)

    if income <= 10000:
        tax = 0.1 * income
    elif income <= 50000:
        tax = 0.2 * income
    else:
        tax = 0.3 * income

    return f"Local tax for an income of {income} is: {tax}"

def get_in_hand_salary(salary: str, tax: str) -> str:
    """
    Calculate in-hand salary after deducting tax from gross salary.
    """

    salary = float(salary.replace("$", "").replace(",", "").split("-")[0].strip())
    tax = float(tax.split(":")[1].strip())

    in_hand_salary = salary - tax

    return f"In-hand salary after deducting local tax is: {in_hand_salary}"

@tool
def subtract_tax_from_salary(input: str) -> str:
    """
    Subtract tax from salary.

    Input format:
    salary,tax

    Example:
    50000,5000
    """

    salary, tax = input.split(",")

    result = float(salary) - float(tax)

    return f"Net salary after tax is {result}"
# -----------------------------------
# Groq LLM
# -----------------------------------
llm = ChatGroq(
    groq_api_key="groq_api_key",
    model_name="llama-3.3-70b-versatile"
)


# -----------------------------------
# Agent Setup
# -----------------------------------
tools = [ get_salary_info, calculate_local_tax, remove_currency_format, subtract_tax_from_salary]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)



# -----------------------------------
# Run Agent
# -----------------------------------
response = agent.run(
    "Give me range of salary for software engineer after having deducted local tax from income.."
)

print("\nFinal Response:")
print(response)
