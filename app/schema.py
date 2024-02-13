instructions = [
    "SET CONSTRAINTS ALL DEFERRED;",
    "DROP TABLE IF EXISTS asignacion;",
    "DROP TABLE IF EXISTS producto;",
    "DROP TABLE IF EXISTS tipo_producto;",
    "DROP TABLE IF EXISTS usuario;",
    "DROP TABLE IF EXISTS tipo_usuario;",
    "SET CONSTRAINTS ALL IMMEDIATE;",

    """
   CREATE TABLE tipo_producto (
      id_tipo_producto SERIAL PRIMARY KEY,
      nombre VARCHAR(80) NOT NULL
   )
   """,
    """
   INSERT INTO tipo_producto(nombre) VALUES ('Material');
   INSERT INTO tipo_producto(nombre) VALUES ('Herramienta');
   INSERT INTO tipo_producto(nombre) VALUES ('EPP');

   """,
    """
      CREATE TABLE producto(
       id_producto SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL UNIQUE,
       marca VARCHAR(80) NOT NULL,
       imagen VARCHAR(200) NOT NULL,
       cantidad INTEGER NOT NULL check(cantidad > 0),
       tipo_producto INTEGER NOT NULL REFERENCES tipo_producto(id_tipo_producto),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE tipo_usuario(
       id_tipo_usuario SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL
    )
    """,
    """
    INSERT INTO tipo_usuario(nombre) VALUES ('admin');
    INSERT INTO tipo_usuario(nombre) VALUES ('usuario');
    """,
    """
    CREATE TABLE usuario(
       id_usuario SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL,
       email VARCHAR(80) NOT NULL,
       password VARCHAR(200) NOT NULL,
       tipo_usuario INTEGER NOT NULL REFERENCES tipo_usuario(id_tipo_usuario),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE asignacion(
       id_asignacion SERIAL PRIMARY KEY,
       id_usuario INTEGER NOT NULL REFERENCES usuario(id_usuario),
       id_producto INTEGER NOT NULL REFERENCES producto(id_producto),
       fecha_devolucion TIMESTAMP,
       fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       CONSTRAINT validacion_fechas CHECK (fecha_devolucion >= fecha_asignacion OR fecha_devolucion IS NULL)
    );
    """


]
