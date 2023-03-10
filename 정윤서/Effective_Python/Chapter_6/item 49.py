import json

class Serializable:
    def __init__(self, *args):
        self.args = args

    def serializable(self):
        return json.dumps({'args':self.args})

class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f'Point2D({self.x}, {self.y})'

point = Point2D(5, 3)
print('Object:      ', point)
print('Serialized:  ', point.serializable())
print('----------------------------------------------')

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint2D(Deserializable):
    ...

before = BetterPoint2D(5, 3)
print('Before:      ', before)
data = before.serializable()
print('Serialized:  ', data)
after = BetterPoint2D.deserialize(data)
print('After:       ', after)
print('----------------------------------------------')

class BetterSerializable:
    def __init__(self, *args):
        self.args = args
    
    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

    def __repr__(self):
        name = self.__class__.__name__
        args_str = ', '.join(str(x) for x in self.args)
        return f'{name}({args_str})'

registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(dat):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

register_class(EvenBetterPoint2D)

before = EvenBetterPoint2D(5, 3)
print('Before:      ', before)
data = before.serialize()
print('Serialized:  ', data)
after = deserialize(data)
print('After:       ', after)
print('----------------------------------------------')

class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

# Forgot to call register_class!

"""point = Point3D(5, 9, -4)
data = point.serialize()
deserialize(data)"""

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

before = Vector3D(10, -7, 3)
print('Before:      ', before)
data = before.serialize()
print('Serialized:  ', data)
print('After:       ', deserialize(data))
print('----------------------------------------------')

class BetterRegisteredSerializable(BetterSerializable):
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)

class Vector1D(BetterRegisteredSerializable):
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude

before = Vector1D(6)
print('Before:      ', before)
data = before.serialize()
print('Serialized:  ', data)
print('After:       ', deserialize(data))