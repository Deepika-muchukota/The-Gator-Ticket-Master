from red_black_tree import RedBlackTree
from max_heap import MaxHeap
import sys

class GatorTicketMaster:
    def __init__(self):
        # Initialize ticket system with RB tree for reservations and MaxHeap for waitlist
        self.reserved_seats = RedBlackTree()
        self.available_seats = []
        self.waitlist = MaxHeap()
        self.timestamp = 0

    def initialize(self, seat_count):
        # Initialize system with given number of seats
        if seat_count <= 0:
            return "Invalid input. Please provide a valid number of seats."
        
        self.available_seats = list(range(1, seat_count + 1))
        return f"{seat_count} Seats are made available for reservation"

    def available(self):
        # Return current count of available seats and waitlist size
        return f"Total Seats Available : {len(self.available_seats)}, Waitlist : {len(self.waitlist.heap)}"

    def reserve(self, user_id, user_priority):
        # Reserve seat for user or add to waitlist if no seats available
        if self.available_seats:
            seat_id = min(self.available_seats)
            self.available_seats.remove(seat_id)
            self.reserved_seats.insert(user_id, seat_id)
            return f"User {user_id} reserved seat {seat_id}"
        else:
            self.timestamp += 1
            self.waitlist.insert((user_priority, user_id, self.timestamp))
            return f"User {user_id} is added to the waiting list"

    def cancel(self, seat_id, user_id):
        # Cancel reservation and assign seat to highest priority waitlisted user
        node = self.reserved_seats.find(user_id)
        if not node or node.seat_id != seat_id:
            return f"User {user_id} has no reservation for seat {seat_id} to cancel"

        self.reserved_seats.delete(user_id)
        
        if self.waitlist.heap:    # If waitlist exists, assign seat to highest priority user
            priority, next_user_id, timestamp = self.waitlist.pop()
            self.reserved_seats.insert(next_user_id, seat_id)
            return f"User {user_id} canceled their reservation\nUser {next_user_id} reserved seat {seat_id}"
        else:
            self.available_seats.append(seat_id)
            return f"User {user_id} canceled their reservation"

    def exit_waitlist(self, user_id):  # Remove user from waitlist if present
        if self.waitlist.contains(user_id):
            self.waitlist.remove(user_id)
            return f"User {user_id} is removed from the waiting list"
        return f"User {user_id} is not in waitlist"

    def update_priority(self, user_id, new_priority):
        # Update priority of waitlisted user
        if self.waitlist.update_priority(user_id, new_priority):
            return f"User {user_id} priority has been updated to {new_priority}"
        return f"User {user_id} priority is not updated"

    def add_seats(self, count):
        # Add new seats and assign to waitlisted users based on priority
        if count <= 0:
            return "Invalid input. Please provide a valid number of seats."

        start_seat = max(
            max((node[0] for node in self.reserved_seats.in_order_traversal()), default=0),
            max(self.available_seats, default=0)
        ) + 1
        
        new_seats = list(range(start_seat, start_seat + count))
        result = [f"Additional {count} Seats are made available for reservation"]

        # Sort waitlist by priority and timestamp
        waitlist_users = sorted(
            [(p, uid, t) for p, uid, t in self.waitlist.heap],
            key=lambda x: (-x[0], x[2])  # Sort by priority (desc) and timestamp (asc)
        )
        self.waitlist.heap = []

        # Assign seats to waitlist users
        for priority, user_id, timestamp in waitlist_users:
            if new_seats:
                seat_id = min(new_seats)
                new_seats.remove(seat_id)
                self.reserved_seats.insert(user_id, seat_id)
                result.append(f"User {user_id} reserved seat {seat_id}")
            else:
                self.waitlist.insert((priority, user_id, timestamp))

        self.available_seats.extend(new_seats)
        return "\n".join(result)

    def release_seats(self, user_id1, user_id2):
        # Release all seats held by users in specified ID range
        if user_id1 > user_id2:
            return "Invalid input. Please provide a valid range of users."

        nodes = self.reserved_seats.in_order_traversal()
        released_seats = []
        result = []
        
        # Find and release seats in range
        for seat_id, user_id in nodes:
            if user_id1 <= user_id <= user_id2:
                released_seats.append(seat_id)
                self.reserved_seats.delete(user_id)
         # Remove users from waitlist in range
        self.waitlist.heap = [
            item for item in self.waitlist.heap 
            if not (user_id1 <= item[1] <= user_id2)
        ]

        if released_seats:
            result.append(f"Reservations of the Users in the range [{user_id1}, {user_id2}] are released")
            # Reassign released seats to waitlist users
            released_seats.sort()
            while self.waitlist.heap and released_seats:
                priority, next_user_id, timestamp = self.waitlist.pop()
                seat_id = released_seats.pop(0)
                self.reserved_seats.insert(next_user_id, seat_id)
                result.append(f"User {next_user_id} reserved seat {seat_id}")
            
            self.available_seats.extend(released_seats)
        else:
            result.append(f"Reservations/waitlist of the users in the range [{user_id1}, {user_id2}] have been released")
        
        return "\n".join(result)

    def print_reservations(self):
        # Print all current reservations sorted by seat number
        nodes = self.reserved_seats.in_order_traversal()
        result = []
        for seat_id, user_id in sorted(nodes, key=lambda x: x[0]):
            result.append(f"Seat {seat_id}, User {user_id}")
        return "\n".join(result)

    def quit(self):
        # Terminate program
        return "Program Terminated!!"

def main():
    # Main function to process commands from input file and write results to output file
    if len(sys.argv) != 2:
        print("Usage: python gatorTicketMaster.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace('.txt', '_output.txt')
    system = GatorTicketMaster()
    
    try:
        # Process input file and write results to output file
        with open(input_file, 'r') as file, open(output_file, 'w') as out_file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse and execute commands
                    command = line.split('(')[0]
                    if command == "Initialize":
                        count = int(line.split('(')[1].split(')')[0])
                        result = system.initialize(count)
                    elif command == "Available":
                        result = system.available()
                    elif command == "Reserve":
                        params = line.split('(')[1].split(')')[0].split(',')
                        user_id = int(params[0])
                        priority = int(params[1])
                        result = system.reserve(user_id, priority)
                    elif command == "Cancel":
                        params = line.split('(')[1].split(')')[0].split(',')
                        seat_id = int(params[0])
                        user_id = int(params[1])
                        result = system.cancel(seat_id, user_id)
                    elif command == "AddSeats":
                        count = int(line.split('(')[1].split(')')[0])
                        result = system.add_seats(count)
                    elif command == "ReleaseSeats":
                        params = line.split('(')[1].split(')')[0].split(',')
                        user_id1 = int(params[0])
                        user_id2 = int(params[1])
                        result = system.release_seats(user_id1, user_id2)
                    elif command == "ExitWaitlist":
                        user_id = int(line.split('(')[1].split(')')[0])
                        result = system.exit_waitlist(user_id)
                    elif command == "UpdatePriority":
                        params = line.split('(')[1].split(')')[0].split(',')
                        user_id = int(params[0])
                        new_priority = int(params[1])
                        result = system.update_priority(user_id, new_priority)
                    elif command == "PrintReservations":
                        result = system.print_reservations()
                    elif command == "Quit":
                        result = system.quit()
                        out_file.write(result + '\n')
                        break
                    elif command == "Release":
                        continue  # Ignore Release command after Quit
                    
                    out_file.write(result + '\n')
                except Exception as e:
                    error_msg = f"Error processing line: {line}\nError details: {str(e)}\n"
                    out_file.write(error_msg)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

if __name__ == "__main__":
    main()