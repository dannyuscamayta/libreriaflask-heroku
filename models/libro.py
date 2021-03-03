from config.base_datos import bd

# si se quiere usar algun DATATYPE especifico de una base de datos en particular
# debemos importar el dialecto para que solamente fucncione en esa base de datos
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship


class LibroModel(bd.Model):
    __tablename__ = "t_libro"
    libroId = bd.Column(name="libro_id", type_=bd.Integer,
                        primary_key=True, autoincrement=True, unique=True)
    libroNombre = bd.Column(name="libro_nombre", type_=bd.String(45))
    libroCantidad = bd.Column(name="libro_cant", type_=bd.Integer)
    # YEAR solo funciona en el dialecto mysql
    libroEdicion = bd.Column(name="libro_edicion", type_=mysql.YEAR())
    # relaciones del libro Foreign key FK
    autor = bd.Column(bd.ForeignKey('t_autor.autor_id'), name="autor_id",
                        type_=bd.Integer, nullable=False)
    categoria = bd.Column(bd.ForeignKey('t_categoria.categoria_id'), name="categoria_id",
                            type_=bd.Integer, nullable=False)

    # ----------------------------------------------------------------
    # recibe la ayuda de la ORM
    # esta linea↓ no crea las relaciones, simplemente sirve para el momento de HACER o relizar las consultas con el JOIN's
    sedes = relationship('SedeLibroModel', backref='libroSede')
    # el nombre sedeLibro no puede ser usado otra vez por eso aqui se pone libroSede
    # y es mucho mejor para hacer los controladores
    # ---------------------------------------------------------------
    # se agrega el constructor ↓

    def __init__(self, nombre, cantidad, edicion, autor, categoria):
        self.libroNombre = nombre
        self.libroCantidad = cantidad
        self.libroEdicion = edicion
        self.autor = autor
        self.categoria = categoria

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return {
            'libro_id': self.libroId,
            'libro_nombre': self.libroNombre,
            'libro_cant': self.libroCantidad,
            'libro_edicion': self.libroEdicion,
            'autor_id': self.autor,
            'categoria_id': self.categoria
        }
