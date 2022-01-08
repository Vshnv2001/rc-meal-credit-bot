import datetime

current_month = datetime.datetime.now().month


sem = 1 if current_month > 6 else 2
total_credits = 108 if sem == 1 else 102

# date for the start of the semester
start_sem2 = datetime.date(2022, 1, 2)
start_sem1 = datetime.date(2022, 8, 1)

current_date = datetime.date.today()
difference = current_date - start_sem1 if sem == 1 else current_date - start_sem2


# Number of sundays between start and current date
completed_weeks = difference.days // 7


expected_usage_bf = 6 * completed_weeks + current_date.weekday() + 1

expected_usage_din = 6 * completed_weeks + current_date.weekday() + 2

# if it's a Sunday, then the expected usage in the current week would've been counted as 7, which is not what we want

if current_date.weekday() == 6:
  expected_usage_bf -= 7
  expected_usage_din -=7


# Display function
def surplus_or_deficit(credits):
  if credits > 0:
    return f"You have a deficit of {credits} credits"
  elif credits < 0:
    credits = - credits
    return f"You have a surplus of {credits} credits"
  else:
    return "You've been using your credits perfectly - no surplus or deficit"


# Returns difference in bf usage. (If positive, deficit)
def bf_calc(current_bf):
  actual_usage = total_credits - int(current_bf)
  return actual_usage - expected_usage_bf 

# Returns difference in dinner usage (If positive, deficit)
def dinner_calc(current_din):
  actual_usage = total_credits - int(current_din)
  return actual_usage - expected_usage_din

# uses the above 2 functions to display a message to the user
def return_message(is_breakfast, credits_left):
  if is_breakfast:
    credit_surplus = bf_calc(credits_left)
    return surplus_or_deficit(credit_surplus)
  else:
    credit_surplus = dinner_calc(credits_left)
    return surplus_or_deficit(credit_surplus)
