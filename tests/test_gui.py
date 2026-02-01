import re
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.usefixtures("api_server", "gui_server")
def test_full_user_flow(page: Page):
    # 1. Access the GUI with specific API port
    page.goto("http://127.0.0.1:3001?api_port=8081")
    expect(page).to_have_title("Calorie Mgmt - Smart Dashboard")

    # 2. Profile Setup
    page.click("text=Profile")
    page.select_option("#gender", "male")
    page.fill("#age", "30")
    page.fill("#height", "175")
    page.fill("#weight", "70")
    # Note: activity-level select is not in the HTML I saw, but I might have missed it or it's injected.
    # Actually, looking at index.html, it's NOT there. I will remove it or fix it.
    # Also fix button text which is "Update Profile" not "Save Profile"
    page.click("button:has-text('Update Profile')")
    
    # 3. Goal Setting
    # Goals section in index.html has target-weight and target-date
    page.fill("#target-weight", "65")
    from datetime import datetime, timedelta
    target_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    page.fill("#target-date", target_date)
    # Button is "Set Goal"
    page.click("button:has-text('Set Goal')")
    
    # 4. Meal Logging & Dashboard Update
    page.click("button[data-tab='dashboard']") # Explicitly click the tab button
    
    # Fill meal form
    page.fill("#food-name", "Test Steak")
    page.fill("#calories", "500")
    page.click("#meal-form button[type='submit']")
    
    # Dashboard checks
    # Use IDs from index.html: total-consumed, daily-goal
    # Wait for the text to change from "0"
    expect(page.locator("#total-consumed")).to_have_text("500", timeout=10000)
    
    # 5. History check
    page.click("button[data-tab='history']")
    expect(page.locator("#meal-history")).to_contain_text("Test Steak")
    expect(page.locator("#meal-history")).to_contain_text("500")
