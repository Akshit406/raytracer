from vector import Vector

class Color(Vector):
    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0

        return cls(x, y, z)
    
    def __repr__(self):
        return f"Color({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
