from fastapi import UploadFile, HTTPException


class ImageFilesValidator:
    SUPPORTED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

    def __call__(self, files: list[UploadFile]):
        valid = []
        for file in files:
            if file.filename.split(".")[-1].lower() in self.SUPPORTED_EXTENSIONS:
                valid.append(file)

        if not valid:
            raise HTTPException(status_code=400, detail="No valid image files found")

        return valid
