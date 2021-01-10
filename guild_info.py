import discord
import json

class GuildInfo:
    def __init__(self, g_id, c_id):
        self.g_id = g_id
        self.c_id = c_id
        try:
            # create new message_file
            open(f'data/guilds/info_{g_id}.json', 'x')
            with open('data/default_messages.json', 'r') as _from, open(f'data/guilds/info_{g_id}.json', 'w') as _to:
                _to.write(_from.read())
            self.set_default_info()
        except FileExistsError:
            pass

    def set_default_info(self):
        print(f'setting default info, channel id: {self.c_id}')
        self.set_new_message('LANDING_PAGE_ID', self.c_id)
        
    def get_guild_file_name(self):
        return f'data/guilds/info_{self.get_id()}.json'

    def get_id(self):
        return self.g_id

    def get_msg_from_input(self, input_key):
        data = self.get_message_file_data()
        try:
            return data[input_key]
        except KeyError:
            return

    def set_new_message(self, key, val):
        data = self.get_message_file_data()
        data[key] = val
        with open(self.get_guild_file_name(), 'w') as doc:
            json.dump(data, doc)
    
    def get_message_file_data(self):
        with open(self.get_guild_file_name(), 'r') as doc:
            return json.load(doc)
    
    def is_guild(self, input_id):
        return input_id == self.get_id()
