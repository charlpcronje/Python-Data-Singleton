from data_singleton.base import BasePlugin

class BitwisePlugin(BasePlugin):
    def set_bit(self, value, bit_index):
        return value | (1 << bit_index)

    def clear_bit(self, value, bit_index):
        return value & ~(1 << bit_index)

    def is_bit_set(self, value, bit_index):
        return (value >> bit_index) & 1