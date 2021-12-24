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

    def initialize(self):
        self.listen_state(self.radon_change, self.args.get("radon_sensor", "sensor.airthings_radon_1day_avg"))

    def radon_change(self, entity, attribute, old, new, kwargs):
        if float(new) > float(self.args['max']):
            self.log("Radon value is just over {} turn on {}".format(self.args['max'], self.args["entity_to_control"]))
            if self.args['dryrun'] != 'on':
                self.turn_on(self.args["entity_to_control"], speed=self.args['on_speed'])
        elif float(new) < float(self.args['min']):
            self.log("Radon value is just below {} turn off {}".format(self.args['min'], self.args["entity_to_control"]))
            if self.args['dryrun'] != 'on':
                self.turn_off(self.args["entity_to_control"], speed='off')
        
