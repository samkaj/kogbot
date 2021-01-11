import discord
import json

# Handles information about discord.Guild and "saves" its state in json form.

class GuildInfo:
    def __init__(self, guild_obj):
        self.guild_obj = guild_obj
        self.guild_id = guild_obj.id
        self.standard_channel = guild_obj.channels[0]
        self.standard_channel_id = self.standard_channel.id
        self.members = guild_obj.members
        self.owner = guild_obj.owner
        self.guild_name = str(guild_obj)
        try:
            # create new message_file, throws exception if file already exists
            open(f'data/guilds/info_{self.guild_id}.json', 'x')
            self.set_default_info()
        except FileExistsError:
            pass

        self.welcome_message = self.get_data('welcome_message')
        self.default_role = self.get_data('default_role')

    def set_default_info(self):
        tmp_data = {
            'guild_name': self.guild_name,
            'guild_id': self.guild_id,
            'standard_channel_id': self.standard_channel_id,
            'members':[{member.name : member.id} for member in self.members],
            'owner': (self.owner.id, self.owner.name),
            'welcome_message': 'welcome <3',
            'default_role': 'none'
        }
        with open(f'data/guilds/info_{self.guild_id}.json', 'w') as doc:
            json.dump(tmp_data, doc)
        print(f'setting default info for guild: {self.guild_obj.name}')

    def get_guild_id(self):
        return self.guild_id

    def get_g_name(self):
        print(self.guild_name)
        return self.guild_name

    def get_welcome_message(self):
        return self.welcome_message

    def get_standard_channel_id(self):
        return self.standard_channel_id

    def set_standard_channel_id(self, new_channel):
        self.standard_channel.id = int(new_channel.id)
        self.change_data('standard_channel_id', int(new_channel))

    def set_standard_channel(self, new_channel):
        self.standard_channel = new_channel

    def get_standard_channel(self):
        return self.standard_channel
    
    def _get_user_id(self, name):
        m = next(n for n in self.members if n.name == name)
        if m:
            print(m.id)
            return m.id
        return ' '

    def get_guild_file_name(self):
        return f'data/guilds/info_{self.get_guild_id()}.json'

    def get_msg_from_input(self, input_key):
        try:
            return self.get_all_data()[input_key]
        except KeyError:
            return
    
    def get_default_role(self):
        return self.get_data('default_role')
    
    def get_members(self):
        return self.members


    def change_data(self, key, val):
        data = self.get_all_data()
        data[key] = val
        with open(self.get_guild_file_name(), 'w') as doc:
            json.dump(data, doc)
    
    # Maybe rename?
    def get_all_data(self):
        with open(self.get_guild_file_name(), 'r') as doc:
            return json.load(doc)
    
    def get_data(self, key):
        return self.get_all_data()[key]

    # TODO: remove?
    def is_guild(self, input_id):
        return input_id == self.get_guild_id()
