#NEWEST AS OF 1800 AND 724 0100 HRS 
class RideDeltaProcessor:
    def __init__(self):
        self.confirmed_classic_starts = 0
        self.confirmed_classic_ends = 0
        self.confirmed_ebike_starts = 0
        self.confirmed_ebike_ends = 0
        self.residuals = {'classic': 0, 'ebikes': 0, 'docks': 0}
        print("Initialized processor with zeroed counts and residuals.")

    def process_changes(self, changes):
        delta_bikes = 0
        delta_ebikes = 0
        delta_docks = 0

        for change in changes:
            if change['field'] == 'num_bikes_available':
                delta_bikes += change['new_value'] - change['old_value']
            if change['field'] == 'num_ebikes_available':
                delta_ebikes += change['new_value'] - change['old_value']
            if change['field'] == 'num_docks_available':
                delta_docks += change['new_value'] - change['old_value']

        print(f"Processed deltas: Bikes={delta_bikes}, eBikes={delta_ebikes}, Docks={delta_docks}")
        print(f"Current residuals: {self.residuals}")
        
        
        if all(value == 0 for value in self.residuals.values()) and self.is_valid_input(delta_bikes,delta_ebikes,delta_docks): # and -delta_docks == delta_bikes
            print("No residuals currently, trx in balance, recording")
            self.handle_balanced_changes(delta_bikes,delta_ebikes)
            
        elif self.check_possible_correction(delta_bikes, delta_ebikes, delta_docks):
            print("Correction possible, applying changes.")
            self.handle_balanced_changes(delta_bikes, delta_ebikes)
            self.reset_residuals()
            
        else:
            print("No correction possible, updating residuals.")
            self.update_residuals(delta_bikes, delta_ebikes, delta_docks)

    def check_possible_correction(self, delta_bikes, delta_ebikes, delta_docks):
        if all(value == 0 for value in self.residuals.values()):
            return False  # Early exit if all residuals are zero

        adjusted_docks = delta_docks + self.residuals['docks']
        corrected_bikes = delta_bikes + self.residuals['classic'] + self.residuals['ebikes']

        if corrected_bikes == -adjusted_docks and self.is_valid_input(corrected_bikes,delta_ebikes,adjusted_docks):
            print("Balance achieved with corrections applied.")
            if self.residuals['ebikes'] > 0:
                self.confirmed_ebike_ends += self.residuals['ebikes']
            elif self.residuals['ebikes'] < 0:
                self.confirmed_ebike_starts -= self.residuals['ebikes']
            if self.residuals['classic'] > 0:
                self.confirmed_classic_ends += self.residuals['classic']
            elif self.residuals['classic'] < 0:
                self.confirmed_classic_starts -= self.residuals['classic']
            return True
        else:
            print('could not find balance')
        return False
    
    def is_valid_input(self,delta_bikes,delta_ebikes,delta_docks):
        if delta_bikes == -delta_docks:
            if delta_bikes == 0 and delta_docks == 0 and delta_ebikes != 0:
                return False
            else:
                return True
        else:
            return False
        

    def handle_balanced_changes(self, delta_bikes, delta_ebikes):
        delta_classic_bikes = delta_bikes - delta_ebikes
        if delta_classic_bikes > 0:
            self.confirmed_classic_ends += delta_classic_bikes
        elif delta_classic_bikes < 0:
            self.confirmed_classic_starts -= delta_classic_bikes
        if delta_ebikes > 0:
            self.confirmed_ebike_ends += delta_ebikes
        elif delta_ebikes < 0:
            self.confirmed_ebike_starts -= delta_ebikes
        print(f"Confirmed rides: {self.get_confirmed_rides()}")

    def update_residuals(self, delta_bikes, delta_ebikes, delta_docks):
        if delta_bikes != 0 and delta_bikes != -delta_docks:
            self.residuals['classic'] = delta_bikes - delta_ebikes
        else:
            self.residuals['classic'] = 0
            
        self.residuals['ebikes'] = delta_ebikes
        self.residuals['docks'] = delta_docks
        print(f"Updated residuals: {self.residuals}")

    def reset_residuals(self):
        print("Resetting residuals.")
        self.residuals = {'classic': 0, 'ebikes': 0, 'docks': 0}

    def get_confirmed_rides(self):
        return {
            'classic_starts': self.confirmed_classic_starts,
            'classic_ends': self.confirmed_classic_ends,
            'ebike_starts': self.confirmed_ebike_starts,
            'ebike_ends': self.confirmed_ebike_ends
        }
