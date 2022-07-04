import os
import base64
from io import BytesIO
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class ImageDataSet(Dataset):
    def __init__(self, path, l, format):
        
        self.images = []
        self.paths = []
        self.format = format

        for filemames in l:
            self.images.append(os.path.join(path, filemames))
            self.paths.append(os.path.join(path, filemames))

        self.transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])

    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        filepath = self.paths[idx]
        img = Image.open(self.images[idx])
        rgb_img = img.convert('RGB')
        buffer = BytesIO()
        rgb_img.save(buffer, self.format)
        buffer.seek(0)
        img_base64 = "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode('utf-8')
        data = self.transform(rgb_img)
        buffer.close()
        rgb_img.close()
        img.close()
        return data, filepath, img_base64