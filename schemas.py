from pydantic import BaseModel, Field

class ImageDetails(BaseModel):
    image_path : str = Field(description = 'store the file path of the image')
    title : str = Field(description = 'store the phrase that captures the essence of the image')
    keywords : list[str] = Field(description = 'store the keywords that cold be identifying features of the image in a list format')