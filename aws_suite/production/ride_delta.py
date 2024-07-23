#THE GOLDEN FINAL CODE

class RideDeltaProcessor:
    def __init__(self):
        self.confirmed_classic_starts = 0
        self.confirmed_classic_ends = 0
        self.confirmed_ebike_starts = 0
        self.confirmed_ebike_ends = 0
        self.residuals = {'classic': 0, 'ebikes': 0, 'docks': 0}

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

        if self.check_possible_correction(delta_bikes, delta_ebikes, delta_docks):
            self.handle_balanced_changes(delta_bikes, delta_ebikes)
            self.reset_residuals()
        else:
            self.update_residuals(delta_bikes, delta_ebikes, delta_docks)

    def check_possible_correction(self, delta_bikes, delta_ebikes, delta_docks):
        # Apply residuals and try to find a balance
        adjusted_docks = delta_docks + self.residuals['docks']
        corrected_bikes = delta_bikes + self.residuals['classic'] + self.residuals['ebikes']

        if corrected_bikes == -adjusted_docks:
            # If we can balance the docks and bikes, apply the residuals
            if self.residuals['ebikes'] > 0:
                self.confirmed_ebike_ends += self.residuals['ebikes']
            elif self.residuals['ebikes'] < 0:
                self.confirmed_ebike_starts -= self.residuals['ebikes']
            if self.residuals['classic'] > 0:
                self.confirmed_classic_ends += self.residuals['classic']
            elif self.residuals['classic'] < 0:
                self.confirmed_classic_starts -= self.residuals['classic']
            return True
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

    def update_residuals(self, delta_bikes, delta_ebikes, delta_docks):
        self.residuals['classic'] = delta_bikes - delta_ebikes
        self.residuals['ebikes'] = delta_ebikes
        self.residuals['docks'] = delta_docks

    def reset_residuals(self):
        self.residuals = {'classic': 0, 'ebikes': 0, 'docks': 0}

    def get_confirmed_rides(self):
        return {
            'classic_starts': self.confirmed_classic_starts,
            'classic_ends': self.confirmed_classic_ends,
            'ebike_starts': self.confirmed_ebike_starts,
            'ebike_ends': self.confirmed_ebike_ends
        }
