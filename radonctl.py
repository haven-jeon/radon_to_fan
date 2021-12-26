import appdaemon.plugins.hass.hassapi as hass

#
# App to turn on entity_to_control when radon sensor values in specific ranges
# Args:
#
# radon_sensor: radon sensor eg. sensor.airthings_radon_1day_avg
# min: minimum value to 'off'
# max: maximum value to 'on'
# entity_to_control:
# dryrun: on or off
# on_speed: off, low, medium, high

class RemoveRadon(hass.Hass):
    speed_map = {'off': 0, 'low': 33, 'medium': 66, 'high': 100}
    
    def initialize(self):
        self.fan = self.args["entity_to_control"]
        self.listen_state(self.radon_change, self.args.get("radon_sensor", "sensor.airthings_radon_1day_avg"))

    def radon_change(self, entity, attribute, old, new, kwargs):
        if float(new) > float(self.args['max']):
            self.log("Radon value is just over {} turn on {}".format(self.args['max'], self.fan))
            self.log(f"dryrun value {self.args['dryrun']}")
            if self.args['dryrun'] == False:
                self.call_service("fan/turn_on", entity_id = self.fan)
                self.run_in(self.set_speed, 5)
        elif float(new) < float(self.args['min']):
            self.log("Radon value is just below {} turn off {}".format(self.args['min'], self.fan))
            if self.args['dryrun'] == False:
                # self.turn_off(self.args["entity_to_control"])
                self.call_service("fan/turn_off", entity_id = self.fan)

    def set_speed(self, kwargs):
        self.log(f'change speed to {self.args["on_speed"]}')
        self.call_service("fan/set_speed", entity_id=self.fan, speed=self.args['on_speed'])
