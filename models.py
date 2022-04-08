from extension import db

"""
class Recipe:
    id:int primarykey
    name:str
    description:str(Text)
"""

class Recipe(db.Model):
    Id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    description = db.Column(db.Text(),nullable=False)

    def __repr__(self) -> str:
        return f"<Recipe {self.name} />"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,title,description):
        self.title = title
        self.description = description
