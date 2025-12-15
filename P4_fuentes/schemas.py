from marshmallow import Schema, fields, validate

class VideoSchema(Schema):
    id = fields.Int(required=True)
    titulo = fields.Str(required=True)
    fecha = fields.Str(required=True) # Formato string simple como pide P3
    id_paises = fields.List(fields.Int(), required=True)

class UserRegisterSchema(Schema):
    # Esquema para el registro (entrada)
    nombre = fields.Str(required=True) # Esto será el username
    password = fields.Str(required=True)
    id = fields.Int(required=True)
    id_pais = fields.Int(required=True)
    id_historial = fields.Int(required=True)
    # es_admin y esta_suscripto se manejan por lógica interna al crear