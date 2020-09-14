from marshmallow import Schema, fields


class TodoItemSchema(Schema):
    todoId = fields.Str()
    title = fields.Str()
    content = fields.Str()
    updatedAt = fields.Str()


todo_item_schema = TodoItemSchema()
todo_items_schema = TodoItemSchema(many=True)
