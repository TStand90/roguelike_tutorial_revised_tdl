from game_messages import Message

import item_functions


class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs

    def to_json(self):
        if self.targeting_message:
            targeting_message_json = self.targeting_message.to_json()
        else:
            targeting_message_json = None

        json_data = {
            'use_function': self.use_function.__name__,
            'targeting': self.targeting,
            'targeting_message': targeting_message_json,
            'function_kwargs': self.function_kwargs
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        use_function_name = json_data.get('use_function')
        targeting = json_data.get('targeting')
        targeting_message_json = json_data.get('targeting_message')
        function_kwargs = json_data.get('function_kwargs', {})

        if use_function_name:
            use_function = getattr(item_functions, use_function_name)
        else:
            use_function = None

        if targeting_message_json:
            targeting_message = Message.from_json(targeting_message_json)
        else:
            targeting_message = None

        item = Item(use_function, targeting, targeting_message, **function_kwargs)

        return item
