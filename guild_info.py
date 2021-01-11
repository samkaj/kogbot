import discord
import json

class GuildInfo:
    def __init__(self, guild_obj):
        self.guild_obj = guild_obj
        self.guild_id = guild_obj.id
        self.standard_channel_id = guild_obj.channels[0].id
        self.members = guild_obj.members
        self.owner = guild_obj.owner
        self.guild_name = str(guild_obj)
        try:
            # create new message_file, throws exception if file already exists
            open(f'data/guilds/info_{self.guild_id}.json', 'x')

            self.set_default_info()
        except FileExistsError:
            pass

    def set_default_info(self):
        tmp_data = {
            'guild_name': self.guild_name,
            'guild_id': self.guild_id,
            'standard_channel_id': self.standard_channel_id,
            'members': [(member.id, member.name) for member in self.members],
            'owner': (self.owner.id, self.owner.name),
            'welcome_message': 'welcome <3'
        }
        with open(f'data/guilds/info_{self.guild_id}.json', 'w') as doc:
            json.dump(tmp_data, doc)

        print(f'setting default info for guild: {self.guild_obj.name}')

        
    def get_guild_file_name(self):
        return f'data/guilds/info_{self.get_guild_id()}.json'

    def get_guild_id(self):
        return self.guild_id

    def get_msg_from_input(self, input_key):
        try:
            return self.get_data()[input_key]
        except KeyError:
            return

    def change_data(self, key, val):
        data = self.get_data()
        data[key] = val
        with open(self.get_guild_file_name(), 'w') as doc:
            json.dump(data, doc)
    
    # Maybe rename?
    def get_data(self):
        with open(self.get_guild_file_name(), 'r') as doc:
            return json.load(doc)
    
    # TODO: remove?
    def is_guild(self, input_id):
        return input_id == self.get_guild_id()
