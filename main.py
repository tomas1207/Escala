import random
import math
import csv

def generate_schedule(team_members, num_weeks=1):
    work_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    office_blocks = [
        ["Monday", "Tuesday", "Wednesday"],
        ["Wednesday", "Thursday", "Friday"]
    ]
    
    team_size = len(team_members)
    min_office_count = math.ceil(0.55 * team_size)  # Calculate 55% of the team size, rounded up

    all_weeks_schedule = []  # Store all schedules for CSV output

    assigned_blocks = {member: [] for member in team_members}  # Track assigned blocks for each team member

    for week in range(num_weeks):
        print(f"--- Week {week + 1} Schedule ---")
        
        # Prepare an empty weekly schedule
        week_schedule = {day: [] for day in work_days}
        
        # Shuffle team members to vary assignments each week
        random.shuffle(team_members)
        
        # Assign each team member a 3-day office block and ensure "Friday office, Monday home" rule
        for member in team_members:
            # Randomly select a 3-day office block
            while True:
                office_days = random.choice(office_blocks)
                
                # Ensure no repetition of office blocks for the same member
                if office_days in assigned_blocks[member]:
                    continue
                
                # Apply "Friday-to-Monday home" rule
                home_days = [day for day in work_days if day not in office_days]
                
                # Ensure no repetition and valid block assignment
                if office_days not in assigned_blocks[member]:
                    # Check if the member is assigned to the office on Friday
                    if "Friday" in office_days:
                        # Ensure the member is assigned to home on Monday
                        if "Monday" not in home_days:
                            continue  # Retry if Monday is not in home_days
                    assigned_blocks[member].append(office_days)
                    break  # Exit loop with valid days

            # Assign the member's schedule to the week
            for day in office_days:
                week_schedule[day].append((member, "Office"))
            for day in home_days:
                week_schedule[day].append((member, "Home"))

        # Enforce the 55% office attendance rule and ensure max 3 office days per member
        for day in work_days:
            office_members = [member for member, status in week_schedule[day] if status == "Office"]
            home_members = [member for member, status in week_schedule[day] if status == "Home"]

            # Move members from home to office if below the 55% requirement
            while len(office_members) < min_office_count and home_members:
                member_to_move = home_members.pop()
                # Ensure the member does not exceed 3 office days
                office_days_count = sum(1 for d in work_days if (member_to_move, "Office") in week_schedule[d])
                if office_days_count < 3:
                    week_schedule[day].remove((member_to_move, "Home"))
                    week_schedule[day].append((member_to_move, "Office"))
                    office_members.append(member_to_move)

        # Ensure no member is assigned to the office more than 3 times in a week
        for member in team_members:
            office_days_count = sum(1 for day in work_days if (member, "Office") in week_schedule[day])
            if office_days_count > 3:
                for day in work_days:
                    if (member, "Office") in week_schedule[day]:
                        week_schedule[day].remove((member, "Office"))
                        week_schedule[day].append((member, "Home"))
                        office_days_count -= 1
                        if office_days_count <= 3:
                            break

        # Store the schedule for this week in the all_weeks_schedule list
        for day in work_days:
            for member, status in week_schedule[day]:
                all_weeks_schedule.append({
                    "Week": week + 1,
                    "Day": day,
                    "Team Member": member,
                    "Location": status
                })

        # Display the schedule for this week in the console
        for day in work_days:
            office_list = [member for member, status in week_schedule[day] if status == "Office"]
            home_list = [member for member, status in week_schedule[day] if status == "Home"]
            print(f"{day}: Office: {office_list} | Home: {home_list}")
        print("\n")
    
    return all_weeks_schedule


def save_schedule_to_csv(schedule, filename="team_schedule.csv"):
    # Define CSV headers
    headers = ["Week", "Day", "Team Member", "Location"]

    # Write data to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(schedule)

    print(f"Schedule saved to {filename}")


# Example usage:
team = [
    "Margarida Vale", "Alexandra Romão", "Isabel Silva", "Joana Lopes", 
    "Neuza Nobre", "Sandra Laurentino", "Paulo Gonçalves", "Paula Sousa", "Hélder Sampaínho", 
    "Carla Mendes", "Catarina Marques", "Sara Baptista", "Luís Duarte", "Fábio Silva Porfírio", 
    "José Sampaio", "Cláudia Monteiro", "Susana Gregório", "Ana Cristina Santos", "Manuel Costa", 
    "Rita Silva", "Rui Melo", "Tânia Oliveira"
]
schedule = generate_schedule(team, num_weeks=4)
save_schedule_to_csv(schedule, filename="team_schedule.csv")
