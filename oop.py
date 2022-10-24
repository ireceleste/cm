"""
Appunti Object Oriented Programming.

Prova su OOP presa da argomenti fatti a lezione.
"""
import math
from array import array

def example_tv():
    class Television:
        """Class describing a televsion."""
    
        def __init__(self, owner):
            """
            Set variables for each object of the class.
    
            It is called every time we create an object of this class
            We can pass arguments to the constructor, just like any function.
            """
            print("Creating a television instance...")
            self.model = "Sv32X553T"  # This is a class attribute in --init--
            self.owner = owner  # This is set to the value of the argument
    
        def print_info(self):
            """Print the model and owner."""
            message = "This is television model {}, owned by {}"
            print(message.format(self.model, self.owner))
    
        NUMBER_OF_CHANNELS = 999  # This is a class attribute
    
    
    my_television = Television('Irene')
    my_television.print_info()
    
    # =============================================================================
    # CLASS ATTRIBUTES E INSTANCE ATTRIBUTES
    # =============================================================================
    
    # la class ha 2 class attributes: NUMBER_OF_CHANNELS e model
    
    print(my_television.model)
    print(Television.NUMBER_OF_CHANNELS)  # class attributes sono  della classe
    
    # class attribyres si possono modificare, o per classe o per singolo oggetto
    Television.NUMBER_OF_CHANNELS = 998
    my_television.NUMBER_OF_CHANNELS = 1000
    my_television.model = 'cdshbjn'
    
    print(Television.NUMBER_OF_CHANNELS)  # class attributes sono  della classe
    
    

def example_vector():
    
    # =============================================================================
    # PROPERTIES ED ENCAPSULATION
    # =============================================================================
    
    
    class Vector2d:
        """
        Class describing a 2d vector.
    
        In input it takes module and angle
        """
    
        def __init__(self, module, angle):
            self.module = float(module)
            self.angle = float(angle)
    
        @property
        def x(self):
            """Define x coordinate."""
            return self.module * math.cos(self.angle)
    
        @property
        def y(self):
            """Define y coordinate."""
            return self.module * math.sin(self.angle)
    
        @x.setter
        def x(self, x):  # this function must be called as the property
            """Update module and angle."""
            self.module, self.angle = math.sqrt(x**2 + self.y**2),\
                math.atan2(self.y, x)

        def print_coordinates(self):
            print(f'(x,y) = ({self.x:.2f}, {self.y:.2f})')
                        
        

    v = Vector2d(3.1622776601683795, -0.3217505543966422)
    print(v.x)
    v.x = 1.
    print(v.x, v.module, v.angle)
    v.print_coordinates()
    v2 = Vector2d(2, 0)
    v2.print_coordinates()
    v.add(v2)  # però non ci piace questa sintassi: vedi special methods
    
    

def example_special_methods():

    class Vector2d:
        """
        Class describing a 2d vector.
    
        In input it takes module and angle
        """
    
        def __init__(self, x, y):
            """
            Initialize a float vector.
        
            In input it takes x and y and float returns error if I don't give 
            a number: it can't float a string or dictionary for example
            I want private attributes to hash the objects Vector2d
            """
            self._x = float(x) 
            self._y = float(y)
        
        @property
        def x(self):
            return self._x
        
        @property
        def y(self):
            return self._y
        
        """
        # i setter li levo se voglio che sia read only
        @x.setter
        def x(self, value):
            self._x = float(value)
        
        @y.setter
        def y(self, value):
            self._y = float(value)
        """
        def __str__(self):
            """
            Dice come oggetti classe sono trasformati in stringhe
            Pensata per l'utente'
            """
            return(f"V({self.x:.3f}, {self.y:.3f})")  # Cos' si decide noi il formato
            #str((self.x, self.y))  # usa str di tupla
        
        def __repr__(self):
            """
            Dice come oggetti classe sono trasformati in stringhe
            Pensata per il debug'
            """
            return(f"Vector2d = ({self.x:.3f}, {self.y:.3f})")

