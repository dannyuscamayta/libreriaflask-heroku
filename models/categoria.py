from config.base_datos import bd
# para que nos ayude SQLalchemy se debe importar el ORM
from sqlalchemy.orm import relationship


class CategoriaModel(bd.Model):
    # crear la tabla dr categoria en la cual el id sea pk, ai, not null, unique
    # descripcion de la categoria sea unique, no pueda ser nulo
    __tablename__ = "t_categoria"
    categoriaId = bd.Column("categoria_id",
                            type_=bd.Integer,
                            primary_key=True,
                            autoincrement=True,
                            nullable=False,
                            unique=True)
    categoriaDescripcion = bd.Column(name="categoria_descripcion",
                                        type_=bd.String(45),
                                        unique=True,
                                        nullable=False)
    #----------------------------------------------------------------
    # recibe la ayuda de la ORM
    # esta linea↓ no crea las relaciones, simplemente sirve para el momento de HACER o relizar las consultas con el JOIN's
    libros = relationship('LibroModel', backref='categoriaLibro', lazy=True)
    # ---------------------------------------------------------------
    # para llamar a las categorias desde categoria controllers es un json 
    def json(self):
        return {
            'categoria_id': self.categoriaId,
            'categoria_descripcion': self.categoriaDescripcion
        }

    def __init__(self, nombre):
        self.categoriaDescripcion = nombre

    def save(self):
        bd.session.add(self)
        bd.session.commit()