from collections import OrderedDict

from json_functions import read_dict, write_data

from clear import clear

class WorkSchedule():
    """Creating/editing work schedule"""
    def __init__(self, schedule):
        """Initialize your schedule"""
        self.schedule = schedule


    def add_day(self, selected_schedule):
        """Add a day to your schedule"""
        entry_num = len(self.schedule) + 1
        day = input('What day is this?\n').strip()
        work_notes = ""
        while not work_notes:
            work_notes = input("from when to when, where?\n").strip().lower()
            if "ink" in work_notes:
                location = "Ink Master"
            elif "snl" in work_notes or 'seth' in work_notes or "fallon" in work_notes:
                location = "NBC"
            elif "other" in work_notes or "runway" in work_notes:
                location = "Other"
            else:
                print("You have to specify where you worked")
                work_notes = ""
        reg_hours = float(input("how many regular hours?\n"))
        ot_hours = float(input("how many OT hours?\n"))
        self.schedule[entry_num] = [day, location, work_notes,
            reg_hours, ot_hours]
        write_data(self.schedule, selected_schedule)


    def edit_full_schedule(self, selected_schedule):
        """Prints out your full schedule"""
        # that seemingly useless key is there so the dictionary's sorted by key
        for key, value in reversed(sorted(self.schedule.items())):
            day = value[0]
            work_notes = value[2]
            message = key + ": " + day + "- Work notes: " + work_notes
            print(message)
        reversed(sorted(self.schedule.items()))
        message = "Enter the number of the entry you want to change.\n"
        message += "\n(q to go back)\n"
        entry_num = input(message)
        if entry_num != "q":
            day = self.schedule[entry_num][0]
            print("So, on " + self.schedule[entry_num][0] + ",")
            work_notes = ""
            
            while not work_notes:
                notes_message = "From when to when did you work and where?\n"
                work_notes = input(notes_message).strip().lower()
                if "ink" in work_notes:
                    location = "Ink Master"
                elif "snl" in work_notes or 'seth' in work_notes or "fallon" in work_notes:
                    location = "NBC"
                elif "other" in work_notes or "runway" in work_notes:
                    location = "Other"
                else:
                    print("You have to specify where you worked")
                    work_notes = ""
            reg_hours = float(input("how many regular hours did you actually work?\n"))
            ot_hours = float(input("how many OT hours did you actually work?\n"))
            self.schedule[entry_num] = [day, location, work_notes,
            reg_hours, ot_hours]
            pause = input('\nhit enter to continue')
            write_data(self.schedule, selected_schedule)


    def remove_entry(self, selected_schedule):
        """Prints out your full schedule"""
        while True:
            counter = len(self.schedule)
            for entry in range(len(self.schedule)):
                day = self.schedule[str(counter)][0]
                notes = self.schedule[str(counter)][2]
                print(str(counter) + '- ' + day + ': ' + notes)
                counter -=1
            message = "\nEnter the number of the day you want to remove."
            message += "\n(q to go back)\n"
            removed_entry = input(message).strip().lower()
            try:
                del self.schedule[removed_entry]
                for key in sorted(self.schedule):
                    if int(key) > int(removed_entry):
                        new_key = int(key) - 1
                        self.schedule[new_key] = self.schedule[key]
                        del self.schedule[key]
                    elif int(key) < int(removed_entry):
                        pass
                pause = input('\nRemoved! Hit enter to continue')
                break
            except:
                if removed_entry == "q":
                    break
                else:
                    print("You can't remove an entry if it doesn't exist!")
        write_data(self.schedule, selected_schedule)

    def export_schedule(self, selected_schedule):
        """Exports schedule in JSON format for records"""
        filename = input("What is the name of the file you will export?") + ".json"
        filename = "past_schedules/" + filename
        write_data(self.schedule, filename)
        empty_schedule = {}
        write_data(empty_schedule, selected_schedule)
        pause = input("successfully exported! Press any key to continue")
## ----------------------------------------------------------------------------

