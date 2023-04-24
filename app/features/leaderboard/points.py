# Define point values for each action
points_per_range_session = 10
points_per_18_holes = 50
points_per_9_holes = 25
points_per_practice_at_home = 5

# Example dictionary of players and their points
player_points = {
    'Alice': 100,
    'Bob': 50,
    'Charlie': 75
}

# Function to add points for an action
def add_points(player_name, action):
    # Lookup the point value for the action
    if action == 'range_session':
        points = points_per_range_session
    elif action == '18_holes':
        points = points_per_18_holes
    elif action == '9_holes':
        points = points_per_9_holes
    elif action == 'practice_at_home':
        points = points_per_practice_at_home
    else:
        raise ValueError(f'Invalid action: {action}')
    
    # Add points to the player's total
    player_points[player_name] += points

# Example usage
add_points('Alice', 'range_session')
add_points('Bob', '9_holes')
add_points('Charlie', 'practice_at_home')
print(player_points)