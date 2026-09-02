from app.preferences import UserPreferences


preferences = UserPreferences()

preferences.set_priority("Technology & AI", "High")
preferences.set_priority("Sports", "Low")

print("Technology priority:",
      preferences.get_priority("Technology & AI"))

print("Sports priority:",
      preferences.get_priority("Sports"))

print("Education priority:",
      preferences.get_priority("Education"))