class CalculateSchedule():
    """DO all the calculations"""
    def __init__(self, schedule):
        """Initialize attributes of the parent class."""
        self.schedule = schedule
        self.hours_counter = OrderedDict()

        self.hours_counter["ink reg"] = 0
        self.hours_counter["ink ot"] = 0
        self.hours_counter["nbc reg"] = 0
        self.hours_counter["nbc ot"] = 0
        self.hours_counter["other reg"] = 0
        self.hours_counter["other ot"] = 0
        self.hours_counter["all reg"] = 0
        self.hours_counter["all ot"] = 0

        self.gross_pay = 0
        self.net_pay = 0

    def calculate_all_hours(self):
        """add up all the reg hours, regardless of show"""
        for work_info in self.schedule.values():
            self.hours_counter["all reg"] += work_info[3]
            self.hours_counter["all ot"] += work_info[4]

    def calculate_specific_hours(self):
        """Break down regular and OT hours by show"""
        for work_info in self.schedule.values():
            if work_info[1] == "NBC":
                self.hours_counter["nbc reg"] += work_info[3]
                self.hours_counter["nbc ot"] += work_info[4]
            elif work_info[1] == "Ink Master":
                self.hours_counter["ink reg"] += work_info[3]
                self.hours_counter["ink ot"] += work_info[4]
            elif work_info[1] == "Other":
                self.hours_counter["other reg"] += work_info[3]
                self.hours_counter["other ot"] += work_info[4]

    def calculate_paycheck(self):
        """Calculates pycheck"""
        all_reg = self.hours_counter["all reg"]
        all_ot = self.hours_counter["all ot"]
        self.gross_pay = (all_reg * 16) + (all_ot * 24)
        if self.gross_pay >= 1000:
            tax = self.gross_pay * .26
        if self.gross_pay < 1000:
            tax = self.gross_pay * .24
        self.net_pay = self.gross_pay - tax


    def display_all_hours(self):
        """display the reg and ot totals"""
        # The list in order is ink, nbc, other, all; in reg, ot order
        hours = []
        for key in self.hours_counter:
            if self.hours_counter[key] == 0:
                hours.append("0")
            else:
                hours.append(str(self.hours_counter[key]).rstrip('0').rstrip("."))
        message = "You've worked a total of " + hours[6]
        message += " regular hours and " + hours[7] + " OT hours."
        print(message)


    def display_full_schedule(self):
        """Prints out your full schedule"""
        counter = len(self.schedule)
        for entry in range(len(self.schedule)):
            day = self.schedule[str(counter)][0]
            notes = self.schedule[str(counter)][2]
            print(day + ': ' + notes)
            counter -=1

        '''
        for key, value in reversed(sorted(self.schedule.items())):

            day = value[0]
            work_notes = value[2]
            print(day + ": " + work_notes)
            counter += 1
        reversed(sorted(self.schedule.items()))
        '''
        pause = input('\nHit enter to continue')


    def display_specific_hours(self):
        hours = []
        for key in self.hours_counter:
            if self.hours_counter[key] == 0:
                hours.append("0")
            else:
                hours.append(str(self.hours_counter[key]).rstrip('0').rstrip("."))

        print("\nHere's the total per show:")
        print("\n\tInk Master: " + hours[0] + " regular hours, " + hours[1]+ " OT hours")
        print("\n\tNBC: " + hours[2] + " regular hours, " + hours[3]+ " OT hours")
        print("\n\tOther: " + hours[4] + " reguar hours, " + hours[5]+ " OT hours")
        pause = input('\nHit enter to continue')


    def display_paycheck(self):
        """Display paycheck"""
        self.net_pay = "%.2f" % self.net_pay
        print("Your estimated paycheck is $" + self.net_pay + "\n")


## MAIN PROGRAM -------------------------------------------------------------
def run_program():
    while True:
        selected_schedule = "work_schedule.json"
        schedule = read_dict(selected_schedule)
        ws = WorkSchedule(schedule)
        cs = CalculateSchedule(schedule)

        clear()
        print("~~~~~~~~~~~ WORK SCHEDULE ~~~~~~~~~~~~~\n")
        cs.calculate_all_hours()
        cs.calculate_paycheck()
        cs.display_all_hours()
        cs.display_paycheck()

        message = "Options:\n"
        message += "Full - display full schedule\n"
        message += "Add - add a day to your schedule\nEdit - edit an entry\n"
        message += "Remove - remove an entry\nPer - display hours worked per show\n"
        message += "Export - export schedule to start a new pay period\n"
        print(message)
        prog_func = input("What would you like to do?\n").lower().strip()
        print("\n")

        if prog_func == "full":
            cs.display_full_schedule()
        if prog_func == "add":
            ws.add_day(selected_schedule)
        if prog_func == "edit":
            ws.edit_full_schedule(selected_schedule)
        if prog_func == "remove":
            ws.remove_entry(selected_schedule)
        if prog_func == "per":
            cs.calculate_specific_hours()
            cs.display_specific_hours()
        if prog_func == "export":
            ws.export_schedule(selected_schedule)

if __name__ == "__main__":
    run_program()