# OPERAZIONI PER VETTORI 

        def __abs__(self):
            """Special method!: Module.
            Called with abs(v)
            """
            return math.sqrt(self.x**2+self.y**2)

        def __add__(self, other):
            """Special method!: Adds vector and other vector.
            Called with vector + other
            """
            return Vector2d(self.x+other.x, self.y+other.y)
        
        def __sub__(self, other):
            """Special method!: Subtracts vector and other vector
            Called with vector - other
            """
            return Vector2d(self.x-other.x, self.y-other.y)

        def __mul__(self, scalar):
            """Special method!: Multiplies vector for scalar
            Called with vector*scalar
            """
            return Vector2d(self.x*scalar, self.y*scalar)
        
        def __rmul__(self, scalar):
            """Special method!: Multiplies vector for scalar 
            Called when scalar*vector and type(scalar )(int, float...) has no 
            multiply for vector method 
            """
            return self*scalar
        
# OPERAZIONI DI IN PLACE PER VETTORI 
# OCCHIO: se gli attributi sono privati, non posso modificare self x e self y
# se voglio iadd devo togliere l'underscore e le property per x e y 
# OPPURE implementare x.setter e y.setter, ma non è più read only

        """
        def __iadd__(self, other):
            #Special method!: Adds vector and other vector
            #Called with v += other
            
            self.x += other.x
            self.y += other.y
            return(self)
        #analogamente con imul, isub, irmul...
        """

# CONFRONTO TRA VETTORI
        def __eq__(self, other):
            """Special method!: verifies if vector = other
            Called with vector == other
            """
            return((self.x, self.y) == (other.x, other.y)) 
            # sta riciclando == delle tuple

        def __gt__(self, other):
            """Special method!: verifies if module(vector) > module(other)
            Called with vector > other
            """
            return(abs(self)> abs(other))

# HASHING DI UN VETTORE
        def __hash__(self, other):
            """Special method!: hashes the vector
            Call ONLY if it's read-only (no x.setter and no iadd)
            Uses hash of numbers
            """
            return(hash(self.x) ^ hash(self.y))

    v = Vector2d(1,2)
    modulo=abs(v)
    print(modulo)

    print(v)  # Lui chiama automaticamente str e se non è implementata repr
    print(str(v))
    print(repr(v))


    v2 = Vector2d(3, 3)
    print("Sum: ", v+v2)
    print("Sub: ", v-v2)
    print("Mul: ", v*2)
    print("Rmul: ", 2*v)
    v += v*0.5
    print("iadd: ", v)
    print(v == v2)
    v3= 2*v*0.5
    print(v == v3)
    print(v > 2*v)


def example_ndvector():
    
    class Vector: 
        """ Class representing a multidimensional vector"""
        # array di python richiede un codice che dica il tipo dell'array
        # conviene definirlo come class attribute, in modo da averlo condiviso 
        # da tutte le istanze
        # array prende come secondo input lista con le componenti

        typecode = 'd'  # We use a class attribute to save the code required 
                        # for array
        def __init__(self, components): 
            self._components = array(self.typecode, components)
        
        def __repr__(self):
            class_name = type(self).__name__
            components = str(self._components)
            components = components[components.find('['): -1]
            return ("{}({}".format(class_name, components))
        
        def __getitem__(self, index):
            """ Called as vector[index]"""
            return self._components[index]
        
        def __setitem__(self, index, value):
            """ Called as vector[index]=value"""
            self._components[index] = value

        def __len__(self):
            return(len(self._components))
        
        def __iter__(self):
            """ 
            Tell Python how to iter.
            
            Called as for element in vector: 
            Per ora usiamo iteratore di array
            
            """
            return iter(self._components)
        # una volta che il vettore è iterabile, possiamo usare vettore ogni 
        # volta che a Python serve un iterabile: ci sono tante funzioni che 
        # accettano input come iterabili, come il costruttore di array: si può
        # creare un vettore da un altro vettore, oppure usare zip



    v = Vector([1., 2., 3.])
    print(v)
    v[1] = 5.  # setitem
    print(v[1])  # getitem
    for element in v:  # iter
        print(element)
    v2 = Vector(v)  # questo solo  possibile se Vector è iterabile
    print(v2)
    
    for element1, element2 in zip(v, v2):
        print(element1, element2)





if __name__ == '__main__':
    #example_tv()
    #example_vector()
    #example_special_methods()
    example_ndvector()