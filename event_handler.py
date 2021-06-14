class EventHandler:
    def __init__(self):
        self.events = []

    def add_event(self, is_repeating: bool, name: str, time: int, arg1=None, arg2=None, arg3=None):
        '''Adds an event to the queue'''
        is_repeating = bool(is_repeating) # whether the event should be repeated every tick or just delayed
        name = str(name) # the name of the event
        time = int(time) # the delay or the amount of repeats

        self.events.append({'type': is_repeating,
                            'name': name,
                            'time_left': time,
                            'arg1': arg1, # additional arguments for the executor (optional)
                            'arg2': arg2,
                            'arg3': arg3})

    def get_events(self, name) -> list:
        '''Gets all the events with the specified name'''
        results = []
        for i in self.events:
            if i['name'] == name:
                results.append(i)
        return results

    def tick(self) -> list:
        '''Ticks every event in the queue and returns all that need to be processed'''
        to_process = []
        counter = 0
        for i in self.events:
            i['time_left'] -= 1
            if i['type'] or not i['time_left']:
                to_process.append(i)
            if i['time_left'] == 0:
                self.events.pop(counter)
            counter += 1
        return to_process