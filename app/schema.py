instructions = [
    "SET CONSTRAINTS ALL DEFERRED;",
    "DROP TABLE IF EXISTS asignacion;",
    "DROP TABLE IF EXISTS material;",
    "DROP TABLE IF EXISTS herramienta;",
    "DROP TABLE IF EXISTS epp;",
    "DROP TABLE IF EXISTS usuario;",
    "DROP TABLE IF EXISTS tipo_usuario;",
    "SET CONSTRAINTS ALL IMMEDIATE;",
    """
    CREATE TABLE material(
       id_material SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL UNIQUE,
       marca VARCHAR(80) NOT NULL,
       cantidad INTEGER NOT NULL check(cantidad > 0),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE herramienta(
       id_herramienta SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL UNIQUE,
       marca VARCHAR(80) NOT NULL,
       cantidad INTEGER NOT NULL check(cantidad > 0),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE epp(
       id_epp SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL UNIQUE,
       cantidad INTEGER NOT NULL check(cantidad > 0),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE tipo_usuario(
       id_tipo SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL
    )
    """,
    """
    INSERT INTO tipo_usuario(nombre) VALUES ('admin');
    INSERT INTO tipo_usuario(nombre) VALUES ('usuario');
    """
    """
    CREATE TABLE usuario(
       id_usuario SERIAL PRIMARY KEY,
       nombre VARCHAR(80) NOT NULL,
       email VARCHAR(80) NOT NULL,
       password VARCHAR(200) NOT NULL,
       tipo_usuario INTEGER NOT NULL REFERENCES tipo_usuario(id_tipo),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE asignacion(
       id_asignacion SERIAL PRIMARY KEY,
       id_usuario INTEGER NOT NULL REFERENCES usuario(id_usuario),
       id_material INTEGER REFERENCES material(id_material),
       id_epp INTEGER REFERENCES epp(id_epp),
       id_herramienta INTEGER REFERENCES herramienta(id_herramienta),
       fecha_devolucion TIMESTAMP,
       fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       CONSTRAINT validacion_fechas CHECK (fecha_devolucion >= fecha_asignacion OR fecha_devolucion IS NULL)
    );
    """


]
