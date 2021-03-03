from sqlalchemy.orm import backref
from config.base_datos import bd
# si aun no sabemos que tipos de datos podemos utilizar en el sqlalchemy
#from sqlalchemy import types

# para crear tablas como si fueran classes


class AutorModel(bd.Model):
    # para cambiar el nombre de la tabla a crearse
    __tablename__= "t_autor"
    autorId = bd.Column(
                                name='autor_id', # todo es una columna en la tabla ejem: nombre de la columna en la base de datos bd
                                type_=bd.Integer,  # tipo de dato en la bd
                                primary_key=True,  # setear si va a ser pk o no
                                autoincrement=True,  # si va a ser auto_incrementable
                                nullable=False,  # si va a tener un valor nulo o vacio
                                unique=True, # si va a ser unique o se va a repetir
                                )

    autorNombre = bd.Column(name="autor_nombre", type_=bd.String(45))
    # ---------------------------------------------------------------------------------
    # tambien existe el  LAZY => define cuando SQLalchemy va a cargar la data de la base de datos
    # 'select' => TRUE => es el valor por defecto de lazy, signif: que SQLalchemy cargara los datos segun sea necesario
    # 'join' => FALSE => le dice  a SQLalchemy cargue la relacion en la misma consulta usando un JOIN
    # 'subquery' => trabaja como un JOIN pero en lugar de hacerlo de una misma consulta lo hara una SUBCONSULTA
    # 'dynamic => este es especial si se tiene muchos elementos y se desea aplicar muchos filtros adicionales
    # el SQLalchemy devolvera otros objeto de consulta que se puede customizar antes de cargar los elementos
    # de la base de datos(CONSUMO ALTO),  al hacer esto tener en cuenta que el proceso de lectura de la base de datos puede ser mayor, y por ende 
    # puede tener un mayor tiempo de espera (lo va a poner lento el sistema)


    # para crear relaciones con el pradre de las tablas 
    #-------------------------------------------------------------------------------------
    # el el caso de llaves foraneas o FOREIGN KEYS se apunta al nombre de la tabla
    # en el caso de RELATIONSHIP se punta al nombre del modelo
    # En el caso de RELATIONSHIP normal, la tabla no puede estar aun creada
    # https://docs.sqlalchemy.org/en/13/orm/relationship_api.html?highlight=relationship#sqlalchemy.orm.relationship
    libros = bd.relationship('LibroModel', backref='autorLibro', lazy=True)
    # ↑↑ BACKREF= sirve para crearse en el modelo hijo(para que nos devuelva los datos del padre)
    # Si no indicamos un backref, Flask lo generara aleatoriamente y sera mas complicado averiguar su nombre
    # el PADRE en la base de datos es USUALMENTE de donde sale la relacion de 1 a muchos, y un HIJO es normamlmente
    # por donde sale la relacion de muchos a UNO
    # --------------------------------------------------------------------------------
    
    # la funcion para hacer un constructor en una clase es el __init__ para su metodo post
    def __init__(self, nombreAutor):
        self.autorNombre = nombreAutor

    # ------------ metodos magicos  de python que funcionan en las classes-----------------------
    def __str__(self):
        return '{}: {}'.format(self.autorId, self.autorNombre)

    def save(self):
        # el metodo session devuelve la seccion actual y evita que se cree una nueva sesion y asi ralentizar la conexion a mi base de datos
        # el metodo add sirve para agregar toda mi instancia (mi nuevo autor) en un formato que sea valido para mi bd
        bd.session.add(self)
        # el commit sirve para que los cambios realizados a la bd se hagan efecto, esto genelmente se usa con transacciones
        bd.session.commit()

    # este metodo retornara un diccionario 
    def json(self):
        return {
            'autor_id': self.autorId,
            'autor_nombre': self.autorNombre
        }

    def delete(self):
        # con el delete se hace la ELIMINACION temporal de la BD
        # este por el momento se guarda en el disco volatil
        bd.session.delete(self)
        # el commit sera para guardar los cambios permanentemente de la BD
        bd.session.commit()
