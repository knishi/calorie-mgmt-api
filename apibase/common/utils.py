import datetime

def calculate_daily_goal(profile, target_weight, target_date):
    """Calculate daily calorie goal based on profile and targets.
    
    Formula:
    1. BMR (Harris-Benedict revised):
       - Male: 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
       - Female: 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    2. TDEE = BMR * activity_level
    3. Daily Deficit = (Current Weight - Target Weight) * 7200 / DaysRemaining
    4. Daily Goal = TDEE - Daily Deficit
    """
    if not profile or not profile.weight or not profile.height or not profile.age:
        return 2000 # Default if profile is incomplete
    
    # 1. BMR
    if profile.gender == 'female':
        bmr = 447.593 + (9.247 * profile.weight) + (3.098 * profile.height) - (4.330 * profile.age)
    else:
        # Default to male math
        bmr = 88.362 + (13.397 * profile.weight) + (4.799 * profile.height) - (5.677 * profile.age)
    
    # 2. TDEE
    tdee = bmr * (profile.activity_level or 1.2)
    
    # 3. Days Remaining
    today = datetime.datetime.utcnow().date()
    if isinstance(target_date, datetime.datetime):
        target_date = target_date.date()
    
    days_remaining = (target_date - today).days
    if days_remaining <= 0:
        return int(tdee) # Maintenance
    
    # 4. Total Deficit
    total_deficit = (profile.weight - target_weight) * 7200
    daily_deficit = total_deficit / days_remaining
    
    goal = tdee - daily_deficit
    
    # Safety: Don't go below BMR or a hard minimum (e.g. 1200)
    return max(int(goal), 1200)
