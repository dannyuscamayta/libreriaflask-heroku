from flask.globals import session
from config.base_datos import bd
from sqlalchemy.orm import relationship
#from sqlalchemy import types

class SedeModel(bd.Model):
    # sie es que se quiere cambiar el nombre de la tabla, columnas se debe poner sto primero __tablename__="t_sede"    
    __tablename__ = "t_sede"
    sedeId = bd.Column(name="sede_id", type_=bd.Integer, primary_key=True, autoincrement=True, unique=True)
    sedeUbicacion = bd.Column(name="sede_ubicacion", type_=bd.String(45))
    # con el tipo de dato DECIMAL se pueden indicar el total de numeros y el total de decimales
    sedeLatitud = bd.Column(name="sede_latitud", type_=bd.DECIMAL(9,7), nullable=False)
    sedeLongitud = bd.Column(name="sede_longitud", type_=bd.DECIMAL(9,7), nullable=False)

    #-----------------------------------------------------------------
    # el lazy es opcional y su valor es por defecto True
    libros = relationship('SedeLibroModel', backref='sedeLibro')
# creando relaciones del libro y debemos tenr la categoria

# -----------------------------------------------------------------
# constructor de la sede
    def __init__(self, ubicacion, latitud, longitud):
        self.sedeUbicacion = ubicacion
        self.sedeLatitud = latitud
        self.sedeLongitud = longitud

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return {
            'sede_id': self.sedeId,
            'sede_ubicacion': self.sedeUbicacion,
            # los valores de la longitud  y latitud son decimales , es por eso que no se puede hacer hacer la conversion
            # de los datos automaticamente y por eso se le coloca el str(bla,bla, bla) NO lo puede INTEPRETAR el front-end
            'sede_latitud': str(self.sedeLatitud),
            'sede_longitud': str(self.sedeLongitud)
        }